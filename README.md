# Face detection

Face detection is a face recognition system for managing attendance using a webcam and a modern web interface. It combines a FastAPI backend with a React frontend to support live recognition, person registration, and attendance logging.

## Overview

- Backend: FastAPI service with OpenCV YuNet and SFace for face detection and recognition
- Frontend: Vite + React single-page application with three main views
- Storage: Registered face images and metadata are stored locally for the application# Face Detection.

A real-time face recognition system for managing attendance using a webcam and a modern web interface. It combines a **FastAPI** backend with a **React** frontend to support live recognition, person registration, and attendance logging.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Node](https://img.shields.io/badge/Node.js-18%2B-green)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)
![React](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB)

---

## 📖 Overview

- **Backend:** FastAPI service with OpenCV **YuNet** and **SFace** for face detection and recognition
- **Frontend:** Vite + React single-page application with three main views
- **Storage:** Registered face images and metadata are stored locally for the application

---

## 🧠 Models Used

This project uses two lightweight, ONNX-based deep learning models from OpenCV's Zoo, chosen for their speed and accuracy in real-time, CPU-friendly applications.

### 1. YuNet — Face Detection

- **Purpose:** Locates faces in a video frame before recognition happens.
- **Type:** Lightweight CNN-based face detector, optimized for edge devices and real-time inference.
- **Highlights:**
  - Very fast, works well even without a GPU
  - Detects multiple faces per frame along with facial landmarks (eyes, nose, mouth corners)
  - Outputs bounding boxes + confidence scores used to crop faces for the recognition stage

### 2. SFace — Face Recognition

- **Purpose:** Converts a detected face into a numerical embedding (feature vector) that uniquely represents that person.
- **Type:** Deep metric learning model trained for face verification/recognition.
- **Highlights:**
  - Generates a 128-d (or similar) embedding vector per face
  - Recognition is done by comparing embeddings using cosine similarity/distance
  - Robust to minor changes in lighting, angle, and expression

> Both models are stored as `.onnx` files inside `backend/models/` and are loaded via `models_loader.py` at application startup using OpenCV's DNN module (`cv2.dnn`).

**Pipeline flow:**

```
Camera Frame → YuNet (detect face) → Crop face → SFace (generate embedding)
      → Compare with known_faces embeddings → Match found? → Log attendance
```

---

## 📁 Project Structure

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
│   ├── models/                # ONNX model files used by the face pipeline (YuNet + SFace)
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
│   └── vite.config.js         # Vite proxy and development configuration
└── README.md
```

---

## ✨ Features

- 📷 Live face recognition from a camera feed
- 🧑‍💼 Registration of new people with face images
- 🗂️ Viewing attendance logs
- 💻 Clean, responsive interface for desktop and tablet use

---

## ⚙️ Requirements

- Python 3.10+
- Node.js 18+
- A working camera device

---

## 🚀 Backend Setup

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows PowerShell
pip install -r requirements.txt
python run.py
```

The backend runs at **http://localhost:8000**.

---

## 🎨 Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend runs at **http://localhost:5173** and connects to the backend API automatically.

---

## 📦 Production Build

```bash
cd frontend
npm run build
```

The build output is generated in the `frontend/dist` directory for deployment.

---

## 🛠️ Tech Stack

| Layer            | Technology          |
| ---------------- | ------------------- |
| Backend          | FastAPI, Python     |
| Face Detection   | OpenCV YuNet (ONNX) |
| Face Recognition | OpenCV SFace (ONNX) |
| Frontend         | React, Vite         |
| Styling          | CSS Modules         |

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome. Feel free to fork the repo and submit a pull request.

## 📄 License

This project is licensed under the MIT License.

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
