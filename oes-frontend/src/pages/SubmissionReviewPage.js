import React, { useEffect, useState } from "react";
import axios from "axios";
import { useParams, Link } from "react-router-dom";

function SubmissionReviewPage() {
  const { submissionId } = useParams();
  const [instructorEmail, setInstructorEmail] = useState("teacher@uni.com");
  const [submission, setSubmission] = useState(null);
  const [answers, setAnswers] = useState([]);
  const [totalScore, setTotalScore] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [overallFeedback, setOverallFeedback] = useState("");

  async function openSubmission() {
    setError("");
    setLoading(true);
    try {
      const res = await axios.post(
        `http://localhost:5000/grading/submissions/${submissionId}/open`,
        { instructor_email: instructorEmail }
      );
      setSubmission(res.data);
      setAnswers(res.data.answers || []);
      setTotalScore(res.data.total_score || res.data.totalScore || null);
      setOverallFeedback(res.data.feedback || "");
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.error || "Failed to open submission for review"
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    openSubmission();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function handleToggleVerdict(questionId, forceCorrect) {
    try {
      const res = await axios.post(
        `http://localhost:5000/grading/submissions/${submissionId}/answers/${questionId}/toggle-verdict`,
        { force_correct: forceCorrect }
      );
      const updatedFinal = res.data.final_points;
      const updatedTotal = res.data.total_score;

      setAnswers((prev) =>
        prev.map((a) =>
          a.question_id === questionId
            ? { ...a, manual_points: updatedFinal, final_points: updatedFinal }
            : a
        )
      );
      setTotalScore(updatedTotal);
    } catch (err) {
      console.error(err);
      alert("Failed to toggle verdict");
    }
  }

  async function handlePartialPoints(questionId, currentPoints) {
    const input = window.prompt(
      "Enter manual points:",
      currentPoints != null ? currentPoints : 0
    );
    if (input === null) return;

    const value = parseFloat(input);
    if (Number.isNaN(value)) {
      alert("Invalid number");
      return;
    }

    try {
      const res = await axios.post(
        `http://localhost:5000/grading/submissions/${submissionId}/answers/${questionId}/manual-points`,
        { points: value }
      );
      const updatedTotal = res.data.total_score;

      setAnswers((prev) =>
        prev.map((a) =>
          a.question_id === questionId
            ? { ...a, manual_points: value, final_points: value }
            : a
        )
      );
      setTotalScore(updatedTotal);
    } catch (err) {
      console.error(err);
      alert("Failed to set manual points");
    }
  }

  async function handleQuestionFeedback(questionId) {
    const input = window.prompt("Enter feedback for this question:");
    if (!input) return;

    try {
      await axios.post(
        `http://localhost:5000/grading/submissions/${submissionId}/feedback`,
        { comment: input, question_id: questionId }
      );

      setAnswers((prev) =>
        prev.map((a) =>
          a.question_id === questionId
            ? {
                ...a,
                feedback: a.feedback ? a.feedback + "\n" + input : input,
              }
            : a
        )
      );
    } catch (err) {
      console.error(err);
      alert("Failed to add question feedback");
    }
  }

  async function handleOverallFeedbackSave() {
    if (!overallFeedback.trim()) {
      alert("Feedback is empty");
      return;
    }
    try {
      await axios.post(
        `http://localhost:5000/grading/submissions/${submissionId}/feedback`,
        { comment: overallFeedback }
      );
      alert("Overall feedback saved");
    } catch (err) {
      console.error(err);
      alert("Failed to save overall feedback");
    }
  }

  async function handleRecalc() {
    try {
      const res = await axios.post(
        `http://localhost:5000/grading/submissions/${submissionId}/recalc`
      );
      setTotalScore(res.data.total_score);
    } catch (err) {
      console.error(err);
      alert("Failed to recalculate");
    }
  }

  async function handleSave() {
    try {
      const res = await axios.post(
        `http://localhost:5000/grading/submissions/${submissionId}/save`
      );
      setTotalScore(res.data.total_score);
      alert("Submission graded and saved");
    } catch (err) {
      console.error(err);
      alert("Failed to save grading");
    }
  }

  async function handleCancel() {
    if (!window.confirm("Cancel review and revert status?")) return;
    try {
      await axios.post(
        `http://localhost:5000/grading/submissions/${submissionId}/cancel`
      );
      alert("Review canceled");
    } catch (err) {
      console.error(err);
      alert("Failed to cancel review");
    }
  }

  if (loading) return <p>Loading submission...</p>;

  if (error)
    return (
      <div>
        <div className="alert alert-danger mt-3">{error}</div>
        <button className="btn btn-secondary mt-2" onClick={openSubmission}>
          Retry
        </button>
      </div>
    );

  return (
    <div>
      <h3>Review Submission #{submissionId}</h3>

      <div className="mt-2">
        <label className="form-label">Instructor Email (for backend check)</label>
        <input
          className="form-control"
          value={instructorEmail}
          onChange={(e) => setInstructorEmail(e.target.value)}
        />
        <button className="btn btn-secondary btn-sm mt-2" onClick={openSubmission}>
          Reload with this email
        </button>
      </div>

      {submission && (
        <div className="mt-3">
          <p>
            <strong>Exam ID:</strong> {submission.exam_id} |{" "}
            <strong>Roll:</strong> {submission.roll_number}
          </p>
          <p>
            <strong>Status:</strong> {submission.status} |{" "}
            <strong>Total Score:</strong>{" "}
            {totalScore != null ? totalScore : submission.total_score}
          </p>
        </div>
      )}

      <h5 className="mt-4">Answers</h5>
      <div className="list-group mt-2">
        {answers.map((ans) => (
          <div key={ans.question_id} className="list-group-item">
            <div className="d-flex justify-content-between">
              <div>
                <strong>Question #{ans.question_id}</strong>
                <div className="mt-1">
                  <span className="fw-semibold">Answer: </span>
                  {ans.answer_text || "(no stored text)"}
                </div>
                <div className="mt-1 small text-muted">
                  Auto: {ans.auto_points ?? 0} | Manual: {ans.manual_points ?? 0} | Final:{" "}
                  {ans.final_points ?? 0}
                </div>
                {ans.feedback && (
                  <div className="mt-1">
                    <span className="fw-semibold">Feedback:</span>
                    <pre className="mb-0 small">{ans.feedback}</pre>
                  </div>
                )}
              </div>

              <div className="text-end">
                <button
                  className="btn btn-sm btn-success mb-1"
                  onClick={() => handleToggleVerdict(ans.question_id, true)}
                >
                  Mark Correct
                </button>
                <br />
                <button
                  className="btn btn-sm btn-outline-danger mb-1"
                  onClick={() => handleToggleVerdict(ans.question_id, false)}
                >
                  Mark Wrong
                </button>
                <br />
                <button
                  className="btn btn-sm btn-outline-primary mb-1"
                  onClick={() =>
                    handlePartialPoints(
                      ans.question_id,
                      ans.manual_points ?? ans.final_points ?? ans.auto_points ?? 0
                    )
                  }
                >
                  Set Partial Points
                </button>
                <br />
                <button
                  className="btn btn-sm btn-outline-secondary"
                  onClick={() => handleQuestionFeedback(ans.question_id)}
                >
                  Add Feedback
                </button>
              </div>
            </div>
          </div>
        ))}
        {answers.length === 0 && (
          <div className="list-group-item text-center">No answers stored.</div>
        )}
      </div>

      <h5 className="mt-4">Overall Feedback</h5>
      <textarea
        className="form-control"
        rows={3}
        value={overallFeedback}
        onChange={(e) => setOverallFeedback(e.target.value)}
      />
      <button
        className="btn btn-outline-primary mt-2"
        onClick={handleOverallFeedbackSave}
      >
        Save Overall Feedback
      </button>

      <div className="mt-4 d-flex gap-2">
        <button className="btn btn-secondary" onClick={handleRecalc}>
          Recalculate Total
        </button>
        <button className="btn btn-primary" onClick={handleSave}>
          Save & Mark as GRADED
        </button>
        <button className="btn btn-outline-danger" onClick={handleCancel}>
          Cancel Review
        </button>
      </div>

      <Link className="btn btn-link mt-3" to={`/instructor/grading/exams/${submission?.exam_id}/submissions`}>
        ← Back to submissions list
      </Link>
    </div>
  );
}

export default SubmissionReviewPage;
