# Use Case 4 — Manual Grading  
# Test Cases


INSERT INTO instructors (id, name, email, password_hash)
VALUES (1, 'Teacher One', 'teacher@uni.com', 'pass');

INSERT INTO students (id, name, student_id, email)
VALUES (1, 'Andreas Andreou', 'CSE2023001', 'andreas@student.uni.com');

INSERT INTO exams (id, course_code, title, instructor_id, time_limit, total_points)
VALUES (1, 'CS410', 'CSE410 Midterm', 1, 90, 10);

INSERT INTO questions (id, exam_id, order_index, question_text, max_points)
VALUES (1, 1, 1, 'What is TCP used for?', 2);

INSERT INTO submissions (id, exam_id, student_id, submitted_at, status, auto_score, manual_score, final_score, locked_by, locked_at)
VALUES (2001, 1, 1, '2025-01-01 10:00:00', 'SUBMITTED', 0, NULL, 0, NULL, NULL);

INSERT INTO submission_answers (id, submission_id, question_id, answer_text, auto_points, manual_points, final_points, manual_override)
VALUES (3105, 2001, 1, 'Some answer', 0, 0, 0, 0);
```

---

## Test Case 1 — Load Manual Grading Dashboard (U4-F1)
**Loads grading dashboard for instructor **1**.

```bash
curl -X GET "http://127.0.0.1:5001/grading/dashboard?user_id=1"
```

---

## Test case 2 — List Submissions for Exam (U4-F2)  
Lists all submissions for **exam 1**.

```bash
curl -X GET "http://127.0.0.1:5001/grading/exams/1/submissions"
```

---

## Test case 3 — Open Submission for Review (U4-F3)  
Opens submission **2001** and locks it for instructor **1**.

```bash
curl -X POST "http://127.0.0.1:5001/grading/submissions/2001/open" \
  -H "Content-Type: application/json" \
  -d '{"instructor_id": 1}'
```

---

## Test case 4 — Toggle Verdict to Correct (U4-F4)  
Forces the answer to be marked **Correct**.

```bash
curl -X POST "http://127.0.0.1:5001/grading/answers/3105/toggle-verdict" \
  -H "Content-Type: application/json" \
  -d '{"force_correct": true}'
```

---

## Test case 5 — Set Partial Manual Points (U4-F5)
Sets **1.5/2** points manually.

```bash
curl -X POST "http://127.0.0.1:5001/grading/answers/3105/manual-points" \
  -H "Content-Type: application/json" \
  -d '{"points": 1.5}'
```

---

## Test case 6 — Add Instructor Feedback (U4-F6)**  
Adds comment for question **1**.

```bash
curl -X POST "http://127.0.0.1:5001/grading/submissions/2001/feedback" \
  -H "Content-Type: application/json" \
  -d '{
        "instructor_id": 1,
        "comment": "Good reasoning, missing formula.",
        "question_id": 1
      }'
```

---

## Test case 7 — Recalculate Submission Totals (U4-F7) 
Recalculates auto + manual + final score.

```bash
curl -X POST "http://127.0.0.1:5001/grading/submissions/2001/recalc"
```

---

## Test case 8 — Save Submission Review (U4-F8)  
Finalizes the grading and releases lock.

```bash
curl -X POST "http://127.0.0.1:5001/grading/submissions/2001/save" \
  -H "Content-Type: application/json" \
  -d '{"instructor_id": 1}'
```

---

## Test case 9 — Cancel Review (U4-F9) 
Cancels session and discards edits.

```bash
curl -X POST "http://127.0.0.1:5001/grading/submissions/2001/cancel" \
  -H "Content-Type: application/json" \
  -d '{"instructor_id": 1}'
```

---

## Test case 10 — Verify Submission Integrity (U4-F10) 
IT 10Support tool—checks & repairs data inconsistencies.

```bash
curl -X POST "http://127.0.0.1:5001/grading/admin/submissions/2001/verify-integrity"
```

---

