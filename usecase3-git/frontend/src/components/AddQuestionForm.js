import { useState } from "react";
import { addQuestion } from "../api";

export default function AddQuestionForm({ examId, onAdded }) {
  const [questionText, setQuestionText] = useState("");
  const [questionType, setQuestionType] = useState("MCQ_SINGLE");
  const [answers, setAnswers] = useState([{ answer_text: "", is_correct: false }]);

  const handleAddAnswer = () => setAnswers([...answers, { answer_text: "", is_correct: false }]);
  const handleAnswerChange = (i, field, value) => {
    const updated = [...answers];
    updated[i][field] = value;
    setAnswers(updated);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = { exam_id: examId, question_text: questionText, question_type: questionType, answers };
    await addQuestion(payload);
    setQuestionText("");
    setAnswers([{ answer_text: "", is_correct: false }]);
    if (onAdded) onAdded();
  };

  return (
    <form onSubmit={handleSubmit} className="mb-4">
      <h5>Add Question</h5>
      <div className="mb-2">
        <label>Question Text</label>
        <textarea className="form-control" value={questionText} onChange={(e) => setQuestionText(e.target.value)} />
      </div>

      <div className="mb-2">
        <label>Type</label>
        <select className="form-select" value={questionType} onChange={(e) => setQuestionType(e.target.value)}>
          <option value="MCQ_SINGLE">MCQ (Single)</option>
          <option value="MCQ_MULTIPLE">MCQ (Multiple)</option>
          <option value="TRUE_FALSE">True / False</option>
          <option value="SHORT_ANSWER">Short Answer</option>
          <option value="NUMERICAL">Numerical</option>
          <option value="ESSAY">Essay</option>
        </select>
      </div>

      {(questionType === "MCQ_SINGLE" || questionType === "MCQ_MULTIPLE" || questionType === "TRUE_FALSE") && (
        <div className="mb-2">
          <label>Answers</label>
          {answers.map((a, i) => (
            <div key={i} className="input-group mb-1">
              <input
                className="form-control"
                placeholder="Answer text"
                value={a.answer_text}
                onChange={(e) => handleAnswerChange(i, "answer_text", e.target.value)}
              />
              <div className="input-group-text">
                <input
                  type="checkbox"
                  checked={a.is_correct}
                  onChange={(e) => handleAnswerChange(i, "is_correct", e.target.checked)}
                />
              </div>
            </div>
          ))}
          <button type="button" className="btn btn-sm btn-secondary" onClick={handleAddAnswer}>
            + Add Option
          </button>
        </div>
      )}

      <button type="submit" className="btn btn-primary mt-2">Add Question</button>
    </form>
  );
}
