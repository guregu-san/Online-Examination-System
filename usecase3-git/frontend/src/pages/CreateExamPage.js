import { useState, useEffect } from "react";
import { getInstructor, createExam } from "../api";
import { useNavigate } from "react-router-dom";

export default function CreateExamPage() {
  const [email, setEmail] = useState("drsmith@example.com");
  const [course, setCourse] = useState("CS101");
  const [title, setTitle] = useState("Untitled Exam");
  const [status, setStatus] = useState("Checking backend...");
  const navigate = useNavigate();

  useEffect(() => {
    getInstructor(email).then(d => setStatus(d.status === "ok" ? "Backend ready" : "Access denied"));
  }, [email]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = await createExam({ instructor_email: email, course_code: course, title });
    if (data.exam_id) navigate(`/edit/${data.exam_id}`);
    else alert(JSON.stringify(data));
  };

  return (
    <>
      <h2>Create Exam</h2>
      <div className="alert alert-info">Backend: {status}</div>
      <form onSubmit={handleSubmit} className="row g-3">
        <div className="col-md-4">
          <label>Email</label>
          <input className="form-control" value={email} onChange={e=>setEmail(e.target.value)} />
        </div>
        <div className="col-md-3">
          <label>Course</label>
          <input className="form-control" value={course} onChange={e=>setCourse(e.target.value)} />
        </div>
        <div className="col-md-3">
          <label>Title</label>
          <input className="form-control" value={title} onChange={e=>setTitle(e.target.value)} />
        </div>
        <div className="col-md-2 d-flex align-items-end">
          <button className="btn btn-primary w-100">Create</button>
        </div>
      </form>
    </>
  );
}
