import React, { useEffect, useState } from "react";
import axios from "axios";
import { useParams, Link } from "react-router-dom";

function ExamSubmissionsList() {
  const { examId } = useParams();
  const [submissions, setSubmissions] = useState([]);
  const [statusFilter, setStatusFilter] = useState("");
  const [error, setError] = useState("");

  async function loadSubmissions() {
    setError("");
    try {
      let url = `http://localhost:5000/grading/exams/${examId}/submissions`;
      if (statusFilter) {
        url += `?status=${encodeURIComponent(statusFilter)}`;
      }
      const res = await axios.get(url);
      setSubmissions(res.data);
    } catch (err) {
      console.error(err);
      setError("Failed to load submissions");
    }
  }

  useEffect(() => {
    loadSubmissions();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [examId, statusFilter]);

  return (
    <div>
      <h3>Submissions for Exam #{examId}</h3>

      <div className="d-flex align-items-center mt-3">
        <label className="me-2 mb-0">Filter by status:</label>
        <select
          className="form-select w-auto"
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
        >
          <option value="">All</option>
          <option value="SUBMITTED">SUBMITTED</option>
          <option value="IN_REVIEW">IN_REVIEW</option>
          <option value="GRADED">GRADED</option>
        </select>
      </div>

      <button className="btn btn-secondary btn-sm mt-2" onClick={loadSubmissions}>
        Refresh
      </button>

      {error && <div className="alert alert-danger mt-3">{error}</div>}

      <table className="table table-striped mt-3">
        <thead>
          <tr>
            <th>Submission ID</th>
            <th>Roll Number</th>
            <th>Student Name</th>
            <th>Submitted At</th>
            <th>Status</th>
            <th>Total Score</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {submissions.map((s) => (
            <tr key={s.submission_id}>
              <td>{s.submission_id}</td>
              <td>{s.roll_number}</td>
              <td>{s.student_name}</td>
              <td>{s.submitted_at}</td>
              <td>{s.status}</td>
              <td>{s.total_score}</td>
              <td>
                <Link
                  className="btn btn-sm btn-outline-primary"
                  to={`/instructor/grading/submissions/${s.submission_id}`}
                >
                  Review
                </Link>
              </td>
            </tr>
          ))}
          {submissions.length === 0 && (
            <tr>
              <td colSpan="7" className="text-center">
                No submissions found.
              </td>
            </tr>
          )}
        </tbody>
      </table>

      <Link className="btn btn-link mt-3" to="/instructor/grading">
        ← Back to Manual Grading Dashboard
      </Link>
    </div>
  );
}

export default ExamSubmissionsList;
