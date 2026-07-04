// Thin wrapper around fetch for the backend API.
// Vite's dev proxy forwards /api/* to the FastAPI server (see vite.config.js),
// so relative paths work in both dev and a same-origin production build.

// In dev, Vite's proxy forwards /api/* to localhost:8000 (see vite.config.js),
// so the default "/api" works with no setup. In production (e.g. Vercel), set
// VITE_API_BASE_URL to your deployed backend's URL, e.g.:
//   VITE_API_BASE_URL=https://face-attendance-backend.onrender.com/api
const BASE = import.meta.env.VITE_API_BASE_URL || "/api";

async function asJson(res) {
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const err = new Error(data.detail || "Request failed");
    err.status = res.status;
    err.data = data;
    throw err;
  }
  return data;
}

export const api = {
  recognize: (imageDataUrl) =>
    fetch(`${BASE}/recognize`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image: imageDataUrl }),
    }).then(asJson),

  register: (name, file) => {
    const fd = new FormData();
    fd.append("name", name);
    fd.append("image", file);
    return fetch(`${BASE}/register`, { method: "POST", body: fd }).then(asJson);
  },

  getRegistered: () => fetch(`${BASE}/registered`).then(asJson),

  removeRegistered: (name) =>
    fetch(`${BASE}/registered/${encodeURIComponent(name)}`, {
      method: "DELETE",
    }).then(asJson),

  getAttendance: () => fetch(`${BASE}/attendance`).then(asJson),

  clearAttendance: () =>
    fetch(`${BASE}/attendance`, { method: "DELETE" }).then(asJson),
};
