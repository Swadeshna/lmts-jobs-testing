import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'portal.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Jobs Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        company_logo TEXT,
        location TEXT NOT NULL,
        job_type TEXT NOT NULL,
        experience TEXT NOT NULL,
        salary TEXT NOT NULL,
        skills TEXT NOT NULL,
        tags TEXT NOT NULL,
        description TEXT NOT NULL,
        requirements TEXT NOT NULL,
        eligibility TEXT NOT NULL,
        posted_date TEXT NOT NULL,
        deadline TEXT,
        apply_url TEXT
    )
    ''')

    # Applications Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id INTEGER NOT NULL,
        job_title TEXT NOT NULL,
        company_name TEXT NOT NULL,
        applicant_name TEXT NOT NULL,
        applicant_email TEXT NOT NULL,
        phone TEXT,
        resume_link TEXT,
        experience_level TEXT,
        portfolio_url TEXT,
        cover_note TEXT,
        status TEXT DEFAULT 'Applied',
        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (job_id) REFERENCES jobs(id)
    )
    ''')

    # Bookmarks Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookmarks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id INTEGER UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (job_id) REFERENCES jobs(id)
    )
    ''')

    # Companies Hiring Process Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        slug TEXT UNIQUE NOT NULL,
        logo TEXT,
        category TEXT NOT NULL,
        tier TEXT NOT NULL,
        description TEXT NOT NULL,
        package_range TEXT NOT NULL,
        eligibility_cgpa TEXT NOT NULL,
        eligibility_branches TEXT NOT NULL,
        eligibility_batch TEXT NOT NULL,
        exam_pattern TEXT NOT NULL,
        rounds_breakdown TEXT NOT NULL,
        syllabus TEXT NOT NULL,
        interview_tips TEXT NOT NULL,
        frequently_asked TEXT NOT NULL
    )
    ''')

    # Prep Material Table (Aptitude, DSA, Technical, HR)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS prep_materials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        subcategory TEXT NOT NULL,
        title TEXT NOT NULL,
        summary TEXT NOT NULL,
        read_time TEXT NOT NULL,
        content_markdown TEXT NOT NULL,
        key_takeaways TEXT NOT NULL
    )
    ''')

    # Practice Questions / MCQs
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS prep_questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        subcategory TEXT NOT NULL,
        question TEXT NOT NULL,
        options TEXT NOT NULL,
        correct_index INTEGER NOT NULL,
        explanation TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        company_tags TEXT NOT NULL
    )
    ''')

    # DSA Topics Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dsa_topics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        slug TEXT UNIQUE NOT NULL,
        icon TEXT NOT NULL,
        description TEXT,
        order_idx INTEGER DEFAULT 0
    )
    ''')

    # DSA Problems Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dsa_problems (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        problem_statement TEXT NOT NULL,
        constraints TEXT,
        examples TEXT,
        optimal_complexity TEXT NOT NULL,
        solution_code TEXT NOT NULL,
        leetcode_url TEXT,
        gfg_url TEXT,
        company_tags TEXT NOT NULL,
        FOREIGN KEY (topic_id) REFERENCES dsa_topics(id)
    )
    ''')

    # User DSA Progress Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_dsa_progress (
        problem_id INTEGER PRIMARY KEY,
        status TEXT DEFAULT 'unsolved',
        is_starred INTEGER DEFAULT 0,
        user_notes TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (problem_id) REFERENCES dsa_problems(id)
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")
