# Test Cases — Use Case 5 (Exam Taking)

## Test Case 1 — Search for Exam (U5-F1)
```bash
# Search for exam by ID (stores exam_id in session cookie)
curl -X POST http://127.0.0.1:5001/take_exam \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'examID=1' \
  -c cookies.txt
```

## Test Case 2 — View Exam Initialization
```bash
# GET exam info before starting (requires session from Test Case 1)
curl -X GET http://127.0.0.1:5001/take_exam/exam_initialization \
  -b cookies.txt
```

## Test Case 3 — Start Exam and Load Questions
```bash
# POST to start exam; returns submission form with questions (uses exam_id from session)
curl -X POST http://127.0.0.1:5001/take_exam/start \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -b cookies.txt \
  -d 'questions-0-question_id=1&questions-0-single_or_multi=single&questions-0-answer_single=11&questions-1-question_id=2&questions-1-single_or_multi=multi&questions-1-answer_multi=20&questions-1-answer_multi=21&csrf_token=<token>'
```

## Test Case 4 — Submit Exam with Single-Choice Answer
```bash
# Submit answers: Q1 (single-choice) = option 11, Q2 (multi-choice) = options [20, 21]
curl -X POST http://127.0.0.1:5001/take_exam/start \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -b cookies.txt \
  -d 'roll_number=1&questions-0-question_id=1&questions-0-single_or_multi=single&questions-0-answer_single=11&questions-1-question_id=2&questions-1-single_or_multi=multi&questions-1-answer_multi=20&questions-1-answer_multi=21&csrf_token=<token>'
```

## Test Case 5 — Invalid Exam Search (Negative Test)
```bash
# Searching for non-existent exam should show validation error
curl -X POST http://127.0.0.1:5001/take_exam \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'examID=999' \
  -c cookies.txt
```

## Test Case 6 — Missing Session for Initialization (Negative Test)
```bash
# Trying to access exam_initialization without session should redirect to exam search
curl -X GET http://127.0.0.1:5001/take_exam/exam_initialization \
  -c cookies.txt
```

## Test Case 7 — Missing Session for Start (Negative Test)
```bash
# Trying to start exam without session should redirect to exam search
curl -X POST http://127.0.0.1:5001/take_exam/start \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'roll_number=1' \
  -c cookies.txt
```