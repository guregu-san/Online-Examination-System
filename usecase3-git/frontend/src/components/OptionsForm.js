import { useState } from "react";
import { setExamOptions } from "../api";

export default function OptionsForm({ exam }) {
  const [timeLimit, setTimeLimit] = useState(exam.time_limit || "");
  const [security, setSecurity] = useState(exam.security_settings || "");

  const handleSubmit = async (e) => {
    e.preventDefault();
    await setExamOptions(exam.exam_id, { time_limit: timeLimit, security_settings: security });
    alert("Settings saved!");
  };

  return (
    <form onSubmit={handleSubmit} className="mb-4">
      <h5>Exam Options</h5>
      <div className="row g-2">
        <div className="col-md-4">
          <label>Time Limit (minutes)</label>
          <input className="form-control" value={timeLimit} onChange={(e) => setTimeLimit(e.target.value)} />
        </div>
        <div className="col-md-8">
          <label>Security Settings</label>
          <input className="form-control" value={security} onChange={(e) => setSecurity(e.target.value)} />
        </div>
      </div>
      <button className="btn btn-primary mt-3">Save Options</button>
    </form>
  );
}
