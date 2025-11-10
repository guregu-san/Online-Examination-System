CREATE TABLE instructors (
    instructor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    password_hash TEXT
);

CREATE TABLE courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_code TEXT,
    course_name TEXT,
    instructor_id INTEGER,
    FOREIGN KEY (instructor_id) REFERENCES instructors(instructor_id)
);

CREATE TABLE exams (
    exam_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER,
    instructor_id INTEGER,
    title TEXT,
    time_limit INTEGER,
    security_settings TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (instructor_id) REFERENCES instructors(instructor_id)
);

CREATE TABLE questions (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    exam_id INTEGER,
    question_text TEXT,
    question_type TEXT CHECK(question_type IN ('MCQ_SINGLE', 'MCQ_MULTIPLE', 'TRUE_FALSE', 'SHORT_ANSWER', 'NUMERICAL', 'ESSAY')),
    order_index INTEGER,
    FOREIGN KEY (exam_id) REFERENCES exams(exam_id)
);

CREATE TABLE answers (
    answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER,
    answer_text TEXT,
    is_correct BOOLEAN,
    FOREIGN KEY (question_id) REFERENCES questions(question_id)
);
