import { deleteQuestion } from "../api";

export default function QuestionList({ questions }) {
  if (!questions || questions.length === 0) return <p>No questions yet.</p>;

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this question?")) return;
    await deleteQuestion(id);
    window.location.reload();
  };

  return (
    <div>
      <h5>Questions</h5>
      <ul className="list-group">
        {questions.map((q) => (
          <li key={q.question_id} className="list-group-item d-flex justify-content-between align-items-center">
            <div>
              <strong>{q.question_text}</strong>
              <div className="text-muted small">{q.question_type}</div>
            </div>
            <button className="btn btn-outline-danger btn-sm" onClick={() => handleDelete(q.question_id)}>
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
