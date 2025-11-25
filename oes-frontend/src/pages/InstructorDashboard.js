import React, { useEffect, useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

function InstructorDashboard() {
  const [email, setEmail] = useState("teacher@uni.com");
  const [exams, setExams] = useState([]);

  async function loadExams() {
    try {
      const res = await axios.get(`http://localhost:5000/exams/instructor/${email}`);
      setExams(res.data);
    } catch (e) {
      console.error(e);
    }
  }

  useEffect(() => {
    loadExams();
  }, []);

  return (
    <div>
      <h3>Instructor Dashboard</h3>

      <label className="form-label mt-2">Instructor Email</label>
      <input
        className="form-control"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <button className="btn btn-primary mt-3" onClick={loadExams}>
        Load Exams
      </button>

      <ul className="list-group mt-4">
        {exams.map((exam) => (
          <li key={exam.exam_id} className="list-group-item d-flex justify-content-between">
            <span>
              {exam.title} — {exam.course_code}
            </span>
            <Link className="btn btn-sm btn-outline-primary" to={`/exam/${exam.exam_id}/edit`}>
              Edit Exam
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default InstructorDashboard;
