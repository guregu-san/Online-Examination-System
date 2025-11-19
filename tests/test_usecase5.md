# Test Cases — Use Case 5 (Exam Taking)

## Database Reset

Before running tests, reset and initialize database:

```bash
rm oesDB.db
sqlite3 oesDB.db < sql_scripts/initializeDB.sql
Insert test data:
```
```sql
INSERT INTO instructors (name, email, password_hash)
VALUES ('Teacher One', 'teacher@uni.com', 'pass');

INSERT INTO courses (course_code, course_name, instructor_email)
VALUES ('CS101', 'Example Course', 'teacher@uni.com');

INSERT INTO students (roll_number, name, email, password_hash, contact_number)
VALUES (1, 'Student One', 'student@uni.com', 'pass', 1234567890);

INSERT INTO exams (course_code, instructor_email, title, time_limit, security_settings)
VALUES ('CS101', 'teacher@uni.com', 'Midterm Exam', 60, 'shuffle=true');

INSERT INTO questions (exam_id, question_text, is_multiple_correct, points, order_index)
VALUES 
    (1, 'What is 2+2?', 0, 5, 1),
    (1, 'Select prime numbers', 1, 10, 2);


INSERT INTO options (question_id, option_text, is_correct)
VALUES 
    (1, '3', 0),
    (1, '4', 1),
    (2, '2', 1),
    (2, '3', 1),
    (2, '4', 0);
```

## USE CASE 5 — EXAM TAKING TEST CASES
### Test Case 1 — Start Exam Attempt (U5-F1)
```bash

curl -X POST http://127.0.0.1:5001/submissions/start \
  -H "Content-Type: application/json" \
  -d '{"exam_id": 1, "roll_number": 1}'
```

### Test Case 2 — Load Exam Content (U5-F2)
```bash

curl http://127.0.0.1:5001/submissions/1
```

### Test Case 3 — Save Student Answer (U5-F3)
#### Example: student selects “4” for Q1.
```bash
curl -X POST http://127.0.0.1:5001/submissions/1/answer \
  -H "Content-Type: application/json" \
  -d '{
        "question_id": 1,
        "selected_options": [2]
      }'
```     

### Test Case 4 — Save Answer for Multi-Select Question (U5-F3)
```bash
curl -X POST http://127.0.0.1:5001/submissions/1/answer \
  -H "Content-Type: application/json" \
  -d '{
        "question_id": 2,
        "selected_options": [3, 4]
      }'
```

### Test Case 5 — Submit Exam (U5-F4)
```bash

curl -X POST http://127.0.0.1:5001/submissions/1/submit
```

### Test Case 6 — Cannot Answer After Submit (Negative Test)
```bash
curl -X POST http://127.0.0.1:5001/submissions/1/answer \
  -H "Content-Type: application/json" \
  -d '{"question_id": 1, "selected_options": [2]}'
```

### Test Case 7 — Attempting Exam Twice (Negative Test)
```bash
curl -X POST http://127.0.0.1:5001/submissions/start \
  -H "Content-Type: application/json" \
  -d '{"exam_id": 1, "roll_number": 1}'
```

### Test Case 8 — Load Results After Submission (U5-F5)
```bash
curl http://127.0.0.1:5001/submissions/1/result
```

### Test Case 9 — Invalid Question ID (Negative Test)
```bash
curl -X POST http://127.0.0.1:5001/submissions/1/answer \
  -H "Content-Type: application/json" \
  -d '{"question_id": 999, "selected_options": [1]}'
```

### Test Case 10 — Invalid Exam ID (Negative Test)
```bash

curl -X POST http://127.0.0.1:5001/submissions/start \
  -H "Content-Type: application/json" \
  -d '{"exam_id": 999, "roll_number": 1}'
```

### Test Case 11 — Invalid Student ID (Negative Test)
```bash
curl -X POST http://127.0.0.1:5001/submissions/start \
  -H "Content-Type: application/json" \
  -d '{"exam_id": 1, "roll_number": 999}'
```