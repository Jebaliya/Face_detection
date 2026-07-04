"""
Central configuration: paths, model URLs, and tunables.
"""

from pathlib import Path
import os

# ── Paths ────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
KNOWN_FACES_DIR = BASE_DIR / "known_faces"
MODELS_DIR = BASE_DIR / "models"

KNOWN_FACES_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)

# ── Model files (OpenCV Zoo — auto-downloaded) ──────────────
YUNET_URL = (
    "https://github.com/opencv/opencv_zoo/raw/main/"
    "models/face_detection_yunet/face_detection_yunet_2023mar.onnx"
)
SFACE_URL = (
    "https://github.com/opencv/opencv_zoo/raw/main/"
    "models/face_recognition_sface/face_recognition_sface_2021dec.onnx"
)
YUNET_PATH = MODELS_DIR / "face_detection_yunet_2023mar.onnx"
SFACE_PATH = MODELS_DIR / "face_recognition_sface_2021dec.onnx"

# SFace cosine similarity threshold (OpenCV-recommended default)
COSINE_THRESHOLD = 0.363

# UI-facing score mapping range (raw threshold..1.0  ->  0.80..0.99)
SCORE_UI_MIN = 0.80
SCORE_UI_MAX = 0.99

# CORS: origins allowed to call this API (Vite dev server, etc.)
# Add your deployed Vercel URL via the CORS_EXTRA_ORIGINS env var
# (comma-separated), e.g. "https://my-app.vercel.app"
_extra_origins = os.environ.get("CORS_EXTRA_ORIGINS", "")
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
] + [o.strip() for o in _extra_origins.split(",") if o.strip()]