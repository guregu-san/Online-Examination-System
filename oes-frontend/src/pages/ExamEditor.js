import React, { useEffect, useState, useRef } from "react";
import axios from "axios";
import { useParams, useNavigate } from "react-router-dom";

function ExamEditor() {
  const { examId } = useParams();
  const navigate = useNavigate();

  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);

  // Modal state
  const [showModal, setShowModal] = useState(false);
  const [editingQuestion, setEditingQuestion] = useState(null);

  const [qText, setQText] = useState("");
  const [qOptions, setQOptions] = useState([{ text: "", isCorrect: false }]);

  const dragItem = useRef(null);
  const dragOverItem = useRef(null);

  // ❗ Fetch questions (requires backend support)
  useEffect(() => {
    async function load() {
      try {
        const res = await axios.get(`http://localhost:5000/exam/${examId}/full`);
        setQuestions(res.data.questions || []);
      } catch (err) {
        console.error("Failed to load exam:", err);
      }
      setLoading(false);
    }
    load();
  }, [examId]);

  function openAddModal() {
    setEditingQuestion(null);
    setQText("");
    setQOptions([{ text: "", isCorrect: false }]);
    setShowModal(true);
  }

  function addOption() {
    setQOptions([...qOptions, { text: "", isCorrect: false }]);
  }

  async function saveQuestion() {
    if (!qText.trim()) return alert("Question text required");

    const formatted = qOptions.map(o => ({
      option_text: o.text,
      is_correct: o.isCorrect
    }));

    try {
      if (editingQuestion === null) {
        // Create question
        await axios.post(`http://localhost:5000/exams/${examId}/questions`, {
          question_text: qText,
          is_multiple_correct: true,
          points: 1,
          options: formatted
        });
      } else {
        // Edit existing question
        await axios.patch(
          `http://localhost:5000/exams/questions/${editingQuestion.question_id}`,
          {
            question_text: qText,
            options: formatted
          }
        );
      }

      window.location.reload();
    } catch (e) {
      console.error(e);
      alert("Failed to save question");
    }
  }

  async function deleteQ(id) {
    if (!window.confirm("Delete this question?")) return;
    try {
      await axios.delete(`http://localhost:5000/exams/questions/${id}`);
      setQuestions(questions.filter(q => q.question_id !== id));
    } catch (e) {
      console.error(e);
    }
  }

  // Drag and drop reorder
  async function handleDrop() {
    const updated = [...questions];
    const dragged = updated[dragItem.current];
    updated.splice(dragItem.current, 1);
    updated.splice(dragOverItem.current, 0, dragged);

    setQuestions(updated);

    await axios.post(`http://localhost:5000/exams/${examId}/reorder`, {
      order: updated.map((q, index) => ({
        question_id: q.question_id,
        order_index: index + 1
      }))
    });
  }

  if (loading) return <p>Loading exam...</p>;

  return (
    <div>
      <h3>Edit Exam #{examId}</h3>

      <button className="btn btn-primary mt-3" onClick={openAddModal}>
        + Add Question
      </button>

      <ul className="list-group mt-4">
        {questions.map((q, index) => (
          <li
            className="list-group-item d-flex justify-content-between"
            key={q.question_id}
            draggable
            onDragStart={() => (dragItem.current = index)}
            onDragEnter={() => (dragOverItem.current = index)}
            onDragEnd={handleDrop}
            onDragOver={e => e.preventDefault()}
          >
            <span>{q.question_text}</span>

            <div>
              <button
                className="btn btn-sm btn-outline-primary me-2"
                onClick={() => {
                  setEditingQuestion(q);
                  setQText(q.question_text);
                  setQOptions(
                    q.options.map(o => ({
                      text: o.option_text,
                      isCorrect: o.is_correct === 1
                    }))
                  );
                  setShowModal(true);
                }}
              >
                Edit
              </button>

              <button
                className="btn btn-sm btn-outline-danger"
                onClick={() => deleteQ(q.question_id)}
              >
                Delete
              </button>
            </div>
          </li>
        ))}
      </ul>

      {/* MODAL */}
      {showModal && (
        <div className="modal d-block" style={{ background: "rgba(0,0,0,0.5)" }}>
          <div className="modal-dialog modal-lg mt-5">
            <div className="modal-content p-3">
              <h5>{editingQuestion ? "Edit Question" : "Add Question"}</h5>

              <label className="mt-2" htmlFor="questionText">Question Text</label>
              <textarea
                id="questionText"
                className="form-control"
                value={qText}
                onChange={e => setQText(e.target.value)}
              />

              <label className="mt-3">Options</label>
              {qOptions.map((opt, i) => (
                <div className="input-group mb-2" key={i}>
                  <span className="input-group-text">
                    <input
                      type="checkbox"
                      checked={opt.isCorrect}
                      onChange={() => {
                        const copy = [...qOptions];
                        copy[i].isCorrect = !copy[i].isCorrect;
                        setQOptions(copy);
                      }}
                    />
                  </span>

                  <input
                    className="form-control"
                    value={opt.text}
                    onChange={e => {
                      const copy = [...qOptions];
                      copy[i].text = e.target.value;
                      setQOptions(copy);
                    }}
                  />
                </div>
              ))}

              <button className="btn btn-secondary mt-1" onClick={addOption}>
                + Add Option
              </button>

              <div className="d-flex justify-content-end mt-3">
                <button
                  className="btn btn-secondary me-2"
                  onClick={() => setShowModal(false)}
                >
                  Cancel
                </button>
                <button className="btn btn-primary" onClick={saveQuestion}>
                  Save Question
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default ExamEditor;
