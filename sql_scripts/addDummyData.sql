-- Sample data for the Online Examination System (idempotent, no explicit primary keys)
-- Run this after `initializeDB.sql` has created the schema.

PRAGMA foreign_keys = ON;

-- Remove any previous sample exam named 'Sample Exam' and its related data
DELETE FROM submissions WHERE exam_id IN (SELECT exam_id FROM exams WHERE title = 'Sample Exam');
DELETE FROM options WHERE question_id IN (SELECT question_id FROM questions WHERE exam_id IN (SELECT exam_id FROM exams WHERE title = 'Sample Exam'));
DELETE FROM questions WHERE exam_id IN (SELECT exam_id FROM exams WHERE title = 'Sample Exam');
DELETE FROM exams WHERE title = 'Sample Exam';

-- Insert an instructor (do not override other instructors)
INSERT OR IGNORE INTO instructors (name, email, password_hash)
VALUES ('Dr Instructor', 'instructor@example.com', 'hashed_pw');

-- Insert a course
INSERT OR IGNORE INTO courses (course_code, course_name, instructor_email)
VALUES ('CS101', 'Intro to Testing', 'instructor@example.com');

-- Insert the exam (let SQLite assign exam_id automatically)
INSERT INTO exams (course_code, instructor_email, title, time_limit, security_settings)
VALUES ('CS101', 'instructor@example.com', 'Sample Exam', 30, '{}');

-- Insert two questions (auto-assigned question_id)
INSERT INTO questions (exam_id, question_text, is_multiple_correct, points, order_index)
VALUES ((SELECT exam_id FROM exams WHERE title='Sample Exam' LIMIT 1), 'What is 2 + 2?', 0, 5, 1);

INSERT INTO questions (exam_id, question_text, is_multiple_correct, points, order_index)
VALUES ((SELECT exam_id FROM exams WHERE title='Sample Exam' LIMIT 1), 'Select prime numbers', 1, 10, 2);

-- Insert options for the two questions (option_id auto-assigned)
-- For Q1 (single correct)
INSERT INTO options (question_id, option_text, is_correct)
VALUES ((SELECT question_id FROM questions WHERE exam_id=(SELECT exam_id FROM exams WHERE title='Sample Exam') AND order_index=1 LIMIT 1), '3', 0);
INSERT INTO options (question_id, option_text, is_correct)
VALUES ((SELECT question_id FROM questions WHERE exam_id=(SELECT exam_id FROM exams WHERE title='Sample Exam') AND order_index=1 LIMIT 1), '4', 1);
INSERT INTO options (question_id, option_text, is_correct)
VALUES ((SELECT question_id FROM questions WHERE exam_id=(SELECT exam_id FROM exams WHERE title='Sample Exam') AND order_index=1 LIMIT 1), '5', 0);

-- For Q2 (multiple correct)
INSERT INTO options (question_id, option_text, is_correct)
VALUES ((SELECT question_id FROM questions WHERE exam_id=(SELECT exam_id FROM exams WHERE title='Sample Exam') AND order_index=2 LIMIT 1), '2', 1);
INSERT INTO options (question_id, option_text, is_correct)
VALUES ((SELECT question_id FROM questions WHERE exam_id=(SELECT exam_id FROM exams WHERE title='Sample Exam') AND order_index=2 LIMIT 1), '3', 1);
INSERT INTO options (question_id, option_text, is_correct)
VALUES ((SELECT question_id FROM questions WHERE exam_id=(SELECT exam_id FROM exams WHERE title='Sample Exam') AND order_index=2 LIMIT 1), '4', 0);
INSERT INTO options (question_id, option_text, is_correct)
VALUES ((SELECT question_id FROM questions WHERE exam_id=(SELECT exam_id FROM exams WHERE title='Sample Exam') AND order_index=2 LIMIT 1), '6', 0);

-- Insert a student (roll_number is PK; use INSERT OR IGNORE to avoid duplicates)
INSERT OR IGNORE INTO students (roll_number, name, email, password_hash, contact_number)
VALUES (1001, 'Student One', 'student1@example.com', 'hashed_pw', '1234567890');

-- Insert a submission for that student with the correct answers
-- Build answers JSON by looking up the actual generated IDs for questions/options
INSERT INTO submissions (exam_id, roll_number, started_at, submitted_at, status, answers, total_score)
VALUES (
	(SELECT exam_id FROM exams WHERE title='Sample Exam' LIMIT 1),
	1001,
	CURRENT_TIMESTAMP,
	CURRENT_TIMESTAMP,
	'GRADED',
	-- build JSON: { "<q1_id>": <opt_id_for_correct>, "<q2_id>": [<opt_id1>,<opt_id2>] }
	json(
		'{"' || (SELECT question_id FROM questions WHERE exam_id=(SELECT exam_id FROM exams WHERE title='Sample Exam') AND order_index=1 LIMIT 1)
			|| '": ' || (SELECT option_id FROM options WHERE question_id=(SELECT question_id FROM questions WHERE exam_id=(SELECT exam_id FROM exams WHERE title='Sample Exam') AND order_index=1 LIMIT 1) AND is_correct=1 LIMIT 1)
			|| ', "' || (SELECT question_id FROM questions WHERE exam_id=(SELECT exam_id FROM exams WHERE title='Sample Exam') AND order_index=2 LIMIT 1)
			|| '": [' || (SELECT option_id FROM options WHERE question_id=(SELECT question_id FROM questions WHERE exam_id=(SELECT exam_id FROM exams WHERE title='Sample Exam') AND order_index=2 LIMIT 1) AND option_text IN ('2','3') ORDER BY option_id LIMIT 1)
			|| ',' || (SELECT option_id FROM options WHERE question_id=(SELECT question_id FROM questions WHERE exam_id=(SELECT exam_id FROM exams WHERE title='Sample Exam') AND order_index=2 LIMIT 1) AND option_text IN ('2','3') ORDER BY option_id LIMIT 1 OFFSET 1)
			|| ']}'
	),
	-- compute total_score (we know points are 5 and 10 here)
	(
		(SELECT points FROM questions WHERE exam_id=(SELECT exam_id FROM exams WHERE title='Sample Exam') AND order_index=1 LIMIT 1)
		+ (SELECT points FROM questions WHERE exam_id=(SELECT exam_id FROM exams WHERE title='Sample Exam') AND order_index=2 LIMIT 1)
	)
);

-- End of sample data

