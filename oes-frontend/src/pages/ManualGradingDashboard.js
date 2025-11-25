import React, { useEffect, useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

function ManualGradingDashboard() {
  const [email, setEmail] = useState("teacher@uni.com");
  const [exams, setExams] = useState([]);
  const [error, setError] = useState("");

  async function loadDashboard() {
    setError("");
    try {
      const res = await axios.get(
        `http://localhost:5000/grading/dashboard/${encodeURIComponent(email)}`
      );
      setExams(res.data);
    } catch (err) {
      console.error(err);
      setError("Failed to load manual grading dashboard");
    }
  }

  useEffect(() => {
    loadDashboard();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div>
      <h3>Manual Grading Dashboard</h3>

      <label className="form-label mt-2">Instructor Email</label>
      <input
        className="form-control"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <button className="btn btn-primary mt-3" onClick={loadDashboard}>
        Load Manual Grading
      </button>

      {error && <div className="alert alert-danger mt-3">{error}</div>}

      <ul className="list-group mt-4">
        {exams.map((exam) => (
          <li
            key={exam.exam_id}
            className="list-group-item d-flex justify-content-between align-items-center"
          >
            <div>
              <strong>{exam.title}</strong> — {exam.course_code}
              <div className="small text-muted">
                Total: {exam.total_submissions} | In review: {exam.in_review} | Graded:{" "}
                {exam.graded}
              </div>
            </div>

            <Link
              className="btn btn-sm btn-outline-primary"
              to={`/instructor/grading/exams/${exam.exam_id}/submissions`}
            >
              View Submissions
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ManualGradingDashboard;
