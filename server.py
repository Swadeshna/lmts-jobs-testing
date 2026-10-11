#!/usr/bin/env python3
import http.server
import json
import os
import mimetypes
import urllib.parse
from database import get_connection, init_db

PORT = 8000
STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')

class PortalHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # 1. API ROUTES
        if path.startswith('/api/'):
            conn = get_connection()
            cursor = conn.cursor()

            try:
                # GET /api/jobs
                if path == '/api/jobs':
                    q = query.get('q', [''])[0].strip().lower()
                    job_type = query.get('type', [''])[0].strip()
                    exp = query.get('exp', [''])[0].strip()

                    sql = "SELECT * FROM jobs WHERE 1=1"
                    params = []

                    if q:
                        sql += " AND (LOWER(title) LIKE ? OR LOWER(company) LIKE ? OR LOWER(skills) LIKE ? OR LOWER(location) LIKE ?)"
                        wild = f"%{q}%"
                        params.extend([wild, wild, wild, wild])
                    if job_type:
                        sql += " AND job_type = ?"
                        params.append(job_type)
                    if exp:
                        sql += " AND experience LIKE ?"
                        params.append(f"%{exp}%")

                    sql += " ORDER BY id DESC"
                    cursor.execute(sql, params)
                    rows = cursor.fetchall()
                    jobs = []
                    for r in rows:
                        item = dict(r)
                        item['skills'] = json.loads(item['skills']) if item['skills'] else []
                        item['tags'] = json.loads(item['tags']) if item['tags'] else []
                        jobs.append(item)
                    return self._send_json({"jobs": jobs, "total": len(jobs)})

                # GET /api/jobs/<id>
                elif path.startswith('/api/jobs/'):
                    job_id = path.split('/')[-1]
                    cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
                    row = cursor.fetchone()
                    if row:
                        job = dict(row)
                        job['skills'] = json.loads(job['skills']) if job['skills'] else []
                        job['tags'] = json.loads(job['tags']) if job['tags'] else []
                        return self._send_json(job)
                    return self._send_json({"error": "Job not found"}, 404)

                # GET /api/bookmarks
                elif path == '/api/bookmarks':
                    cursor.execute("SELECT job_id FROM bookmarks")
                    bookmarks = [r['job_id'] for r in cursor.fetchall()]
                    return self._send_json({"bookmarks": bookmarks})

                # GET /api/applications
                elif path == '/api/applications':
                    cursor.execute("SELECT * FROM applications ORDER BY applied_at DESC")
                    apps = [dict(r) for r in cursor.fetchall()]
                    return self._send_json({"applications": apps})

                # GET /api/companies
                elif path == '/api/companies':
                    cursor.execute("SELECT * FROM companies ORDER BY id ASC")
                    companies = []
                    for r in cursor.fetchall():
                        c = dict(r)
                        c['exam_pattern'] = json.loads(c['exam_pattern']) if c['exam_pattern'] else {}
                        c['rounds_breakdown'] = json.loads(c['rounds_breakdown']) if c['rounds_breakdown'] else []
                        c['syllabus'] = json.loads(c['syllabus']) if c['syllabus'] else {}
                        c['frequently_asked'] = json.loads(c['frequently_asked']) if c['frequently_asked'] else []
                        companies.append(c)
                    return self._send_json({"companies": companies})

                # GET /api/prep
                elif path == '/api/prep':
                    category = query.get('category', [''])[0].strip()
                    if category:
                        cursor.execute("SELECT * FROM prep_materials WHERE category = ? ORDER BY id ASC", (category,))
                    else:
                        cursor.execute("SELECT * FROM prep_materials ORDER BY id ASC")
                    items = []
                    for r in cursor.fetchall():
                        item = dict(r)
                        item['key_takeaways'] = json.loads(item['key_takeaways']) if item['key_takeaways'] else []
                        items.append(item)
                    return self._send_json({"materials": items})

                # GET /api/prep/questions
                elif path == '/api/prep/questions':
                    category = query.get('category', [''])[0].strip()
                    if category:
                        cursor.execute("SELECT * FROM prep_questions WHERE category = ? ORDER BY id ASC", (category,))
                    else:
                        cursor.execute("SELECT * FROM prep_questions ORDER BY id ASC")
                    questions = []
                    for r in cursor.fetchall():
                        q = dict(r)
                        q['options'] = json.loads(q['options']) if q['options'] else []
                        q['company_tags'] = json.loads(q['company_tags']) if q['company_tags'] else []
                        questions.append(q)
                    return self._send_json({"questions": questions})

                # GET /api/dsa/topics
                elif path == '/api/dsa/topics':
                    cursor.execute("""
                    SELECT t.*, 
                           COUNT(p.id) as total_problems,
                           SUM(CASE WHEN up.status = 'solved' THEN 1 ELSE 0 END) as solved_count
                    FROM dsa_topics t
                    LEFT JOIN dsa_problems p ON t.id = p.topic_id
                    LEFT JOIN user_dsa_progress up ON p.id = up.problem_id
                    GROUP BY t.id
                    ORDER BY t.order_idx ASC
                    """)
                    topics = [dict(r) for r in cursor.fetchall()]
                    return self._send_json({"topics": topics})

                # GET /api/dsa/problems
                elif path == '/api/dsa/problems':
                    topic_id = query.get('topic_id', [''])[0].strip()
                    sql = """
                    SELECT p.*, t.name as topic_name, t.slug as topic_slug,
                           COALESCE(up.status, 'unsolved') as user_status,
                           COALESCE(up.is_starred, 0) as is_starred,
                           up.user_notes
                    FROM dsa_problems p
                    JOIN dsa_topics t ON p.topic_id = t.id
                    LEFT JOIN user_dsa_progress up ON p.id = up.problem_id
                    WHERE 1=1
                    """
                    params = []
                    if topic_id:
                        sql += " AND p.topic_id = ?"
                        params.append(topic_id)
                    sql += " ORDER BY p.topic_id ASC, p.id ASC"

                    cursor.execute(sql, params)
                    problems = []
                    for r in cursor.fetchall():
                        p = dict(r)
                        p['examples'] = json.loads(p['examples']) if p['examples'] else []
                        p['company_tags'] = json.loads(p['company_tags']) if p['company_tags'] else []
                        problems.append(p)
                    return self._send_json({"problems": problems})

                else:
                    return self._send_json({"error": "Endpoint not found"}, 404)
            finally:
                conn.close()

        # 2. STATIC FILES / SPA FALLBACK
        if path == '/' or not os.path.exists(os.path.join(STATIC_DIR, path.lstrip('/'))):
            self.path = '/index.html'

        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(body) if body else {}

        conn = get_connection()
        cursor = conn.cursor()

        try:
            # POST /api/apply
            if path == '/api/apply':
                job_id = data.get('job_id')
                cursor.execute("SELECT title, company FROM jobs WHERE id = ?", (job_id,))
                job = cursor.fetchone()
                if not job:
                    return self._send_json({"error": "Job not found"}, 404)

                cursor.execute("""
                INSERT INTO applications (
                    job_id, job_title, company_name, applicant_name, applicant_email,
                    phone, resume_link, experience_level, portfolio_url, cover_note
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    job_id,
                    job['title'],
                    job['company'],
                    data.get('name', 'Anonymous Candidate'),
                    data.get('email', ''),
                    data.get('phone', ''),
                    data.get('resume_link', ''),
                    data.get('experience_level', 'Fresher'),
                    data.get('portfolio_url', ''),
                    data.get('cover_note', '')
                ))
                conn.commit()
                app_id = cursor.lastrowid
                return self._send_json({"success": True, "application_id": app_id, "message": "Application submitted successfully!"}, 201)

            # POST /api/jobs (Post a new job)
            elif path == '/api/jobs':
                cursor.execute("""
                INSERT INTO jobs (
                    title, company, company_logo, location, job_type, experience,
                    salary, skills, tags, description, requirements, eligibility, posted_date, deadline, apply_url
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    data.get('title'),
                    data.get('company'),
                    data.get('company_logo', 'https://via.placeholder.com/60'),
                    data.get('location', 'Remote'),
                    data.get('job_type', 'Full-time'),
                    data.get('experience', 'Fresher'),
                    data.get('salary', 'Competitive'),
                    json.dumps(data.get('skills', [])),
                    json.dumps(data.get('tags', ["New Opening"])),
                    data.get('description', ''),
                    data.get('requirements', ''),
                    data.get('eligibility', ''),
                    data.get('posted_date', 'Today'),
                    data.get('deadline', '30 Days'),
                    data.get('apply_url', '')
                ))
                conn.commit()
                new_id = cursor.lastrowid
                return self._send_json({"success": True, "job_id": new_id}, 201)

            # POST /api/bookmarks (Toggle bookmark)
            elif path == '/api/bookmarks':
                job_id = data.get('job_id')
                cursor.execute("SELECT id FROM bookmarks WHERE job_id = ?", (job_id,))
                exists = cursor.fetchone()
                if exists:
                    cursor.execute("DELETE FROM bookmarks WHERE job_id = ?", (job_id,))
                    conn.commit()
                    return self._send_json({"bookmarked": False, "job_id": job_id})
                else:
                    cursor.execute("INSERT INTO bookmarks (job_id) VALUES (?)", (job_id,))
                    conn.commit()
                    return self._send_json({"bookmarked": True, "job_id": job_id})

            # POST /api/dsa/status (Update DSA problem progress)
            elif path == '/api/dsa/status':
                problem_id = data.get('problem_id')
                status = data.get('status') # 'unsolved', 'solved', 'revising'
                is_starred = data.get('is_starred')
                user_notes = data.get('user_notes')

                cursor.execute("SELECT * FROM user_dsa_progress WHERE problem_id = ?", (problem_id,))
                row = cursor.fetchone()

                if row:
                    new_status = status if status is not None else row['status']
                    new_starred = is_starred if is_starred is not None else row['is_starred']
                    new_notes = user_notes if user_notes is not None else row['user_notes']

                    cursor.execute("""
                    UPDATE user_dsa_progress
                    SET status = ?, is_starred = ?, user_notes = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE problem_id = ?
                    """, (new_status, new_starred, new_notes, problem_id))
                else:
                    cursor.execute("""
                    INSERT INTO user_dsa_progress (problem_id, status, is_starred, user_notes)
                    VALUES (?, ?, ?, ?)
                    """, (
                        problem_id,
                        status or 'unsolved',
                        is_starred or 0,
                        user_notes or ''
                    ))
                conn.commit()
                return self._send_json({"success": True, "problem_id": problem_id})

            else:
                return self._send_json({"error": "Endpoint not found"}, 404)
        finally:
            conn.close()

def run_server():
    init_db()
    server_address = ('', PORT)
    httpd = http.server.ThreadingHTTPServer(server_address, PortalHandler)
    print(f"Server started on http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()

if __name__ == '__main__':
    run_server()
