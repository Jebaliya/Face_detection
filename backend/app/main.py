"""
Face Recognition Attendance System — FastAPI Backend (API-only)

Uses OpenCV's built-in YuNet (face detection) + SFace (face recognition).
Models auto-download on first run (~37 MB total). No dlib, no TensorFlow.

This app now serves JSON only — the frontend is a separate React (Vite)
app that talks to it over HTTP (see ../../frontend). CORS is enabled for
the Vite dev server origin (see app/config.py -> ALLOWED_ORIGINS).
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import ALLOWED_ORIGINS
from .face_service import face_service
from .routers import recognition, registration, attendance


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n-- Startup -------------------------")
    face_service.startup()
    print("-- Ready -- http://localhost:8000\n")
    yield


app = FastAPI(title="Face Attendance API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recognition.router)
app.include_router(registration.router)
app.include_router(attendance.router)


@app.get("/api/health")
async def health():
    return {"status": "ok", "registered": len(face_service.known_features)}
