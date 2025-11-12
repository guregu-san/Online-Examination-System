import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import CreateExamPage from "./pages/CreateExamPage";
import ExamEditorPage from "./pages/ExamEditorPage";
import InstructorExamsPage from "./pages/InstructorExamsPage";
import "bootstrap/dist/css/bootstrap.min.css";

export default function App() {
  return (
    <Router>
      <nav className="navbar navbar-expand navbar-dark bg-dark px-3">
        <Link className="navbar-brand" to="/">Exam Creator</Link>
        <div className="navbar-nav">
          <Link className="nav-link" to="/">Create</Link>
          <Link className="nav-link" to="/exams">My Exams</Link>
        </div>
      </nav>
      <div className="container py-4">
        <Routes>
          <Route path="/" element={<CreateExamPage />} />
          <Route path="/edit/:id" element={<ExamEditorPage />} />
          <Route path="/exams" element={<InstructorExamsPage />} />
        </Routes>
      </div>
    </Router>
  );
}
