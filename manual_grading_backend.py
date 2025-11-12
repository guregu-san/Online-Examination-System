import sqlite3
from typing import List, Dict, Optional


#U4-F1 Loads exams with submission counts so instructor can choose which to grade
#loadGradingDashboard(user_id)
def loadManualGradingDashboard(conn, instructor_email):
    """
      Manual Grading Dashboard

    This function:
    - Finds all exams that belong to a specific instructor (by email).
    - For each exam, counts:
        * total submissions
        * submissions with status = 'IN_REVIEW'
        * submissions with status = 'GRADED'
    - Returns a list of dictionaries, one per exam.
    """

    cur = conn.cursor()

    # exams created by the instructor
    cur.execute("""
        SELECT exam_id, title
        FROM exams
        WHERE instructor_email = ?
        ORDER BY created_at DESC
    """, (instructor_email,))

    exams = []

    # 2. For each exam, compute submission counters
    for exam_id, title in cur.fetchall():
        # Count total submissions for this exam
        cur.execute("""
            SELECT
                COUNT(*) AS total,
                SUM(CASE WHEN status = 'IN_REVIEW' THEN 1 ELSE 0 END) AS in_review,
                SUM(CASE WHEN status = 'GRADED'    THEN 1 ELSE 0 END) AS graded
            FROM submissions
            WHERE exam_id = ?
        """, (exam_id,))

        row = cur.fetchone()

        
        total_submissions = row[0] or 0
        in_review         = row[1] or 0
        graded            = row[2] or 0

      
        exams.append({
            "exam_id": exam_id,
            "title": title,
            "total_submissions": total_submissions,
            "in_review": in_review,
            "graded": graded
        })

    #This list as JSON can be send to the front end
    return exams


#U4-F2 listSubmissions(exam_id, filters)
#Displays all submitted exams with student names and grading status
def listSubmissions(conn, exam_id):
    """
     List Submissions for Selected Exam

    This function:
    - Retrieves all submissions for a given exam.
    - Joins with the students table to show student name and roll number.
    - Returns a list of dictionaries, one per submission, ordered by submitted_at.
    """

    cur = conn.cursor()

    # Join submissions with students to show who submitted each attempt
    cur.execute("""
        SELECT
            s.submission_id,
            st.roll_number,
            st.name,
            s.submitted_at,
            s.total_score,
            s.status
        FROM submissions s
        JOIN students st ON st.roll_number = s.roll_number
        WHERE s.exam_id = ?
        ORDER BY s.submitted_at ASC
    """, (exam_id,))

    submissions = []

    
    for submission_id, roll_number, name, submitted_at, total_score, status in cur.fetchall():
        submissions.append({
            "submission_id": submission_id,
            "roll_number": roll_number,
            "student_name": name,
            "submitted_at": submitted_at,
            "total_score": total_score,
            "status": status
        })

    return submissions
