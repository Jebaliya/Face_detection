import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import LiveCamera from "./pages/LiveCamera";
import AttendanceLog from "./pages/AttendanceLog";
import RegisterPeople from "./pages/RegisterPeople";
import { ToastProvider } from "./components/ToastContext";

export default function App() {
  return (
    <ToastProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<Layout />}>
            <Route index element={<LiveCamera />} />
            <Route path="log" element={<AttendanceLog />} />
            <Route path="register" element={<RegisterPeople />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </ToastProvider>
  );
}
