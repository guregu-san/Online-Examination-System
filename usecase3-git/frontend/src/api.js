const API = "http://127.0.0.1:5003";

export async function getInstructor(email) {
  return fetch(`${API}/api/instructor/${email}`).then(r => r.json());
}

export async function createExam(data) {
  return fetch(`${API}/api/exams`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(data)
  }).then(r => r.json());
}

export async function getExam(id) {
  return fetch(`${API}/api/exams/${id}/detail`).then(r => r.json());
}

export async function addQuestion(payload) {
  return fetch(`${API}/api/questions`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(payload)
  }).then(r => r.json());
}
// 🗑️ Delete a question
export async function deleteQuestion(question_id) {
    const res = await fetch(`${API}/api/questions/${question_id}`, {
      method: "DELETE",
    });
    return res.json();
  }
  
  // ⚙️ Set exam options (time limit, security settings)
  export async function setExamOptions(exam_id, options) {
    const res = await fetch(`${API}/api/exams/${exam_id}/options`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(options),
    });
    return res.json();
  }
  