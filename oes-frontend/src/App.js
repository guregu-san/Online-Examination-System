import React from "react";
import { Routes, Route, Link } from "react-router-dom";
import ExamSetup from "./pages/ExamSetup";
import ExamEditor from "./pages/ExamEditor";
import PreviewExamPage from "./pages/PreviewExamPage";
import InstructorDashboard from "./pages/InstructorDashboard";
import ITSupportTools from "./pages/ITSupportTools";

function App() {
  return (
    <>
      <nav className="navbar navbar-dark bg-dark navbar-expand-lg">
        <div className="container-fluid">
          <Link className="navbar-brand" to="/">
            OES System
          </Link>

          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#menu">
            <span className="navbar-toggler-icon"></span>
          </button>

          <div id="menu" className="collapse navbar-collapse">
            <ul className="navbar-nav">
              <li className="nav-item">
                <Link className="nav-link" to="/">Create Exam</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/instructor">Instructor Home</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/it-tools">IT Support</Link>
              </li>
            </ul>
          </div>
        </div>
      </nav>

      <main className="container mt-4">
        <Routes>
          <Route path="/" element={<ExamSetup />} />
          <Route path="/exam/:examId/edit" element={<ExamEditor />} />
          <Route path="/exam/:examId/preview" element={<PreviewExamPage />} />
          <Route path="/instructor" element={<InstructorDashboard />} />
          <Route path="/it-tools" element={<ITSupportTools />} />
        </Routes>
      </main>
    </>
  );
}

export default App;
