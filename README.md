# Face detection

Face detection is a face recognition system for managing attendance using a webcam and a modern web interface. It combines a FastAPI backend with a React frontend to support live recognition, person registration, and attendance logging.

## Overview

- Backend: FastAPI service with OpenCV YuNet and SFace for face detection and recognition
- Frontend: Vite + React single-page application with three main views
- Storage: Registered face images and metadata are stored locally for the application

## Project Structure

```text
project/
├── backend/
│   ├── app/
│   │   ├── routers/           # API endpoints for attendance, recognition, and registration
│   │   ├── config.py          # Application settings and CORS configuration
│   │   ├── face_service.py    # Core face detection and recognition logic
│   │   ├── main.py            # FastAPI app initialization
│   │   ├── models_loader.py   # Model loading and setup
│   │   └── utils.py           # Helper utilities
│   ├── models/                # ONNX model files used by the face pipeline
│   ├── known_faces/           # Stored images for registered individuals
│   ├── requirements.txt       # Python dependencies
│   └── run.py                 # Backend entry point
├── frontend/
│   ├── public/                # Static assets
│   ├── src/
│   │   ├── api.js             # API communication helper
│   │   ├── App.jsx            # App routing and layout entry
│   │   ├── main.jsx           # React application bootstrap
│   │   ├── components/        # Shared UI components
│   │   ├── pages/             # Camera, log, and registration pages
│   │   └── styles/            # CSS modules and shared styling
│   ├── package.json           # Frontend dependencies and scripts
│   └── vite.config.js        # Vite proxy and development configuration
└── README.md
```

## Features

- Live face recognition from a camera feed
- Registration of new people with face images
- Viewing attendance logs
- Clean, responsive interface for desktop and tablet use

## Requirements

- Python 3.10+
- Node.js 18+
- A working camera device

## Backend Setup

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows PowerShell
pip install -r requirements.txt
python run.py
```

The backend runs at http://localhost:8000.

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend runs at http://localhost:5173 and connects to the backend API automatically.

## Production Build

```bash
cd frontend
npm run build
```

The build output is generated in the frontend/dist directory for deployment.
