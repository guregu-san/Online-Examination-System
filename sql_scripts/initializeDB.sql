CREATE TABLE IF NOT EXISTS instructors (
    instructor_id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE IF NOT EXISTS students (
    roll_number INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT UNIQUE,
    password_hash TEXT,
    contact_number INTEGER
);

CREATE TABLE IF NOT EXISTS courses (
    course_code TEXT PRIMARY KEY,
    course_name TEXT NOT NULL,
    instructor_email TEXT NOT NULL,
    FOREIGN KEY (instructor_email) REFERENCES instructors(email)
);

CREATE TABLE IF NOT EXISTS exams (
    exam_id INTEGER PRIMARY KEY,
    course_code INTEGER,
    instructor_email TEXT,
    title TEXT,
    time_limit INTEGER,
    security_settings TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_code) REFERENCES courses(course_code),
    FOREIGN KEY (instructor_email) REFERENCES instructors(email)
);

CREATE TABLE IF NOT EXISTS questions (
    question_id INTEGER PRIMARY KEY,
    exam_id INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    is_multiple_correct BOOLEAN NOT NULL,
    points INTEGER NOT NULL,
    order_index INTEGER NOT NULL,
    FOREIGN KEY (exam_id) REFERENCES exams(exam_id)
);

CREATE TABLE IF NOT EXISTS options (
    option_id INTEGER PRIMARY KEY,
    question_id INTEGER NOT NULL,
    option_text TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL,
    FOREIGN KEY (question_id) REFERENCES questions(question_id)
);

CREATE TABLE IF NOT EXISTS submissions (
    submission_id INTEGER PRIMARY KEY,
    exam_id INTEGER NOT NULL,
    roll_number TEXT NOT NULL,
    started_at DATETIME,
    submitted_at DATETIME,
    updated_at DATETIME,
    feedback TEXT,
    status TEXT CHECK (status IN ('IN_PROGRESS', 'SUBMITTED', 'IN_REVIEW', 'GRADED')),
    answers TEXT,
    total_score INTEGER,
    FOREIGN KEY (exam_id) REFERENCES exams (exam_id),
    FOREIGN KEY (roll_number) REFERENCES students (roll_number)
);