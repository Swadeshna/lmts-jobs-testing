import json
from database import get_connection, init_db

def seed():
    init_db()
    conn = get_connection()
    cursor = conn.cursor()

    # Clear existing
    cursor.execute("DELETE FROM jobs")
    cursor.execute("DELETE FROM companies")
    cursor.execute("DELETE FROM prep_materials")
    cursor.execute("DELETE FROM prep_questions")
    cursor.execute("DELETE FROM dsa_topics")
    cursor.execute("DELETE FROM dsa_problems")

    # 1. SEED JOBS
    jobs_data = [
        (
            "Software Development Engineer I (SDE-1)",
            "Amazon",
            "https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg",
            "Bangalore / Hyderabad (Hybrid)",
            "Full-time",
            "0 - 2 Years",
            "₹32 - 45 LPA",
            json.dumps(["Java", "C++", "Data Structures", "Distributed Systems", "AWS"]),
            json.dumps(["FAANG", "Freshers Eligible", "Top Tier"]),
            "Join Amazon as an SDE-1 to build scalable, fault-tolerant microservices powering millions of daily transactions globally. You will design, develop, and deploy cloud-native software on AWS.",
            "Strong fundamentals in DSA, OOP, problem-solving, and clean coding. Bachelor's/Master's in CS or related field.",
            "Batch 2024 / 2025 / 2026, Min 7.0 CGPA or 70% with no active backlogs.",
            "2026-10-10",
            "2026-11-15",
            "https://amazon.jobs"
        ),
        (
            "Graduate Software Engineer (Freshers 2026)",
            "Microsoft",
            "https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg",
            "Hyderabad / Noida / Bangalore",
            "Full-time",
            "Fresher (0 Years)",
            "₹38 - 48 LPA",
            json.dumps(["C++", "C#", "Python", "Algorithms", "Azure"]),
            json.dumps(["Campus Drive", "High Package", "MNC"]),
            "Microsoft is hiring 2026 & 2025 graduates for the Azure Core and Developer Experiences teams. Work on world-class hyper-scale cloud infrastructure and AI developer tools.",
            "Proficiency in at least one modern language (C++, C#, Java, Python). Strong grasping of Operating Systems and Algorithms.",
            "B.Tech / B.E / M.Tech in CSE / IT / ECE, CGPA >= 7.5.",
            "2026-10-08",
            "2026-11-20",
            "https://careers.microsoft.com"
        ),
        (
            "Frontend Engineer (React / Next.js)",
            "Razorpay",
            "https://upload.wikimedia.org/wikipedia/commons/8/89/Razorpay_logo.svg",
            "Bangalore (Hybrid)",
            "Full-time",
            "1 - 3 Years",
            "₹22 - 32 LPA",
            json.dumps(["React", "TypeScript", "Next.js", "Web Performance", "TailwindCSS"]),
            json.dumps(["FinTech", "Fast Growing", "Tech Stack"]),
            "Build checkout experiences that process billions of dollars for millions of merchants across India and Southeast Asia. Focus on latency, accessibility, and delightful UX.",
            "Deep understanding of modern JavaScript, React concurrency, state management, and web vitals.",
            "Degree in Engineering / MCA or equivalent practical experience.",
            "2026-10-09",
            "2026-11-10",
            "https://razorpay.com/jobs"
        ),
        (
            "System Engineer (Digital & Prime Tracks)",
            "Tata Consultancy Services (TCS)",
            "https://upload.wikimedia.org/wikipedia/commons/b/b1/Tata_Consultancy_Services_Logo.svg",
            "Pan India (Multiple Locations)",
            "Full-time",
            "0 - 1 Years",
            "₹7.0 - 9.5 LPA (Prime / Digital)",
            json.dumps(["Python", "Java", "SQL", "Cloud Basics", "Data Analysis"]),
            json.dumps(["Mass Recruiter", "NQT Special", "Multiple Openings"]),
            "TCS National Qualifier Test (NQT) hiring for high-performing graduates across India for Digital and Prime roles. Work on enterprise AI transformation and BFSI systems.",
            "Cognitive ability, programming proficiency in C/C++/Java/Python, and clear communication.",
            "B.E. / B.Tech / M.E. / M.Tech / MCA (2025 & 2026 Batch), Min 60% throughout 10th, 12th, and Degree.",
            "2026-10-05",
            "2026-11-30",
            "https://tcs.com/careers"
        ),
        (
            "Associate Software Engineer",
            "Accenture",
            "https://upload.wikimedia.org/wikipedia/commons/c/cd/Accenture.svg",
            "Bangalore, Pune, Hyderabad, Gurgaon, Chennai",
            "Full-time",
            "Freshers",
            "₹4.5 - 6.5 LPA",
            json.dumps(["Core Java", "Python", "SQL", "Agile", "DevOps"]),
            json.dumps(["Pan India", "Training Provided", "Freshers Welcome"]),
            "Join Accenture's Advanced Technology Centers in India (ATCI). You will design, develop, test, and maintain innovative software for Global 500 enterprises.",
            "Good analytical thinking, programming logic in any language, familiarity with database queries.",
            "All Engineering branches eligible, 2025/2026 batch, Minimum 65% aggregate with 0 active backlogs.",
            "2026-10-07",
            "2026-11-25",
            "https://accenture.com/careers"
        ),
        (
            "Specialist Programmer (Power Programmer)",
            "Infosys",
            "https://upload.wikimedia.org/wikipedia/commons/9/95/Infosys_logo.svg",
            "Bangalore / Pune / Hyderabad",
            "Full-time",
            "Freshers (2026 Batch)",
            "₹9.5 - 12.0 LPA",
            json.dumps(["Advanced DSA", "Dynamic Programming", "Python", "Java", "System Design"]),
            json.dumps(["HackWithInfy", "High Compensation", "Elite Track"]),
            "Infosys Specialist Programmer (SP) is an elite coding cadre focusing on high-end tech, complex algorithmic problem solving, machine learning, and cloud architecture.",
            "Ranked high in HackWithInfy or InfyTQ with stellar competitive programming credentials.",
            "B.E./B.Tech/M.E./M.Tech/MCA from any stream, 60% or 6.0 CGPA.",
            "2026-10-06",
            "2026-11-18",
            "https://infosys.com/careers"
        ),
        (
            "Backend Engineer - Go / Microservices",
            "Swiggy",
            "https://upload.wikimedia.org/wikipedia/en/1/12/Swiggy_logo.svg",
            "Bangalore (Remote / Hybrid)",
            "Full-time",
            "1 - 4 Years",
            "₹25 - 38 LPA",
            json.dumps(["Go", "Kafka", "PostgreSQL", "Redis", "Distributed Systems"]),
            json.dumps(["Consumer Tech", "High Scale", "Stock Options"]),
            "Deliver food, groceries (Instamart), and dining experiences at scale. Build high-concurrency order dispatching and live tracking systems with sub-50ms latency.",
            "Deep experience with Golang or Java, distributed message queues (Kafka), cache optimization, and microservice architectures.",
            "B.Tech/B.E in Computer Science or related degree.",
            "2026-10-04",
            "2026-11-12",
            "https://swiggy.com/careers"
        ),
        (
            "Software Engineer - Core Search & AI",
            "Google",
            "https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg",
            "Bangalore / Hyderabad",
            "Full-time",
            "0 - 2 Years",
            "₹45 - 60 LPA",
            json.dumps(["C++", "Python", "DSA", "Algorithms", "AI/ML"]),
            json.dumps(["FAANG", "Prestigious", "Research & Scale"]),
            "Develop next-generation information retrieval and multimodal search algorithms. Solve algorithmic challenges that operate at billion-user scale.",
            "Exemplary data structures & algorithm mastery, code cleanliness, algorithmic complexity optimization.",
            "BS/MS in Computer Science or related technical field, 2024-2026 passouts.",
            "2026-10-11",
            "2026-12-01",
            "https://careers.google.com"
        )
    ]

    for j in jobs_data:
        cursor.execute('''
        INSERT INTO jobs (
            title, company, company_logo, location, job_type, experience, salary,
            skills, tags, description, requirements, eligibility, posted_date, deadline, apply_url
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', j)

    # 2. SEED COMPANIES HIRING PROCESS
    companies_data = [
        (
            "Google",
            "google",
            "https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg",
            "Product / Big Tech",
            "Tier 1",
            "Global technology leader in search, cloud computing, artificial intelligence, and operating systems.",
            "₹45 - 65 LPA (Fresher Base + Stocks + Bonus)",
            "6.5+ CGPA or 65% (Relaxed for exceptional contest rankers)",
            "CSE, IT, ECE, Mathematics & Computing, AI/DS",
            "2025, 2026 & Recent Graduates",
            json.dumps({
                "rounds_count": 4,
                "online_assessment": "90 Mins, 2 Algorithmic coding questions on HackerEarth/Google platform (Graph, DP, Greedy)",
                "elimination": "High cutoff in OA (usually 100% test cases pass required)"
            }),
            json.dumps([
                {"round": "Round 1: Online Assessment", "details": "2 medium-hard coding questions (90 mins). Focus on Time/Space complexity, edge cases."},
                {"round": "Round 2: Technical Interview 1", "details": "45 mins live Google Meet + Google Docs/CoderPad. DSA: Trees, Graphs, Two Pointers. Focus on communication."},
                {"round": "Round 3: Technical Interview 2", "details": "45 mins. Dynamic Programming, Advanced Data Structures (Trie, Heap, Segment Tree), System considerations."},
                {"round": "Round 4: Googleyness & Leadership", "details": "45 mins with Engineering Manager. Navigating ambiguity, ethical scenarios, cross-functional teamwork."}
            ]),
            json.dumps({
                "dsa_weightage": "80%",
                "cs_fundamentals": "10%",
                "behavioral": "10%",
                "key_topics": ["Graphs (Dijkstra, BFS/DFS, TopoSort)", "Dynamic Programming", "Binary Trees & BST", "String algorithms", "Disjoint Set Union (DSU)"]
            }),
            "1. Think out loud! Google interviewers grade your thought process more than the final snippet.\n2. Always state brute force, then optimize.\n3. Write production-quality code with descriptive variable names and edge-case testing.",
            json.dumps(["LRU Cache", "Course Schedule II", "Trapping Rain Water", "Word Ladder", "Median of Two Sorted Arrays"])
        ),
        (
            "Microsoft",
            "microsoft",
            "https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg",
            "Product / Cloud Leader",
            "Tier 1",
            "World's leading computing and cloud enterprise powering Windows, Azure, Office 365, and OpenAI partnership.",
            "₹42 - 52 LPA",
            "7.0+ CGPA with no active backlogs",
            "B.Tech / M.Tech (CSE, IT, ECE, EE)",
            "2025 & 2026 Batch",
            json.dumps({
                "rounds_count": 4,
                "online_assessment": "Codility / Mettl: 3 coding questions (Easy, Medium, Hard) in 90-120 minutes + CS MCQs",
                "elimination": "2.5+ questions solved needed for shortlist"
            }),
            json.dumps([
                {"round": "Round 1: Online Assessment", "details": "Codility Platform: 3 algorithmic questions. Automated test suite includes hidden stress tests."},
                {"round": "Round 2: Technical Round 1", "details": "Data structures, Arrays, Linked Lists, Binary Trees, Recursion. Emphasis on writing bug-free code."},
                {"round": "Round 3: Technical Round 2", "details": "System concepts, OOP Design patterns, Operating Systems (Threads, Deadlocks), DBMS (Indexing)."},
                {"round": "Round 4: AA Round (As Appropriate)", "details": "Senior Partner / Director round. Culture fit, project deep-dive, low-level design problem."}
            ]),
            json.dumps({
                "dsa_weightage": "60%",
                "cs_fundamentals": "25%",
                "behavioral": "15%",
                "key_topics": ["Binary Trees (LCA, Views)", "Linked Lists", "OOP & Design Patterns", "Concurrency & OS", "Dynamic Programming"]
            }),
            "1. Microsoft values clean, modular, object-oriented code.\n2. Know your resume projects inside out — be ready to whiteboard your database schema and architecture.\n3. Ask thoughtful questions about Microsoft products at the end.",
            json.dumps(["Serialize and Deserialize Binary Tree", "Reverse Nodes in k-Group", "Design Min Stack", "Rotting Oranges", "LRU Cache"])
        ),
        (
            "Amazon",
            "amazon",
            "https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg",
            "Product / E-Commerce & Cloud",
            "Tier 1",
            "World's leading e-commerce, cloud provider (AWS), and digital streaming platform driven by Customer Obsession.",
            "₹35 - 46 LPA",
            "6.5+ CGPA or 65%",
            "CSE, IT, ECE, EEE, AI",
            "2025 & 2026 Batch",
            json.dumps({
                "rounds_count": 4,
                "online_assessment": "Part 1: 2 Coding Problems (70 mins). Part 2: Work Style Assessment / 16 Leadership Principles (20 mins).",
                "elimination": "Both coding performance and Leadership Principle alignment are strictly evaluated."
            }),
            json.dumps([
                {"round": "Round 1: Online Assessment", "details": "HackerRank: 2 medium DSA questions + Work Style Survey testing 16 Leadership Principles."},
                {"round": "Round 2: Technical Round 1", "details": "60 mins: 1-2 coding problems (Greedy/Trees/HashMaps) + 20 mins behavioral LP questions."},
                {"round": "Round 3: Technical Round 2", "details": "60 mins: Graph traversal, Dynamic Programming, Heap problems + 20 mins behavioral LP questions."},
                {"round": "Round 4: Bar Raiser", "details": "Evaluator from an unrelated Amazon team ensuring the candidate is better than 50% of current peers. Heavy focus on Customer Obsession & Bias for Action."}
            ]),
            json.dumps({
                "dsa_weightage": "60%",
                "leadership_principles": "30%",
                "cs_fundamentals": "10%",
                "key_topics": ["Heaps & Priority Queues", "BFS/DFS Grid traversal", "Dynamic Programming", "Hash Tables", "Amazon 16 Leadership Principles"]
            }),
            "1. Prepare 2 STAR-format stories for EVERY Amazon Leadership Principle (especially Customer Obsession, Ownership, Bias for Action, Have Backbone).\n2. Write functional, testable code without syntax errors.\n3. Always discuss boundary conditions and large dataset limits.",
            json.dumps(["Top K Frequent Elements", "Number of Islands", "Course Schedule", "Word Search", "Sliding Window Maximum"])
        ),
        (
            "TCS (Ninja / Digital / Prime)",
            "tcs",
            "https://upload.wikimedia.org/wikipedia/commons/b/b1/Tata_Consultancy_Services_Logo.svg",
            "IT Services / Global Giant",
            "Mass & Digital",
            "India's largest IT exporter and market leader, offering 3 distinct hiring tracks: Ninja (3.36 LPA), Digital (7 LPA), Prime (9-11 LPA).",
            "₹3.36 LPA (Ninja) | ₹7.0 LPA (Digital) | ₹9-11.5 LPA (Prime)",
            "Minimum 60% aggregate in 10th, 12th, Diploma, UG, and PG. Maximum 1 active backlog allowed at time of test.",
            "All Engineering disciplines (B.E/B.Tech/M.E/M.Tech/MCA)",
            "2025 & 2026 Batch",
            json.dumps({
                "rounds_count": 3,
                "online_assessment": "TCS NQT: Foundation Section (Cognitive, Numerical, Reasoning, Verbal - 75 Mins) + Advanced Section (Advanced Quantitative, Advanced Reasoning, 2 Coding Questions - 90 Mins).",
                "elimination": "High score in Advanced Section qualifies candidates for Prime and Digital interviews."
            }),
            json.dumps([
                {"round": "Round 1: TCS NQT Examination", "details": "National Qualifier Test conducted at TCS iON centres or web-proctored. Tests Aptitude, Verbal, Logical, and 2 Hands-on Coding questions (Easy-Medium)."},
                {"round": "Round 2: Technical Interview", "details": "Discussion on C/C++/Java/Python, DBMS SQL queries, basic DSA (Arrays, Strings, Searching), and Final Year Project."},
                {"round": "Round 3: Managerial & HR Round", "details": "Willingness to relocate, night shifts, communication check, ethical questions, Tata code of conduct."}
            ]),
            json.dumps({
                "aptitude_weightage": "40%",
                "coding_weightage": "40%",
                "cs_basics_hr": "20%",
                "key_topics": ["Percentages, Profit & Loss, Time & Work", "Syllogisms & Seating Arrangement", "Basic Array Manipulations", "Strings & Matrix operations", "SQL Joins & Group By"]
            }),
            "1. Practice with on-screen calculator as allowed in TCS iON.\n2. Complete Foundation with zero negative marks, and write working code for both advanced problems to unlock the ₹9 LPA Prime interview.\n3. Revise basic SQL commands and OOP concepts thoroughly.",
            json.dumps(["Count occurrences in array", "Matrix Rotation", "Reverse words in a sentence", "Armstrong Number & Primes", "Binary to Decimal conversions"])
        ),
        (
            "Infosys (SE / DSE / Specialist Programmer)",
            "infosys",
            "https://upload.wikimedia.org/wikipedia/commons/9/95/Infosys_logo.svg",
            "IT Services & Consulting",
            "Mass & High Package Track",
            "Infosys hires through InfyTQ, HackWithInfy, and National On-Campus Drives for System Engineer (3.6 LPA), DSE (6.25 LPA), and Specialist Programmer (9.5 LPA).",
            "₹3.6 LPA (SE) | ₹6.25 LPA (DSE) | ₹9.5 - 12 LPA (Specialist Programmer)",
            "60% or 6.0 CGPA across academic career. Max 1 active backlog permitted.",
            "All Engineering streams and MCA",
            "2025 & 2026 Batch",
            json.dumps({
                "rounds_count": 2,
                "online_assessment": "Infosys Online Test: Reasoning Ability (15 Qs, 25 mins), Mathematical Ability (10 Qs, 35 mins), Verbal (20 Qs, 20 mins), Pseudocode (5 Qs, 10 mins), Puzzle Solving (4 Qs, 10 mins).",
                "elimination": "Sectional cutoffs exist in every section."
            }),
            json.dumps([
                {"round": "Round 1: Online Assessment / HackWithInfy", "details": "Aptitude + Pseudocode + Coding. For Specialist Programmer, HackWithInfy involves 3 competitive coding problems in 3 hours."},
                {"round": "Round 2: Technical + HR Interview", "details": "Technical discussion on OOP, Data Structures, DBMS, Web technologies, and soft skills."}
            ]),
            json.dumps({
                "aptitude_weightage": "50% (SE track)",
                "coding_weightage": "90% (SP track)",
                "interview": "20%",
                "key_topics": ["Permutations & Probability", "Pseudocode & Bitwise operations", "Cryptarithmetic puzzles", "Dynamic Programming", "Tree & Graph traversals"]
            }),
            "1. Focus heavily on Cryptarithmetic questions and Pseudocode analysis in the Infosys test.\n2. Time management is crucial: questions have individual section timers!\n3. For Specialist Programmer, solve LeetCode Medium/Hard DP and Tree problems.",
            json.dumps(["Longest Palindromic Substring", "Coin Change Problem", "Subarray with given sum", "Detect loop in linked list", "Knapsack 0/1"])
        ),
        (
            "Accenture",
            "accenture",
            "https://upload.wikimedia.org/wikipedia/commons/c/cd/Accenture.svg",
            "IT & Consulting",
            "Tier 2 / Mass",
            "Global professional services company with leading capabilities in digital, cloud and security.",
            "₹4.5 LPA (ASE) | ₹6.5 - 11.8 LPA (FSE / Advanced)",
            "65% or 6.5 CGPA in current degree. No active backlogs allowed at registration.",
            "All B.E/B.Tech/M.E/M.Tech/MCA branches",
            "2025 & 2026 Batch",
            json.dumps({
                "rounds_count": 4,
                "online_assessment": "Stage 1: Cognitive & Technical Assessment (90 Qs, 90 mins). Stage 2: Coding Assessment (2 questions, 45 mins). Stage 3: Communication Assessment (AI Voice proctored).",
                "elimination": "Stage 1 results are declared within 5 minutes. Passing Stage 1 unlocks the Coding test."
            }),
            json.dumps([
                {"round": "Round 1: Cognitive & Technical Assessment", "details": "English Ability, Critical Thinking, Abstract Reasoning, MS Office, Common Application/Security, Pseudocode."},
                {"round": "Round 2: Coding Assessment", "details": "2 problems to be solved in C/C++/Java/Python/DotNet within 45 minutes."},
                {"round": "Round 3: Communication Assessment", "details": "Automated voice-based assessment testing reading, listening, sentence repeating, storytelling, and speech clarity."},
                {"round": "Round 4: Technical & HR Interview", "details": "30 mins interview covering resume projects, learning agility, team experiences, and scenario questions."}
            ]),
            json.dumps({
                "cognitive_technical": "45%",
                "coding": "35%",
                "communication": "20%",
                "key_topics": ["Pseudocode tracing", "MS Office shortcuts & features", "Networking basics", "Array operations", "English grammar & comprehension"]
            }),
            "1. Use a high-quality noise-free headset for the Communication Assessment.\n2. In pseudocode questions, trace loop boundaries and bitwise XOR/AND carefully.\n3. Prepare a crisp 2-minute elevator pitch for your final project.",
            json.dumps(["Difference between max and min in array", "String character frequency", "Fibonacci sequence variation", "Binary string operation", "Inversion count"])
        )
    ]

    for c in companies_data:
        cursor.execute('''
        INSERT INTO companies (
            name, slug, logo, category, tier, description, package_range,
            eligibility_cgpa, eligibility_branches, eligibility_batch,
            exam_pattern, rounds_breakdown, syllabus, interview_tips, frequently_asked
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', c)

    # 3. SEED PREPARATION MATERIALS (Aptitude, DSA Core, Technical, HR)
    prep_data = [
        # Aptitude
        (
            "aptitude",
            "Quantitative Aptitude",
            "Speed Math, Percentages & Profit-Loss Master Cheatsheet",
            "Comprehensive formulas, shortcut tricks, and speed calculation methods for campus placement aptitude exams.",
            "10 min read",
            """# Speed Math & Arithmetic Formulas

### 1. Speed Math Shortcuts
* **Multiplication by 11:** For `25 * 11`, write `2` and `5`, place `2+5=7` in the middle: `275`.
* **Squaring numbers ending in 5:** For `75^2`, multiply `7 * (7+1) = 56`, append `25` -> `5625`.
* **Percentage Base Conversion:**
  * `1/2 = 50%` | `1/3 = 33.33%` | `1/4 = 25%` | `1/5 = 20%`
  * `1/6 = 16.66%` | `1/7 = 14.28%` | `1/8 = 12.5%` | `1/9 = 11.11%`

### 2. Profit and Loss
* $\\text{Profit} = SP - CP$
* $\\text{Profit \\%} = \\left(\\frac{\\text{Profit}}{CP}\\right) \\times 100$
* **Successive Discount:** $D_{net} = D_1 + D_2 - \\frac{D_1 \\times D_2}{100}$

### 3. Time, Speed & Distance
* $\\text{Speed} = \\frac{\\text{Distance}}{\\text{Time}}$
* $1 \\text{ km/hr} = \\frac{5}{18} \\text{ m/s}$
* **Average Speed (Equal Distances):** $\\frac{2xy}{x+y}$
* **Relative Speed:**
  * Same direction: $S_1 - S_2$
  * Opposite direction: $S_1 + S_2$

### 4. Time & Work
* If A takes $x$ days and B takes $y$ days, together they take: $\\frac{xy}{x+y}$ days.
* **Work done formula:** $\\frac{M_1 D_1 H_1}{W_1} = \\frac{M_2 D_2 H_2}{W_2}$""",
            json.dumps(["Master fraction-to-percentage conversions", "Remember relative speed formulas for trains and boats", "Use LCM method for Time & Work problems"])
        ),
        (
            "aptitude",
            "Logical Reasoning",
            "Syllogisms, Blood Relations & Seating Arrangement",
            "Proven strategies and Venn diagram techniques to tackle tricky deductive reasoning questions.",
            "8 min read",
            """# Deductive Logic & Blood Relations

### 1. Syllogisms Master Rules
Use standard Venn Diagram overlaps:
* **All A are B:** Circle A is completely inside Circle B.
* **Some A are B:** Circle A and Circle B overlap.
* **No A is B:** Circle A and Circle B are completely disjoint.
* **Golden Rule for 'Possibility':** If a conclusion is valid in at least ONE possible Venn diagram, the "possibility" conclusion is TRUE.

### 2. Blood Relations Decoding
Always draw a family tree using conventions:
* Male = `[+]` or Square
* Female = `[-]` or Circle
* Married Couple = `<->` (Double line)
* Siblings = `---` (Horizontal line)
* Generational gap = `|` (Vertical line)

### 3. Circular Seating Arrangement
* **Facing Centre:** Left = Clockwise, Right = Anti-Clockwise.
* **Facing Outside:** Left = Anti-Clockwise, Right = Clockwise.
* *Strategy:* Always start with direct definite clues (e.g., 'A sits 3rd to right of B') before placing conditional clues.""",
            json.dumps(["Venn diagrams resolve 95% of syllogisms", "Draw generational family trees step by step", "Distinguish clockwise vs anti-clockwise based on facing direction"])
        ),
        # Technical
        (
            "technical",
            "Operating Systems",
            "Processes, Concurrency, Deadlocks & Virtual Memory",
            "High-frequency OS interview concepts asked by top engineering companies and campus interviews.",
            "12 min read",
            """# Operating Systems Core Notes

### 1. Process vs Thread
* **Process:** An executing program with independent address space, memory, registers, and open file handles. High context-switch overhead.
* **Thread:** Lightweight unit of execution within a process sharing code, data, and OS resources, but having its own stack and registers.

### 2. Process Scheduling
* **Preemptive:** CPU can be taken away (Round Robin, Shortest Remaining Time First).
* **Non-preemptive:** Runs till completion or I/O (FCFS, Shortest Job First).

### 3. Deadlock & 4 Coffman Conditions
Deadlock occurs if and only if all 4 conditions hold simultaneously:
1. **Mutual Exclusion:** Resources cannot be shared.
2. **Hold and Wait:** A process holds resources while waiting for more.
3. **No Preemption:** Resources cannot be forcibly seized.
4. **Circular Wait:** Closed chain of processes waiting on each other.
* *Prevention:* Break any one condition (e.g., hierarchical resource ordering prevents Circular Wait).

### 4. Virtual Memory & Paging
* **Paging:** Division of physical memory into fixed-size frames and logical memory into pages. Eliminates external fragmentation.
* **Page Fault:** CPU tries to access a page not present in physical RAM; OS brings it from secondary storage via Page Replacement Algorithms (LRU, FIFO, Optimal).
* **Thrashing:** System spends more time swapping pages in/out than executing instructions.""",
            json.dumps(["Recall the 4 Coffman conditions verbatim", "Understand LRU page replacement algorithm", "Know why thread context switches are faster than processes"])
        ),
        (
            "technical",
            "DBMS & SQL",
            "ACID Properties, Normalization, Indexing & Joins",
            "Everything you need to crack database rounds: ACID, 1NF to BCNF, B-Trees, and complex SQL queries.",
            "12 min read",
            """# Database Management Systems (DBMS)

### 1. ACID Properties
* **Atomicity:** All-or-nothing execution of transactions.
* **Consistency:** Database transitions only between valid states conforming to constraints.
* **Isolation:** Concurrent transactions execute without interfering (Isolation levels: Read Uncommitted, Read Committed, Repeatable Read, Serializable).
* **Durability:** Committed transactions persist even in system crashes (WAL - Write Ahead Logging).

### 2. Database Normalization
* **1NF:** Eliminate repeating groups; atomic column values.
* **2NF:** In 1NF + No partial dependency (non-key attributes depend on whole candidate key).
* **3NF:** In 2NF + No transitive dependency ($A \\rightarrow B$ and $B \\rightarrow C$).
* **BCNF:** For every functional dependency $X \\rightarrow Y$, $X$ must be a super key.

### 3. Indexing & B+ Trees
* Why Indexes? Fast retrieval from $O(N)$ full table scan to $O(\\log N)$.
* Clustered Index (data rows stored in sorted order of key, only 1 per table) vs Non-Clustered Index (separate pointer structure, multiple allowed).

### 4. Top High-Frequency SQL Patterns
```sql
-- 2nd Highest Salary
SELECT MAX(salary) FROM employees 
WHERE salary < (SELECT MAX(salary) FROM employees);

-- Alternatively using DENSE_RANK()
WITH RankedSalaries AS (
  SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) as rank_num
  FROM employees
)
SELECT salary FROM RankedSalaries WHERE rank_num = 2;
```""",
            json.dumps(["Explain ACID using a bank transfer example", "Understand the difference between clustered and non-clustered index", "Practice window functions: DENSE_RANK, ROW_NUMBER"])
        ),
        (
            "technical",
            "Computer Networks & OOP",
            "OSI Layers, TCP vs UDP, HTTP/2/3 & SOLID Principles",
            "Network protocols, DNS resolution pipeline, and Object-Oriented Design principles.",
            "10 min read",
            """# Computer Networks & OOP Fundamentals

### 1. OSI Model vs TCP/IP
* 7 Layers: Application, Presentation, Session, Transport, Network, Data Link, Physical.
* **Transport Layer:** Port numbers, reliability, flow control (TCP) or speed (UDP).
* **Network Layer:** IP routing, packets, routers.
* **Data Link Layer:** MAC addresses, Ethernet frames, switches.

### 2. TCP 3-Way Handshake
1. Client sends `SYN` (Synchronize sequence number).
2. Server responds with `SYN-ACK`.
3. Client replies with `ACK`. Connection established!
* Connection teardown uses a 4-way `FIN` handshake.

### 3. DNS Lookup Step-by-Step
When typing `www.google.com`:
1. Check browser cache -> OS cache -> Router cache.
2. Query ISP Recursive Resolver.
3. Query Root Name Server (`.`) -> TLD Name Server (`.com`) -> Authoritative Name Server (`google.com`).
4. IP address returned and cached.

### 4. SOLID Principles of OOP
* **S - Single Responsibility:** A class should have only one reason to change.
* **O - Open/Closed:** Open for extension, closed for modification.
* **L - Liskov Substitution:** Subtypes must be substitutable for their base types without altering correctness.
* **I - Interface Segregation:** Prefer multiple small interfaces over one bloated interface.
* **D - Dependency Inversion:** Depend on abstractions, not on concrete implementations.""",
            json.dumps(["Memorize the TCP 3-way handshake diagram", "Walk through the complete browser URL to page render journey", "Give real-world code examples for each SOLID principle"])
        ),
        # HR
        (
            "hr",
            "Behavioral & HR Round",
            "The STAR Method, Top 20 Questions & Winning Scripts",
            "Structure your life stories into persuasive interview answers that impress hiring managers.",
            "15 min read",
            """# Cracking the HR & Behavioral Round

### The STAR Framework
Always frame project and conflict answers using:
* **S (Situation):** Set the context, team size, timeline, and stakes (15-20% of time).
* **T (Task):** What was the exact challenge or goal assigned to YOU (10-15%).
* **A (Action):** What specific tools, initiatives, and steps did YOU take? Use "I" instead of "we" (50-60%).
* **R (Result):** Measurable impact: latency dropped 40%, saved 20 hrs/week, won 1st prize (15-20%).

---

### Winning Scripts for Crucial Questions

#### 1. "Tell me about yourself"
* **Structure:** Present -> Past -> Future
* *Model Answer:* "I am a Final Year Computer Science student passionate about distributed systems and cloud engineering. Over the past two years, I developed a real-time microservices ordering engine and interned at XYZ where I optimized database queries by 35%. I've solved over 300 DSA problems and won two hackathons. What excites me about joining your team is your scale and culture of innovation, where I can apply my problem-solving skills to build mission-critical products."

#### 2. "What is your biggest weakness?"
* *Formula:* Pick a genuine professional trait, show self-awareness, and detail how you actively manage it.
* *Model Answer:* "Earlier, I struggled with delegating tasks because I wanted everything done to exact specifications, which caused unnecessary bottlenecks during hackathons. I realized this was unsustainable, so I adopted Scrum sprint planning and learned to trust teammates while using code reviews as our quality gate. This helped our team deliver projects 25% faster."

#### 3. "Why should we hire you?"
* *Model Answer:* "I bring a strong combination of algorithmic foundation, rapid learning agility, and proven teamwork. Beyond technical skills, I have a track record of taking end-to-end ownership. I am ready to ramp up quickly and make a tangible contribution from day one."

#### 4. Questions to Ask the Interviewer at the End
* "What does a successful first 90 days look like for a new graduate joining this team?"
* "What is the biggest engineering challenge the team is currently tackling?"
* "How does the team foster mentorship and continuous learning for junior engineers?" """,
            json.dumps(["Use the STAR technique with quantifiable metrics", "Never say you have no weaknesses or say 'I am a perfectionist'", "Always ask 2 insightful questions at the end of the interview"])
        )
    ]

    for p in prep_data:
        cursor.execute('''
        INSERT INTO prep_materials (
            category, subcategory, title, summary, read_time, content_markdown, key_takeaways
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', p)

    # 4. SEED PRACTICE QUESTIONS / MCQs
    questions_data = [
        # Aptitude MCQs
        (
            "aptitude",
            "Quantitative",
            "A train 180 meters long is running at a speed of 54 km/h. How much time will it take to pass a standing man on the platform?",
            json.dumps(["10 seconds", "12 seconds", "15 seconds", "18 seconds"]),
            1,
            "Speed = 54 km/h = 54 * (5/18) = 15 m/s. Distance to cover = length of train = 180 m. Time = Distance / Speed = 180 / 15 = 12 seconds.",
            "Easy",
            json.dumps(["TCS", "Infosys", "Wipro", "Accenture"])
        ),
        (
            "aptitude",
            "Quantitative",
            "A and B can do a work in 12 days, B and C in 15 days, and C and A in 20 days. If A, B, and C work together, in how many days will they complete the work?",
            json.dumps(["5 days", "10 days", "12 days", "8 days"]),
            1,
            "2(A + B + C)'s 1 day work = 1/12 + 1/15 + 1/20 = (5 + 4 + 3)/60 = 12/60 = 1/5. Therefore, (A + B + C)'s 1 day work = 1/10. Work completed in 10 days.",
            "Medium",
            json.dumps(["TCS Prime", "Cognizant", "Capgemini"])
        ),
        (
            "aptitude",
            "Quantitative",
            "A shopkeeper marks an article at 40% above the cost price and allows a discount of 25% on the marked price. What is his net profit or loss percentage?",
            json.dumps(["5% Profit", "10% Profit", "5% Loss", "15% Profit"]),
            0,
            "Let CP = 100. MP = 140. Discount = 25% of 140 = 35. SP = 140 - 35 = 105. Net Profit = 105 - 100 = 5%.",
            "Easy",
            json.dumps(["Accenture", "TCS", "Infosys"])
        ),
        (
            "aptitude",
            "Logical",
            "Pointing to a photograph, Rohit said, 'She is the mother of my father's only son's daughter.' How is the woman related to Rohit?",
            json.dumps(["Sister", "Daughter", "Wife", "Mother"]),
            2,
            "Father's only son = Rohit himself. Rohit's daughter's mother = Rohit's wife. Hence, the woman is Rohit's wife.",
            "Medium",
            json.dumps(["Infosys", "TCS", "Amazon"])
        ),
        # Technical MCQs
        (
            "technical",
            "Operating Systems",
            "Which of the following condition is NOT necessary for a deadlock to occur?",
            json.dumps(["Mutual Exclusion", "Circular Wait", "Preemption allowed", "Hold and Wait"]),
            2,
            "For deadlock to occur, NO PREEMPTION is required. If preemption is allowed, deadlock cannot occur.",
            "Easy",
            json.dumps(["Microsoft", "Google", "Amazon", "Infosys"])
        ),
        (
            "technical",
            "DBMS",
            "Which normal form deals with the elimination of transitive functional dependencies?",
            json.dumps(["1NF", "2NF", "3NF", "BCNF"]),
            2,
            "Third Normal Form (3NF) requires the relation to be in 2NF and have no transitive functional dependencies (X -> Y and Y -> Z).",
            "Medium",
            json.dumps(["Amazon", "Oracle", "TCS Digital", "Accenture"])
        ),
        (
            "technical",
            "Computer Networks",
            "Which protocol operates at the Transport Layer and provides reliable, ordered, and error-checked delivery?",
            json.dumps(["UDP", "IP", "TCP", "ICMP"]),
            2,
            "TCP (Transmission Control Protocol) is a connection-oriented Transport Layer protocol providing flow control, reliability, and ordered byte streaming.",
            "Easy",
            json.dumps(["Cisco", "Microsoft", "Accenture"])
        ),
        (
            "technical",
            "OOP Concepts",
            "Which principle of OOP states that subclasses should be substitutable for their parent classes without breaking functionality?",
            json.dumps(["Single Responsibility", "Open/Closed Principle", "Liskov Substitution Principle", "Interface Segregation"]),
            2,
            "Liskov Substitution Principle (the 'L' in SOLID) requires that derived classes must be substitutable for their base types without altering correctness.",
            "Medium",
            json.dumps(["Google", "Microsoft", "Atlassian"])
        ),
        # HR Scenario Questions
        (
            "hr",
            "HR & Culture",
            "If an interviewer asks: 'Tell me about a time you strongly disagreed with a teammate or lead. How did you handle it?' What is the best strategy?",
            json.dumps([
                "Say that I never disagree with anyone because I always follow instructions without questioning.",
                "Explain the disagreement calmly, focus on data/facts rather than emotions, describe the constructive compromise reached, and emphasize team success.",
                "Explain that my teammate was wrong and I escalated immediately to the professor/manager to prove I was right.",
                "Avoid the question by saying I only work independently."
            ]),
            1,
            "Hiring managers look for psychological safety, objective data-driven reasoning, maturity, empathy, and constructive resolution skills.",
            "Easy",
            json.dumps(["Amazon (Have Backbone; Disagree & Commit)", "Google", "Microsoft"])
        )
    ]

    for q in questions_data:
        cursor.execute('''
        INSERT INTO prep_questions (
            category, subcategory, question, options, correct_index, explanation, difficulty, company_tags
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', q)

    # 5. SEED DSA TOPICS
    dsa_topics = [
        ("Arrays & Hashing", "arrays-hashing", "grid", "Fundamental arrays, frequency maps, prefix sums, and two-pointer basics.", 1),
        ("Strings", "strings", "type", "Pattern matching, anagrams, palindromes, sliding window string problems.", 2),
        ("Linked Lists", "linked-lists", "link", "Pointers, fast & slow pointers, reversing, merging, cycle detection.", 3),
        ("Stacks & Queues", "stacks-queues", "layers", "Monotonic stacks, parentheses matching, min-stack, BFS queues.", 4),
        ("Trees & BST", "trees-bst", "git-branch", "Binary trees, traversals, height, LCA, BST properties, serialization.", 5),
        ("Graphs", "graphs", "share-2", "BFS, DFS, cycle detection, topological sort, Dijkstra, shortest path.", 6),
        ("Dynamic Programming", "dynamic-programming", "cpu", "Memoization, tabulation, 1D/2D DP, knapsack, LCS, LIS, grid paths.", 7),
        ("Recursion & Backtracking", "backtracking", "rotate-ccw", "Subsets, permutations, combinations, N-Queens, maze solving.", 8),
        ("Greedy & Searching", "greedy-searching", "search", "Binary search variations, interval scheduling, fractional knapsack.", 9)
    ]

    for t in dsa_topics:
        cursor.execute('''
        INSERT INTO dsa_topics (name, slug, icon, description, order_idx)
        VALUES (?, ?, ?, ?, ?)
        ''', t)

    # Get topic IDs mapping
    cursor.execute("SELECT id, slug FROM dsa_topics")
    topic_map = {row['slug']: row['id'] for row in cursor.fetchall()}

    # 6. SEED COMPREHENSIVE DSA PROBLEMS (SDE Sheet)
    dsa_problems = [
        # Arrays & Hashing
        (
            topic_map["arrays-hashing"],
            "Two Sum",
            "Easy",
            "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. You may assume each input has exactly one solution.",
            "2 <= nums.length <= 10^4, -10^9 <= nums[i] <= 10^9",
            json.dumps([{"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]"}, {"input": "nums = [3,2,4], target = 6", "output": "[1,2]"}]),
            "Time: O(N), Space: O(N) using HashMap",
            """def twoSum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []""",
            "https://leetcode.com/problems/two-sum/",
            "https://www.geeksforgeeks.org/check-if-pair-with-given-sum-exists-in-array/",
            json.dumps(["Google", "Amazon", "Microsoft", "Meta", "TCS"])
        ),
        (
            topic_map["arrays-hashing"],
            "Kadane's Algorithm (Maximum Subarray)",
            "Medium",
            "Given an integer array nums, find the subarray with the largest sum, and return its sum.",
            "1 <= nums.length <= 10^5, -10^4 <= nums[i] <= 10^4",
            json.dumps([{"input": "nums = [-2,1,-3,4,-1,2,1,-5,4]", "output": "6 (subarray [4,-1,2,1])"}]),
            "Time: O(N), Space: O(1)",
            """def maxSubArray(nums: list[int]) -> int:
    max_sum = nums[0]
    current_sum = 0
    for num in nums:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    return max_sum""",
            "https://leetcode.com/problems/maximum-subarray/",
            "https://www.geeksforgeeks.org/largest-sum-contiguous-subarray/",
            json.dumps(["Amazon", "Microsoft", "TCS Digital", "Infosys SP", "Adobe"])
        ),
        (
            topic_map["arrays-hashing"],
            "Next Permutation",
            "Medium",
            "A permutation of an array of integers is an arrangement of its members into a sequence. Find the next lexicographically greater permutation of numbers in-place.",
            "1 <= nums.length <= 100",
            json.dumps([{"input": "nums = [1,2,3]", "output": "[1,3,2]"}, {"input": "nums = [3,2,1]", "output": "[1,2,3]"}]),
            "Time: O(N), Space: O(1)",
            """def nextPermutation(nums: list[int]) -> None:
    # 1. Find pivot from right
    i = len(nums) - 2
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1
    if i >= 0:
        # 2. Find successor
        j = len(nums) - 1
        while nums[j] <= nums[i]:
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]
    # 3. Reverse suffix
    nums[i + 1:] = reversed(nums[i + 1:])""",
            "https://leetcode.com/problems/next-permutation/",
            "https://www.geeksforgeeks.org/next-permutation/",
            json.dumps(["Google", "Atlassian", "Uber", "Amazon"])
        ),
        (
            topic_map["arrays-hashing"],
            "Trapping Rain Water",
            "Hard",
            "Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.",
            "n == height.length, 1 <= n <= 2 * 10^4",
            json.dumps([{"input": "height = [0,1,0,2,1,0,1,3,2,1,2,1]", "output": "6"}]),
            "Time: O(N), Space: O(1) Two Pointers",
            """def trap(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    left_max, right_max = 0, 0
    trapped_water = 0
    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                trapped_water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                trapped_water += right_max - height[right]
            right -= 1
    return trapped_water""",
            "https://leetcode.com/problems/trapping-rain-water/",
            "https://www.geeksforgeeks.org/trapping-rain-water/",
            json.dumps(["Google", "Microsoft", "Amazon", "Swiggy"])
        ),

        # Strings
        (
            topic_map["strings"],
            "Longest Substring Without Repeating Characters",
            "Medium",
            "Given a string s, find the length of the longest substring without repeating characters.",
            "0 <= s.length <= 5 * 10^4",
            json.dumps([{"input": "s = 'abcabcbb'", "output": "3 ('abc')"}, {"input": "s = 'bbbbb'", "output": "1 ('b')"}]),
            "Time: O(N), Space: O(min(N, M)) Sliding Window",
            """def lengthOfLongestSubstring(s: str) -> int:
    char_map = {}
    left = 0
    max_len = 0
    for right, char in enumerate(s):
        if char in char_map and char_map[char] >= left:
            left = char_map[char] + 1
        char_map[char] = right
        max_len = max(max_len, right - left + 1)
    return max_len""",
            "https://leetcode.com/problems/longest-substring-without-repeating-characters/",
            "https://www.geeksforgeeks.org/length-of-the-longest-substring-without-repeating-characters/",
            json.dumps(["Amazon", "Microsoft", "Google", "Infosys"])
        ),
        (
            topic_map["strings"],
            "Valid Anagram",
            "Easy",
            "Given two strings s and t, return true if t is an anagram of s, and false otherwise.",
            "1 <= s.length, t.length <= 5 * 10^4",
            json.dumps([{"input": "s = 'anagram', t = 'nagaram'", "output": "true"}, {"input": "s = 'rat', t = 'car'", "output": "false"}]),
            "Time: O(N), Space: O(1) [26 characters]",
            """def isAnagram(s: str, t: str) -> bool:
    if len(s) != len(t): return False
    count = [0] * 26
    for c1, c2 in zip(s, t):
        count[ord(c1) - ord('a')] += 1
        count[ord(c2) - ord('a')] -= 1
    return all(c == 0 for c in count)""",
            "https://leetcode.com/problems/valid-anagram/",
            "https://www.geeksforgeeks.org/check-whether-two-strings-are-anagram-of-each-other/",
            json.dumps(["Accenture", "TCS", "Cognizant", "Uber"])
        ),

        # Linked Lists
        (
            topic_map["linked-lists"],
            "Reverse a Linked List",
            "Easy",
            "Given the head of a singly linked list, reverse the list, and return the reversed list head.",
            "Number of nodes in list is [0, 5000]",
            json.dumps([{"input": "head = [1,2,3,4,5]", "output": "[5,4,3,2,1]"}]),
            "Time: O(N), Space: O(1)",
            """def reverseList(head):
    prev = None
    curr = head
    while curr:
        next_temp = curr.next
        curr.next = prev
        prev = curr
        curr = next_temp
    return prev""",
            "https://leetcode.com/problems/reverse-linked-list/",
            "https://www.geeksforgeeks.org/reverse-a-linked-list/",
            json.dumps(["Microsoft", "Amazon", "Infosys", "TCS"])
        ),
        (
            topic_map["linked-lists"],
            "LRU Cache",
            "Medium",
            "Design a data structure that follows the constraints of a Least Recently Used (LRU) cache with O(1) get and put operations.",
            "capacity <= 3000, at most 2 * 10^5 calls to get and put",
            json.dumps([{"input": "LRUCache(2); put(1,1); put(2,2); get(1) -> 1; put(3,3); get(2) -> -1", "output": "Evicts key 2"}]),
            "Time: O(1) for both get and put, Space: O(capacity)",
            """class Node:
    def __init__(self, key=0, val=0):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {}
        self.head, self.tail = Node(), Node()
        self.head.next, self.tail.prev = self.tail, self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add(node)
            return node.val
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        node = Node(key, value)
        self.cache[key] = node
        self._add(node)
        if len(self.cache) > self.cap:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]""",
            "https://leetcode.com/problems/lru-cache/",
            "https://www.geeksforgeeks.org/lru-cache-implementation/",
            json.dumps(["Google", "Amazon", "Microsoft", "Atlassian", "Uber"])
        ),

        # Stacks & Queues
        (
            topic_map["stacks-queues"],
            "Valid Parentheses",
            "Easy",
            "Given a string s containing '(', ')', '{', '}', '[' and ']', determine if the input string is valid.",
            "1 <= s.length <= 10^4",
            json.dumps([{"input": "s = '()[]{}'", "output": "true"}, {"input": "s = '(]'", "output": "false"}]),
            "Time: O(N), Space: O(N)",
            """def isValid(s: str) -> bool:
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    for char in s:
        if char in mapping:
            top = stack.pop() if stack else '#'
            if mapping[char] != top:
                return False
        else:
            stack.append(char)
    return not stack""",
            "https://leetcode.com/problems/valid-parentheses/",
            "https://www.geeksforgeeks.org/check-for-balanced-parentheses-in-an-expression/",
            json.dumps(["Google", "Amazon", "Infosys", "Accenture"])
        ),

        # Trees & BST
        (
            topic_map["trees-bst"],
            "Lowest Common Ancestor of a Binary Tree",
            "Medium",
            "Given a binary tree, find the lowest common ancestor (LCA) of two given nodes p and q.",
            "Number of nodes [2, 10^5], All Node.val are unique",
            json.dumps([{"input": "root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1", "output": "3"}]),
            "Time: O(N), Space: O(H) where H is tree height",
            """def lowestCommonAncestor(root, p, q):
    if not root or root == p or root == q:
        return root
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)
    if left and right:
        return root
    return left if left else right""",
            "https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/",
            "https://www.geeksforgeeks.org/lowest-common-ancestor-binary-tree-set-1/",
            json.dumps(["Microsoft", "Amazon", "Facebook", "Google"])
        ),

        # Graphs
        (
            topic_map["graphs"],
            "Number of Islands",
            "Medium",
            "Given an m x n 2D binary grid grid which represents a map of '1's (land) and '0's (water), return the number of islands.",
            "m == grid.length, n == grid[i].length, 1 <= m, n <= 300",
            json.dumps([{"input": "grid with 4 connected components", "output": "1"}]),
            "Time: O(M * N), Space: O(M * N) BFS/DFS",
            """def numIslands(grid: list[list[str]]) -> int:
    if not grid: return 0
    m, n = len(grid), len(grid[0])
    count = 0
    def dfs(r, c):
        if r < 0 or r >= m or c < 0 or c >= n or grid[r][c] != '1':
            return
        grid[r][c] = '0'  # Mark visited
        dfs(r+1, c)
        dfs(r-1, c)
        dfs(r, c+1)
        dfs(r, c-1)
    for r in range(m):
        for c in range(n):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)
    return count""",
            "https://leetcode.com/problems/number-of-islands/",
            "https://www.geeksforgeeks.org/find-number-of-islands/",
            json.dumps(["Amazon", "Google", "Microsoft", "Uber"])
        ),

        # Dynamic Programming
        (
            topic_map["dynamic-programming"],
            "0/1 Knapsack Problem",
            "Medium",
            "Given N items each with specific weight and value, determine the maximum value that can be put in a knapsack of capacity W.",
            "1 <= N <= 1000, 1 <= W <= 1000",
            json.dumps([{"input": "weights = [1, 2, 3], values = [10, 15, 40], W = 6", "output": "65"}]),
            "Time: O(N * W), Space: O(W) with 1D optimization",
            """def knapsack(weights, values, W, n):
    dp = [0] * (W + 1)
    for i in range(n):
        for w in range(W, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    return dp[W]""",
            "https://www.geeksforgeeks.org/0-1-knapsack-problem-dp-10/",
            "https://www.geeksforgeeks.org/0-1-knapsack-problem-dp-10/",
            json.dumps(["Amazon", "Microsoft", "Infosys SP", "TCS Prime"])
        ),
        (
            topic_map["dynamic-programming"],
            "Coin Change",
            "Medium",
            "You are given an integer array coins representing coins of different denominations and an integer amount. Return the fewest number of coins that you need to make up that amount.",
            "1 <= coins.length <= 12, 0 <= amount <= 10^4",
            json.dumps([{"input": "coins = [1,2,5], amount = 11", "output": "3 (5 + 5 + 1)"}]),
            "Time: O(amount * len(coins)), Space: O(amount)",
            """def coinChange(coins: list[int], amount: int) -> int:
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1""",
            "https://leetcode.com/problems/coin-change/",
            "https://www.geeksforgeeks.org/coin-change-dp-7/",
            json.dumps(["Amazon", "Microsoft", "Paytm", "Flipkart"])
        )
    ]

    for p in dsa_problems:
        cursor.execute('''
        INSERT INTO dsa_problems (
            topic_id, title, difficulty, problem_statement, constraints,
            examples, optimal_complexity, solution_code, leetcode_url, gfg_url, company_tags
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', p)

    conn.commit()
    conn.close()
    print("Database seeded with high-quality career & preparation data successfully!")

if __name__ == '__main__':
    seed()
