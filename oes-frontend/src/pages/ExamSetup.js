import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function ExamSetup() {
  const [courseCode, setCourseCode] = useState("");
  const [instructorEmail, setInstructorEmail] = useState("");
  const [title] = useState("Midterm Exam");
  const [timeLimit] = useState(60);
  const [security] = useState("shuffle=true");
  const [error, setError] = useState("");

  const navigate = useNavigate();

  async function handleCreate() {
    setError("");

    if (!courseCode.trim() || !instructorEmail.trim()) {
      setError("Course Code and Instructor Email are required");
      return;
    }

    try {
      const res = await axios.post("http://localhost:5000/exams", {
        course_code: courseCode,
        instructor_email: instructorEmail,
        title,
        time_limit: timeLimit,
        security_settings: security,
      });

      const examId = res.data.exam_id;

      navigate(`/exam/${examId}/edit`, {
        state: { courseCode, instructorEmail },
      });
    } catch (err) {
      setError(err.response?.data?.error || "Failed to create exam");
    }
  }

  return (
    <div className="col-lg-6 mx-auto">
      <h3>Create New Exam</h3>

      {error && <div className="alert alert-danger">{error}</div>}

      {/* Course Code */}
      <label className="form-label mt-2" htmlFor="courseCode">
        Course Code
      </label>
      <input
        id="courseCode"
        className="form-control"
        value={courseCode}
        onChange={(e) => setCourseCode(e.target.value)}
      />

      {/* Instructor Email */}
      <label className="form-label mt-2" htmlFor="instructorEmail">
        Instructor Email
      </label>
      <input
        id="instructorEmail"
        className="form-control"
        value={instructorEmail}
        onChange={(e) => setInstructorEmail(e.target.value)}
      />

      <button onClick={handleCreate} className="btn btn-primary mt-3">
        Create Exam
      </button>
    </div>
  );
}

export default ExamSetup;
