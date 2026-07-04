# Face Attendance — React + FastAPI

Converted from the original static HTML/CSS/JS + FastAPI app into:

- **backend/** — FastAPI, refactored into a small `app/` package
  (config, models loader, face service, routers) instead of one big `main.py`.
  Same OpenCV YuNet + SFace pipeline, same API contract.
- **frontend/** — React (Vite) single-page app with 3 routes:
  `/` (Live Camera), `/log` (Attendance Log), `/register` (Register People).

## Run the backend

```bash
cd backend
python -m venv venv && source venv/bin/activate   # optional but recommended
pip install -r requirements.txt
python run.py
```

Starts on `http://localhost:8000`. First run downloads ~37 MB of ONNX models
into `backend/models/`. Registered face photos are stored in `backend/known_faces/`.

## Run the frontend

```bash
cd frontend
npm install
npm run dev
```

Starts on `http://localhost:5173`. The Vite dev server proxies `/api/*` calls
to `http://localhost:8000` (see `vite.config.js`), so just run both and open
`http://localhost:5173`.

## Production build

```bash
cd frontend
npm run build      # outputs static files to frontend/dist
```

Serve `frontend/dist` with any static host (nginx, the backend itself via
`StaticFiles`, Vercel, etc.) and point it at your deployed FastAPI URL — update
`ALLOWED_ORIGINS` in `backend/app/config.py` accordingly.

## What changed from the original

- `main.py` split into `config.py`, `models_loader.py`, `face_service.py`
  (a `FaceService` class replacing module-level globals), and `routers/`
  (`recognition.py`, `registration.py`, `attendance.py`).
- Backend is now API-only (no more `FileResponse` HTML routes) + CORS enabled,
  since the frontend is a separate Vite app.
- All three HTML pages became React components (`LiveCamera`, `AttendanceLog`,
  `RegisterPeople`) sharing a `Layout` (header/nav) and a `ToastProvider`.
- `style.css` split by concern (`layout.css`, `camera.css`, `log.css`,
  `register.css`) but kept the same design tokens/colors — same look and feel.
