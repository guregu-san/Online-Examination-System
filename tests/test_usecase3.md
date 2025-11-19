# Test Cases — Use Case 3 (Exam Management)

## Database Reset

Before running any tests:

```bash
rm oesDB.db
sqlite3 oesDB.db < sql_scripts/initializeDB.sql
Insert base test records:
```

```sql
INSERT INTO instructors (name, email, password_hash)
VALUES ('Teacher One', 'teacher@uni.com', 'pass');

INSERT INTO courses (course_code, course_name, instructor_email)
VALUES ('CS101', 'Example Course', 'teacher@uni.com');
```
###Test Case 1 — Create Exam (U3-F1)

```bash
curl -X POST http://127.0.0.1:5001/exams \
  -H "Content-Type: application/json" \
  -d '{
        "course_code": "CS101",
        "instructor_email": "teacher@uni.com",
        "title": "Midterm Exam",
        "time_limit": 90,
        "security_settings": "shuffle=true"
      }'
```
###Test Case 2 — Add Question (U3-F2)
```bash

curl -X POST http://127.0.0.1:5001/exams/1/questions \
  -H "Content-Type: application/json" \
  -d '{
        "question_text": "What is 2+2?",
        "is_multiple_correct": false,
        "points": 5,
        "options": [
          {"option_text": "3", "is_correct": false},
          {"option_text": "4", "is_correct": true}
        ]
      }'
```

###Test Case 3 — Edit Question (U3-F3)
```bash

curl -X PATCH http://127.0.0.1:5001/exams/questions/1 \
  -H "Content-Type: application/json" \
  -d '{
        "question_text": "What is 3+3?",
        "points": 10,
        "options": [
          {"option_text": "6", "is_correct": true}
        ]
      }'
```
###Test Case 4 — Delete Question (U3-F4)
```bash

curl -X DELETE http://127.0.0.1:5001/exams/questions/1
```
###Test Case 5 — Reorder Questions (U3-F5)
```bash

curl -X POST http://127.0.0.1:5001/exams/1/reorder \
  -H "Content-Type: application/json" \
  -d '{
        "order": [
          {"question_id": 2, "order_index": 1},
          {"question_id": 3, "order_index": 2}
        ]
      }'
```

###Test Case 6 — Update Exam Options (U3-F6)
```bash

curl -X PATCH http://127.0.0.1:5001/exams/1/options \
  -H "Content-Type: application/json" \
  -d '{
        "title": "Midterm v2",
        "time_limit": 100,
        "security_settings": "shuffle=true"
      }'
```
###Test Case 7 — List Exams by Instructor (U3-F7)
```bash

curl http://127.0.0.1:5001/exams/instructor/teacher@uni.com
```
###Test Case 8 — Missing Required Fields (Negative Test)
```bash

curl -X POST http://127.0.0.1:5001/exams \
  -H "Content-Type: application/json" \
  -d '{"instructor_email":"teacher@uni.com"}'
```
###Test Case 9 — Invalid Instructor Email (Negative Test)
```bash

curl -X POST http://127.0.0.1:5001/exams \
  -H "Content-Type: application/json" \
  -d '{
        "course_code": "CS101",
        "instructor_email": "wrong@uni.com",
        "title": "Exam",
        "time_limit": 60
      }'
```