# Use Case 4 — Manual Grading  
-- Instructors
INSERT INTO instructors (instructor_id, name, email, password_hash)
VALUES (1, 'Teacher One', 'teacher@uni.com', 'pass');

-- Students
INSERT INTO students (roll_number, name, email)
VALUES ('CSE2023001', 'Andreas Andreou', 'andreas@student.uni.com');

-- Course
INSERT INTO courses (course_code, course_name, instructor_email)
VALUES ('CS410', 'Networking Fundamentals', 'teacher@uni.com');

-- Exam
INSERT INTO exams (exam_id, course_code, title, instructor_email, time_limit)
VALUES (1, 'CS410', 'CSE410 Midterm', 'teacher@uni.com', 90);

-- Question
INSERT INTO questions (question_id, exam_id, order_index, question_text, points, is_multiple_correct)
VALUES (1, 1, 1, 'What is TCP used for?', 2, 0);

-- Submission
INSERT INTO submissions (
    submission_id,
    exam_id,
    roll_number,
    submitted_at,
    status,
    answers,
    total_score
)
VALUES (
    2001,
    1,
    'CSE2023001',
    '2025-01-01 10:00:00',
    'SUBMITTED',
    '[]',
    0
);
```

---

#Test Case 1 — Load Manual Grading Dashboard (U4-F1)

```bash
curl -X GET "http://127.0.0.1:5000/grading/dashboard/teacher@uni.com"
```

---

#Test Case 2 — List Submissions for Exam (U4-F2)

```bash
curl -X GET "http://127.0.0.1:5000/grading/exams/1/submissions"
```

---

#Test Case 3 — Open Submission for Review (U4-F3)

```bash
curl -X POST "http://127.0.0.1:5000/grading/submissions/2001/open" \
  -H "Content-Type: application/json" \
  -d '{"instructor_email": "teacher@uni.com"}'
```

---

#Test Case 4 — Toggle Verdict to Correct (U4-F4)

```bash
curl -X POST \
 "http://127.0.0.1:5000/grading/submissions/2001/answers/1/toggle-verdict" \
 -H "Content-Type: application/json" \
 -d '{"force_correct": true}'
```

---

#Test Case 5 — Set Partial Manual Points (U4-F5)

```bash
curl -X POST \
 "http://127.0.0.1:5000/grading/submissions/2001/answers/1/manual-points" \
 -H "Content-Type: application/json" \
 -d '{"points": 1.5}'
```

---

#Test Case 6 — Add Instructor Feedback (U4-F6)

```bash
curl -X POST "http://127.0.0.1:5000/grading/submissions/2001/feedback" \
  -H "Content-Type: application/json" \
  -d '{
        "comment": "Good reasoning, missing formula.",
        "question_id": 1
      }'
```

---

#Test Case 7 — Recalculate Submission Total Score (U4-F7)

```bash
curl -X POST "http://127.0.0.1:5000/grading/submissions/2001/recalc"
```

---

#Test Case 8 — Save Submission Review (U4-F8)

```bash
curl -X POST "http://127.0.0.1:5000/grading/submissions/2001/save"
```

---

#Test Case 9 — Cancel Review (U4-F9)

```bash
curl -X POST "http://127.0.0.1:5000/grading/submissions/2001/cancel"
```

---

#Test Case 10 — Verify Submission Integrity (U4-F10)

```bash
curl -X POST \
 "http://127.0.0.1:5000/grading/admin/submissions/2001/verify-integrity"
```

---
