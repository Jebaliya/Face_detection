import { useEffect, useState } from "react";
import { api } from "../api";
import { useToast } from "../components/ToastContext";
import "../styles/log.css";

export default function AttendanceLog() {
  const toast = useToast();
  const [records, setRecords] = useState([]);
  const currentDate = new Date().toLocaleDateString("en-US", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  async function loadAttendance() {
    try {
      const data = await api.getAttendance();
      setRecords(data.records);
    } catch (_) {
      /* silent */
    }
  }

  useEffect(() => {
    loadAttendance();
    const id = setInterval(loadAttendance, 3000);
    return () => clearInterval(id);
  }, []);

  async function clearAttendance() {
    if (!confirm("Clear all attendance records for today?")) return;
    try {
      await api.clearAttendance();
      toast("Attendance cleared", "info");
      loadAttendance();
    } catch (_) {
      /* silent */
    }
  }

  return (
    <section className="card attendance-section">
      <div className="card-header">
        <h2>
          📋 Attendance Log &mdash; <span>{currentDate}</span>
        </h2>
        <div className="header-right">
          <span className="count-badge">{records.length}</span>
          <button className="btn btn-outline" onClick={clearAttendance}>
            Clear
          </button>
        </div>
      </div>
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Name</th>
              <th>Time</th>
              <th>Score</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {records.length === 0 ? (
              <tr className="empty-row">
                <td colSpan={5}>No attendance recorded yet</td>
              </tr>
            ) : (
              records.map((r, i) => (
                <tr className="fade-in" key={r.name}>
                  <td>{i + 1}</td>
                  <td>
                    <strong>{r.name}</strong>
                  </td>
                  <td>{r.time}</td>
                  <td>{r.score ? (r.score * 100).toFixed(1) + "%" : "-"}</td>
                  <td>
                    <span className="badge badge-present">Present</span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}
