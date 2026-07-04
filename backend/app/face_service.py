"""
FaceService: owns the detector/recognizer models plus the in-memory
known-faces and attendance state, and exposes the operations the API
routers need. Wrapping this in a class (instead of module-level globals)
keeps state ownership explicit and makes the service easy to test.
"""

from datetime import datetime, date
from pathlib import Path

import cv2
import numpy as np

from .config import KNOWN_FACES_DIR, COSINE_THRESHOLD, SCORE_UI_MIN, SCORE_UI_MAX
from .models_loader import init_models


class FaceService:
    def __init__(self) -> None:
        self.detector: cv2.FaceDetectorYN | None = None
        self.recognizer: cv2.FaceRecognizerSF | None = None
        self.known_features: dict[str, np.ndarray] = {}   # name -> feature vector
        self.attendance_log: dict[str, dict] = {}          # name -> {time, date, score}

    # ── Lifecycle ────────────────────────────────────────────
    def startup(self) -> None:
        self.detector, self.recognizer = init_models()
        self.load_known_faces()

    # ── Low-level face ops ───────────────────────────────────
    def extract_feature(self, img: np.ndarray):
        """Detect the largest face and return its feature vector, or None."""
        h, w = img.shape[:2]
        self.detector.setInputSize((w, h))
        _, faces = self.detector.detect(img)
        if faces is None or len(faces) == 0:
            return None
        aligned = self.recognizer.alignCrop(img, faces[0])
        return self.recognizer.feature(aligned)

    def detect_all(self, img: np.ndarray) -> list[dict]:
        """Detect every face -> [{feature, left, top, right, bottom}, ...]."""
        h, w = img.shape[:2]
        self.detector.setInputSize((w, h))
        _, faces = self.detector.detect(img)
        if faces is None:
            return []
        results = []
        for f in faces:
            aligned = self.recognizer.alignCrop(img, f)
            feat = self.recognizer.feature(aligned)
            x, y, fw, fh = int(f[0]), int(f[1]), int(f[2]), int(f[3])
            results.append({
                "feature": feat,
                "left": x, "top": y,
                "right": x + fw, "bottom": y + fh,
            })
        return results

    def match_face(self, feat: np.ndarray) -> tuple[str, float]:
        """Compare a feature vector against all known faces -> (name, score)."""
        best_name, best_score = "Unknown", 0.0
        for name, kf in self.known_features.items():
            score = self.recognizer.match(feat, kf, cv2.FaceRecognizerSF_FR_COSINE)
            if score > best_score:
                best_score, best_name = score, name

        if best_score >= COSINE_THRESHOLD:
            # Scale raw score into an intuitive UI range
            mapped = SCORE_UI_MIN + (
                (best_score - COSINE_THRESHOLD) / (1.0 - COSINE_THRESHOLD)
            ) * (SCORE_UI_MAX - SCORE_UI_MIN)
            return best_name, float(mapped)

        return "Unknown", float(best_score)

    # ── Known faces persistence ──────────────────────────────
    def load_known_faces(self) -> None:
        """Scan known_faces/ dir, compute features for every saved image."""
        self.known_features.clear()
        for p in KNOWN_FACES_DIR.iterdir():
            if p.suffix.lower() in (".jpg", ".jpeg", ".png"):
                img = cv2.imread(str(p))
                if img is None:
                    continue
                feat = self.extract_feature(img)
                if feat is not None:
                    self.known_features[p.stem] = feat
                    print(f"  OK {p.stem}")
        print(f"  {len(self.known_features)} registered face(s)")

    def register_face(self, clean_name: str, img: np.ndarray) -> np.ndarray | None:
        """Validate + save a new face image. Returns the feature vector, or None."""
        feat = self.extract_feature(img)
        if feat is None:
            return None
        cv2.imwrite(str(KNOWN_FACES_DIR / f"{clean_name}.jpg"), img)
        self.known_features[clean_name] = feat
        return feat

    def remove_registered(self, name: str) -> bool:
        if name not in self.known_features:
            return False
        del self.known_features[name]
        (KNOWN_FACES_DIR / f"{name}.jpg").unlink(missing_ok=True)
        self.attendance_log.pop(name, None)
        return True

    # ── Attendance ────────────────────────────────────────────
    def recognize_and_log(self, img: np.ndarray) -> list[dict]:
        """Detect+recognize every face in `img`, logging first sighting today."""
        today_str = date.today().isoformat()
        now_str = datetime.now().strftime("%I:%M:%S %p")
        faces = []

        for d in self.detect_all(img):
            name, score = self.match_face(d["feature"])

            if name != "Unknown":
                existing = self.attendance_log.get(name)
                if existing is None or existing["date"] != today_str:
                    self.attendance_log[name] = {
                        "time": now_str, "date": today_str, "score": score,
                    }
                elif score > existing.get("score", 0.0):
                    existing["score"] = score

            faces.append({
                "name": name,
                "score": score,
                "left": d["left"], "top": d["top"],
                "right": d["right"], "bottom": d["bottom"],
            })

        return faces

    def get_todays_attendance(self) -> list[dict]:
        today = date.today().isoformat()
        records = [
            {"name": n, "time": i["time"], "date": i["date"], "score": i.get("score", 0.0)}
            for n, i in self.attendance_log.items()
            if i["date"] == today
        ]
        records.sort(key=lambda r: r["time"])
        return records

    def clear_attendance(self) -> None:
        self.attendance_log.clear()


# Singleton instance shared across the app / routers
face_service = FaceService()
