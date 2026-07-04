import { NavLink, Outlet } from "react-router-dom";

export default function Layout() {
  return (
    <>
      <header>
        <div className="header-content">
          <h1>Face detection</h1>
          <p>Real-time face detection &amp; tracking</p>
        </div>
        <nav className="nav-bar">
          <NavLink to="/" end className={({ isActive }) => `nav-link${isActive ? " active" : ""}`}>
            Live Camera
          </NavLink>
          <NavLink to="/log" className={({ isActive }) => `nav-link${isActive ? " active" : ""}`}>
            Attendance Log
          </NavLink>
          <NavLink to="/register" className={({ isActive }) => `nav-link${isActive ? " active" : ""}`}>
            Register People
          </NavLink>
        </nav>
      </header>

      <main>
        <Outlet />
      </main>
    </>
  );
}
