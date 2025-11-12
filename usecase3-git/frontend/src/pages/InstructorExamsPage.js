import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

export default function InstructorExamsPage() {
  const [exams, setExams] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5003/api/instructors/1/exams")
      .then(r => r.json()).then(d => setExams(d.exams || []));
  }, []);

  return (
    <>
      <h2>My Exams</h2>
      <ul className="list-group">
        {exams.map(e => (
          <li key={e.exam_id} className="list-group-item d-flex justify-content-between">
            <span>{e.title}</span>
            <Link className="btn btn-sm btn-outline-primary" to={`/edit/${e.exam_id}`}>Edit</Link>
          </li>
        ))}
      </ul>
    </>
  );
}
