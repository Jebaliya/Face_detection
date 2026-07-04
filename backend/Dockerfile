FROM python:3.12-slim

# Install system libraries required by OpenCV (cv2):
#   libxcb        — X protocol C-language Binding (libxcb.so.1)
#   libxkbcommon  — XKB keyboard handling
#   libxrender    — X Rendering Extension client library
#   libxext       — X11 miscellaneous extensions
#   libgl1        — OpenGL (libGL.so.1, pulled in by opencv-python)
#   libglib2.0-0  — GLib (libgthread-2.0, required by OpenCV highgui)
# build-essential + wget are included for any native-extension pip packages.
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        wget \
        libxcb1 \
        libxkbcommon-x11-0 \
        libxrender1 \
        libxext6 \
        libgl1 \
        libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first (layer-cache friendly)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
