# CareerLaunch — Job Portal & Comprehensive Placement Preparation Platform

A full-stack, production-ready web platform tailored for engineering graduates, job seekers, and developers preparing for campus drives and tech interviews.

---

## 🌟 Key Modules & Features

### 1. 💼 Job Portal
- **Curated Openings**: Tech jobs for freshers (2025/2026 Batch) and experienced engineers (Amazon, Microsoft, Google, TCS Prime, Infosys SP, Swiggy, Razorpay, Accenture).
- **Search & Multi-Facet Filters**: Instant search by job title, company name, required skills, job type (Full-time, Internship, Remote), and experience level.
- **Quick Apply Flow**: Seamless application submission modal (resume link, phone, portfolio, batch, and cover note) with immediate tracking.
- **Save & Bookmarks**: Star jobs to review later and view bookmarked jobs with a single click.
- **Recruiter Job Posting**: Modal allowing recruiters to publish new listings dynamically into the portal database.

### 2. 📚 Preparation Hub (Aptitude, DSA, Technical, HR)
- **Quantitative & Logical Aptitude**: Formulas & shortcuts for Speed Math, Percentages, Profit & Loss, Time & Work, Relative Speed, Syllogisms, and Blood Relations.
- **CS Core Subjects**:
  - **Operating Systems**: Processes vs Threads, CPU Scheduling, Deadlock Coffman Conditions, Virtual Memory & Paging.
  - **DBMS & SQL**: ACID properties, Normalization (1NF to BCNF), Clustered/Non-Clustered Indexes, Nth highest salary SQL patterns.
  - **Computer Networks & OOP**: TCP 3-Way Handshake, DNS Resolution Flow, OSI Layers, SOLID Design Principles.
- **HR & Behavioral Round**: Comprehensive guide to the **STAR Framework** (Situation, Task, Action, Result) with proven scripts for *"Tell me about yourself"*, *"Greatest weakness"*, and insightful questions to ask interviewers.
- **Interactive MCQ Practice Widget**: Real placement MCQs with live answer verification, point tracking, and detailed explanations.

### 3. 🏢 Companies Hiring Process
Detailed blueprints for top tech enterprises and mass hiring giants:
- **Google**: 4-round breakdown, HackerEarth OA pattern, 80% DSA weightage, Graph/DP focus, Googleyness round.
- **Microsoft**: Codility OA, Low-Level Design & OOP, Operating Systems & Concurrency questions, Partner/AA round.
- **Amazon**: HackerRank OA + Work Style Survey, 16 Leadership Principles integration, Bar Raiser round.
- **TCS (Ninja / Digital / Prime)**: Complete TCS NQT pattern (Foundation vs Advanced section), syllabus weightages, Prime track (₹9-11 LPA) strategies.
- **Infosys (SE / DSE / Specialist Programmer)**: InfyTQ & HackWithInfy patterns, pseudocode & cryptarithmetic puzzles.
- **Accenture**: ASE & FSE hiring stages, Cognitive Assessment, Coding test, AI Voice Communication round.

### 4. ⚡ Dedicated DSA Topic-Wise Sheet
- **Curated SDE Sheet**: Categorized into high-frequency topics:
  - *Arrays & Hashing* (Two Sum, Kadane's Algorithm, Next Permutation, Trapping Rain Water)
  - *Strings* (Longest Substring Without Repeating Characters, Valid Anagram)
  - *Linked Lists* (Reverse Linked List, LRU Cache)
  - *Stacks & Queues* (Valid Parentheses)
  - *Trees & BST* (Lowest Common Ancestor)
  - *Graphs* (Number of Islands)
  - *Dynamic Programming* (0/1 Knapsack, Coin Change)
- **Interactive Tracking**:
  - Live checkboxes to mark problems as **Solved** or **Unsolved**.
  - ⭐ Star problems for quick revision.
  - Real-time animated **Progress Bar** with counts for Easy, Medium, and Hard problems.
  - **Solution Drawer**: Comprehensive problem statement, constraints, example I/O, optimal Time & Space complexity ($O(N)$, $O(1)$), clean Python 3 implementation, and direct links to LeetCode & GeeksforGeeks.
  - **Personal Notes**: Editable note box per problem stored persistently in the database.

### 5. 📊 My Placement Dashboard
- Live tracking of all job applications submitted via the portal.
- Quick access to all bookmarked openings.

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+ (Zero external dependencies; uses Python standard library `http.server` & `sqlite3`).

### 1. Initialize & Seed Database
```bash
cd /Users/swadeshna/.gemini/antigravity/scratch/career-portal
python3 seed_data.py
```

### 2. Start the Server
```bash
python3 server.py
```
Visit **[http://localhost:8000](http://localhost:8000)** in your browser.

*(Alternatively, you can open `static/index.html` directly in any web browser; it is built with an offline fallback dataset).*

---

## 📡 REST API Documentation

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/jobs` | `GET` | List all jobs with `?q=`, `?type=`, and `?exp=` filters |
| `/api/jobs/<id>` | `GET` | Retrieve job details by ID |
| `/api/jobs` | `POST` | Create a new job opening |
| `/api/apply` | `POST` | Submit a candidate application |
| `/api/applications` | `GET` | Retrieve submitted job applications |
| `/api/bookmarks` | `GET`, `POST` | Get or toggle bookmarked job IDs |
| `/api/companies` | `GET` | List company hiring guides, rounds & syllabus |
| `/api/prep` | `GET` | Retrieve study notes by `?category=aptitude\|technical\|hr` |
| `/api/prep/questions` | `GET` | Retrieve placement practice MCQs |
| `/api/dsa/topics` | `GET` | List DSA topics with problem counts |
| `/api/dsa/problems` | `GET` | Retrieve DSA problems with user status |
| `/api/dsa/status` | `POST` | Update problem solved status, star, or revision notes |

---

## 📁 Project Structure

```
career-portal/
├── database.py       # SQLite connection and schema creation
├── seed_data.py      # Rich database seed script
├── server.py         # Multi-threaded HTTP server & JSON REST API router
├── README.md         # Documentation & API reference
└── static/
    ├── index.html    # Modern Single-Page Application interface
    ├── style.css     # Design system, CSS variables, dark/light theme
    ├── app.js        # Dynamic UI controllers, state management, quiz & DSA engine
    └── data.js       # Standalone fallback dataset
```
