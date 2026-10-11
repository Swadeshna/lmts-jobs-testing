// CareerLaunch Single Page Application Logic

(function () {
  'use strict';

  // --- Global App State ---
  const state = {
    theme: localStorage.getItem('career_theme') || 'dark',
    currentUser: JSON.parse(localStorage.getItem('lmt_user') || 'null'),
    activeTab: 'home-tab',
    activePrepCategory: 'aptitude',
    activeDsaTopicId: 'all',
    
    // Data stores
    jobs: [],
    bookmarks: JSON.parse(localStorage.getItem('career_bookmarks') || '[]'),
    applications: JSON.parse(localStorage.getItem('career_applications') || '[]'),
    companies: [],
    prepMaterials: [],
    prepQuestions: [],
    dsaTopics: [],
    dsaProblems: [],
    userDsaProgress: JSON.parse(localStorage.getItem('career_dsa_progress') || '{}'), // { [problemId]: { status, is_starred, notes } }

    // Quiz state
    currentQuizIndex: 0,
    filteredQuizQuestions: [],
    quizScore: 0,

    // Filters
    jobSearchQuery: '',
    jobTypeFilter: '',
    jobExpFilter: '',
    bookmarksOnly: false,

    companySearchQuery: '',
    companyTierFilter: '',

    dsaSearchQuery: '',
    dsaDiffFilter: '',
    dsaStatusFilter: ''
  };

  // --- API / Data Loader ---
  async function loadInitialData() {
    // Apply theme
    applyTheme(state.theme);

    // Try fetching from API server first
    try {
      const [jobsRes, compRes, prepRes, questRes, dsaTopicsRes, dsaProbsRes] = await Promise.all([
        fetch('/api/jobs').then(r => r.json()).catch(() => null),
        fetch('/api/companies').then(r => r.json()).catch(() => null),
        fetch('/api/prep').then(r => r.json()).catch(() => null),
        fetch('/api/prep/questions').then(r => r.json()).catch(() => null),
        fetch('/api/dsa/topics').then(r => r.json()).catch(() => null),
        fetch('/api/dsa/problems').then(r => r.json()).catch(() => null),
      ]);

      if (jobsRes && jobsRes.jobs) state.jobs = jobsRes.jobs;
      else state.jobs = window.PORTAL_DATA.jobs;

      if (compRes && compRes.companies) state.companies = compRes.companies;
      else state.companies = window.PORTAL_DATA.companies;

      if (prepRes && prepRes.materials) state.prepMaterials = prepRes.materials;
      else state.prepMaterials = window.PORTAL_DATA.prep_materials;

      if (questRes && questRes.questions) state.prepQuestions = questRes.questions;
      else state.prepQuestions = window.PORTAL_DATA.prep_questions;

      if (dsaTopicsRes && dsaTopicsRes.topics) state.dsaTopics = dsaTopicsRes.topics;
      else state.dsaTopics = window.PORTAL_DATA.dsa_topics;

      if (dsaProbsRes && dsaProbsRes.problems) state.dsaProblems = dsaProbsRes.problems;
      else state.dsaProblems = window.PORTAL_DATA.dsa_problems;

      // Sync DSA local progress into problem list
      syncDsaProgressToState();

    } catch (err) {
      console.warn('API error, falling back to local dataset', err);
      state.jobs = window.PORTAL_DATA.jobs;
      state.companies = window.PORTAL_DATA.companies;
      state.prepMaterials = window.PORTAL_DATA.prep_materials;
      state.prepQuestions = window.PORTAL_DATA.prep_questions;
      state.dsaTopics = window.PORTAL_DATA.dsa_topics;
      state.dsaProblems = window.PORTAL_DATA.dsa_problems;
      syncDsaProgressToState();
    }

    renderAll();
    setupEventListeners();
  }

  function syncDsaProgressToState() {
    state.dsaProblems.forEach(p => {
      const saved = state.userDsaProgress[p.id];
      if (saved) {
        p.user_status = saved.status || p.user_status || 'unsolved';
        p.is_starred = saved.is_starred !== undefined ? saved.is_starred : (p.is_starred || 0);
        p.user_notes = saved.notes || p.user_notes || '';
      }
    });
  }

  function saveDsaProgress(problemId, status, isStarred, notes) {
    if (!state.userDsaProgress[problemId]) {
      state.userDsaProgress[problemId] = {};
    }
    if (status !== undefined) state.userDsaProgress[problemId].status = status;
    if (isStarred !== undefined) state.userDsaProgress[problemId].is_starred = isStarred;
    if (notes !== undefined) state.userDsaProgress[problemId].notes = notes;

    localStorage.setItem('career_dsa_progress', JSON.stringify(state.userDsaProgress));

    // Also notify backend if online
    fetch('/api/dsa/status', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        problem_id: problemId,
        status: status,
        is_starred: isStarred,
        user_notes: notes
      })
    }).catch(() => {});
  }

  // --- Theme Controller ---
  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    state.theme = theme;
    localStorage.setItem('career_theme', theme);

    const icon = document.getElementById('themeIcon');
    const label = document.getElementById('themeLabel');
    if (icon) {
      icon.innerText = theme === 'light' ? '☀️' : '🌙';
    }
    if (label) {
      label.innerText = theme === 'light' ? 'Light Mode' : 'Dark Mode';
    }
  }

  // --- Authentication Controller ---
  function renderAuthUI() {
    const container = document.getElementById('authNavContainer');
    if (!container) return;

    if (state.currentUser) {
      const initial = (state.currentUser.name || 'U').charAt(0).toUpperCase();
      container.innerHTML = `
        <div class="user-badge">
          <div class="user-badge-avatar">${escapeHtml(initial)}</div>
          <span>${escapeHtml(state.currentUser.name.split(' ')[0])}</span>
          <span style="font-size:0.7rem; color:var(--accent-primary);">(${escapeHtml(state.currentUser.role || 'User')})</span>
          <button class="signout-btn" onclick="window.signOut()" title="Sign Out">Logout</button>
        </div>
      `;
    } else {
      container.innerHTML = `
        <button class="signin-btn" id="openSignInModalBtn" onclick="openModal('signInModal')">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg>
          Sign In
        </button>
      `;
    }
  }

  window.demoSignIn = function (type) {
    if (type === 'candidate') {
      state.currentUser = {
        name: 'Swadeshna Ray',
        email: 'swadeshna@lmtjobs.com',
        role: 'Candidate'
      };
    } else {
      state.currentUser = {
        name: 'Alex Morgan',
        email: 'alex.recruiter@lmtjobs.com',
        role: 'Recruiter'
      };
    }
    localStorage.setItem('lmt_user', JSON.stringify(state.currentUser));
    renderAuthUI();
    closeModal('signInModal');
    showToast(`👋 Welcome back, ${state.currentUser.name}!`);
  };

  window.signOut = function () {
    state.currentUser = null;
    localStorage.removeItem('lmt_user');
    renderAuthUI();
    showToast('👋 Signed out of LMT Jobs');
  };

  // --- Render All Sections ---
  function renderAll() {
    renderAuthUI();
    renderHome();
    renderJobs();
    renderPrepMaterials();
    renderQuiz();
    renderCompanies();
    renderDsaTopicChips();
    renderDsaProblems();
    renderDashboard();
    updateStatsCounter();
  }

  function updateStatsCounter() {
    const jobsCountEl = document.getElementById('statsJobsCount');
    if (jobsCountEl) jobsCountEl.innerText = `${state.jobs.length}+`;

    const compCountEl = document.getElementById('statsCompaniesCount');
    if (compCountEl) compCountEl.innerText = `${state.companies.length}+ Blueprints`;
  }

  // --- 0. HOME PAGE SPOTLIGHT RENDERING ---
  function renderHome() {
    const jobsEl = document.getElementById('homeFeaturedJobsGrid');
    if (jobsEl) {
      const topJobs = state.jobs.slice(0, 3);
      jobsEl.innerHTML = topJobs.map(job => {
        const isBookmarked = state.bookmarks.includes(job.id);
        const isApplied = state.applications.some(a => a.job_id === job.id);
        return `
          <div class="job-card" data-job-id="${job.id}">
            <div class="job-header">
              <img src="${job.company_logo || 'https://via.placeholder.com/44'}" alt="${job.company}" class="company-logo" onerror="this.src='https://via.placeholder.com/44?text=${encodeURIComponent(job.company.substring(0,2))}'">
              <div class="job-info">
                <h3 class="job-title">${escapeHtml(job.title)}</h3>
                <div class="job-company">${escapeHtml(job.company)} • ${escapeHtml(job.location)}</div>
              </div>
              <button class="bookmark-btn ${isBookmarked ? 'active' : ''}" onclick="window.toggleJobBookmark(${job.id})">
                ${isBookmarked ? '★' : '☆'}
              </button>
            </div>
            <div class="job-meta-row">
              <span class="job-salary">${escapeHtml(job.salary)}</span>
              <span>•</span>
              <span class="job-meta-item">💼 ${escapeHtml(job.experience)}</span>
              <span>•</span>
              <span class="job-meta-item">🏷️ ${escapeHtml(job.job_type)}</span>
            </div>
            <p class="job-desc">${escapeHtml(job.description)}</p>
            <div class="skills-tags">
              ${(job.skills || []).slice(0, 3).map(skill => `<span class="skill-tag">${escapeHtml(skill)}</span>`).join('')}
            </div>
            <div class="job-footer">
              <span class="job-eligibility-badge">${escapeHtml(job.eligibility ? job.eligibility.split(',')[0] : 'Freshers Eligible')}</span>
              <div class="job-actions">
                <button class="btn-secondary" onclick="window.showJobDetail(${job.id})">Details</button>
                ${isApplied ? `
                  <button class="btn-secondary" style="color:var(--accent-emerald);" disabled>✓ Applied</button>
                ` : `
                  <button class="btn-primary" onclick="window.openApplyModal(${job.id})">Quick Apply</button>
                `}
              </div>
            </div>
          </div>
        `;
      }).join('');
    }

    const compEl = document.getElementById('homeFeaturedCompaniesGrid');
    if (compEl) {
      const topComps = state.companies.slice(0, 3);
      compEl.innerHTML = topComps.map(c => `
        <div class="company-card">
          <div class="company-card-top">
            <img src="${c.logo}" alt="${c.name}" class="company-card-logo" onerror="this.src='https://via.placeholder.com/50?text=${encodeURIComponent(c.name.substring(0,2))}'">
            <div style="flex:1;">
              <div style="display:flex; align-items:center; justify-content:space-between;">
                <h3 class="company-name">${escapeHtml(c.name)}</h3>
                <span class="company-tier-badge">${escapeHtml(c.tier)}</span>
              </div>
              <div style="font-size:0.8rem; color:var(--text-dim);">${escapeHtml(c.category)}</div>
            </div>
          </div>
          <div class="company-highlight-row">
            <div class="highlight-box">
              <span class="highlight-lbl">Fresher CTC Package</span>
              <span class="highlight-val" style="color:var(--accent-emerald);">${escapeHtml(c.package_range)}</span>
            </div>
            <div class="highlight-box">
              <span class="highlight-lbl">Cutoff</span>
              <span class="highlight-val">${escapeHtml(c.eligibility_cgpa.split('(')[0].trim())}</span>
            </div>
          </div>
          <button class="btn-primary" style="margin-top:auto;" onclick="window.showCompanyDetail('${c.slug}')">View Blueprint →</button>
        </div>
      `).join('');
    }
  }

  // --- 1. JOB PORTAL RENDERING ---
  function renderJobs() {
    const container = document.getElementById('jobsGrid');
    if (!container) return;

    let filtered = state.jobs.filter(job => {
      const matchQ = !state.jobSearchQuery || 
        job.title.toLowerCase().includes(state.jobSearchQuery.toLowerCase()) ||
        job.company.toLowerCase().includes(state.jobSearchQuery.toLowerCase()) ||
        job.skills.some(s => s.toLowerCase().includes(state.jobSearchQuery.toLowerCase())) ||
        job.location.toLowerCase().includes(state.jobSearchQuery.toLowerCase());

      const matchType = !state.jobTypeFilter || job.job_type === state.jobTypeFilter;
      const matchExp = !state.jobExpFilter || job.experience.toLowerCase().includes(state.jobExpFilter.toLowerCase());
      const matchBookmark = !state.bookmarksOnly || state.bookmarks.includes(job.id);

      return matchQ && matchType && matchExp && matchBookmark;
    });

    if (filtered.length === 0) {
      container.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; padding: 3rem; background: var(--bg-card); border-radius: var(--radius-md); border: 1px solid var(--border-color);">
          <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔍</div>
          <h3 style="font-size: 1.15rem; font-weight: 700; margin-bottom: 0.35rem;">No openings found matching your criteria</h3>
          <p style="color: var(--text-muted); font-size: 0.875rem;">Try modifying your keyword search or resetting the job type/experience filters.</p>
        </div>
      `;
      return;
    }

    container.innerHTML = filtered.map(job => {
      const isBookmarked = state.bookmarks.includes(job.id);
      const isApplied = state.applications.some(a => a.job_id === job.id);

      return `
        <div class="job-card" data-job-id="${job.id}">
          <div class="job-header">
            <img src="${job.company_logo || 'https://via.placeholder.com/44'}" alt="${job.company}" class="company-logo" onerror="this.src='https://via.placeholder.com/44?text=${encodeURIComponent(job.company.substring(0,2))}'">
            <div class="job-info">
              <h3 class="job-title">${escapeHtml(job.title)}</h3>
              <div class="job-company">${escapeHtml(job.company)} • ${escapeHtml(job.location)}</div>
            </div>
            <button class="bookmark-btn ${isBookmarked ? 'active' : ''}" onclick="window.toggleJobBookmark(${job.id})" title="${isBookmarked ? 'Remove Bookmark' : 'Save Job'}">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="${isBookmarked ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            </button>
          </div>

          <div class="job-meta-row">
            <span class="job-salary">${escapeHtml(job.salary)}</span>
            <span>•</span>
            <span class="job-meta-item">💼 ${escapeHtml(job.experience)}</span>
            <span>•</span>
            <span class="job-meta-item">🏷️ ${escapeHtml(job.job_type)}</span>
          </div>

          <p class="job-desc">${escapeHtml(job.description)}</p>

          <div class="skills-tags">
            ${(job.skills || []).slice(0, 4).map(skill => `<span class="skill-tag">${escapeHtml(skill)}</span>`).join('')}
            ${(job.skills && job.skills.length > 4) ? `<span class="skill-tag">+${job.skills.length - 4} more</span>` : ''}
          </div>

          <div class="job-footer">
            <span class="job-eligibility-badge">${escapeHtml(job.eligibility ? job.eligibility.split(',')[0] : 'Open to Batch 2025/2026')}</span>
            <div class="job-actions">
              <button class="btn-secondary" onclick="window.showJobDetail(${job.id})">Details</button>
              ${isApplied ? `
                <button class="btn-secondary" style="color:var(--accent-emerald); border-color:var(--accent-emerald);" disabled>✓ Applied</button>
              ` : `
                <button class="btn-primary" onclick="window.openApplyModal(${job.id})">Quick Apply</button>
              `}
            </div>
          </div>
        </div>
      `;
    }).join('');
  }

  window.toggleJobBookmark = function (jobId) {
    const idx = state.bookmarks.indexOf(jobId);
    if (idx > -1) {
      state.bookmarks.splice(idx, 1);
      showToast('Removed from saved jobs');
    } else {
      state.bookmarks.push(jobId);
      showToast('⭐ Job saved to bookmarks');
    }
    localStorage.setItem('career_bookmarks', JSON.stringify(state.bookmarks));

    fetch('/api/bookmarks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ job_id: jobId })
    }).catch(() => {});

    renderJobs();
    renderDashboard();
  };

  window.showJobDetail = function (jobId) {
    const job = state.jobs.find(j => j.id === jobId);
    if (!job) return;

    const modalContent = document.getElementById('jobDetailContent');
    const isApplied = state.applications.some(a => a.job_id === job.id);

    modalContent.innerHTML = `
      <div style="display:flex; align-items:center; gap:1rem; margin-bottom:1.25rem;">
        <img src="${job.company_logo}" alt="${job.company}" class="company-logo" style="width:56px; height:56px;" onerror="this.src='https://via.placeholder.com/56'">
        <div>
          <h2 style="font-size:1.35rem; font-weight:700;">${escapeHtml(job.title)}</h2>
          <div style="color:var(--text-muted); font-size:0.9rem;">${escapeHtml(job.company)} • ${escapeHtml(job.location)}</div>
        </div>
      </div>

      <div style="display:flex; flex-wrap:wrap; gap:0.75rem; background:var(--bg-secondary); padding:0.85rem; border-radius:var(--radius-sm); margin-bottom:1.25rem; font-size:0.85rem;">
        <div><strong>Package:</strong> <span style="color:var(--accent-emerald); font-weight:700;">${escapeHtml(job.salary)}</span></div>
        <div>•</div>
        <div><strong>Experience:</strong> ${escapeHtml(job.experience)}</div>
        <div>•</div>
        <div><strong>Job Type:</strong> ${escapeHtml(job.job_type)}</div>
        <div>•</div>
        <div><strong>Deadline:</strong> ${escapeHtml(job.deadline || 'Rolling')}</div>
      </div>

      <h4 style="font-size:0.95rem; font-weight:700; margin-bottom:0.4rem;">Role Overview</h4>
      <p style="font-size:0.875rem; color:var(--text-muted); margin-bottom:1rem; line-height:1.5;">${escapeHtml(job.description)}</p>

      <h4 style="font-size:0.95rem; font-weight:700; margin-bottom:0.4rem;">Key Requirements</h4>
      <p style="font-size:0.875rem; color:var(--text-muted); margin-bottom:1rem; line-height:1.5;">${escapeHtml(job.requirements)}</p>

      <h4 style="font-size:0.95rem; font-weight:700; margin-bottom:0.4rem;">Eligibility Criteria</h4>
      <p style="font-size:0.875rem; color:var(--text-muted); margin-bottom:1.25rem; line-height:1.5;">${escapeHtml(job.eligibility)}</p>

      <div style="margin-bottom:1.5rem;">
        <h4 style="font-size:0.95rem; font-weight:700; margin-bottom:0.4rem;">Required Tech Stack</h4>
        <div class="skills-tags">
          ${(job.skills || []).map(s => `<span class="skill-tag" style="background:rgba(59,130,246,0.1); color:#60a5fa;">${escapeHtml(s)}</span>`).join('')}
        </div>
      </div>

      <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid var(--border-color); padding-top:1rem;">
        <a href="${job.apply_url || '#'}" target="_blank" rel="noopener noreferrer" class="btn-secondary" style="display:flex; align-items:center; gap:0.4rem;">
          <span>Official Careers Site ↗</span>
        </a>
        <div style="display:flex; gap:0.6rem;">
          <button class="btn-secondary" onclick="closeModal('jobDetailModal')">Close</button>
          ${isApplied ? `
            <button class="btn-secondary" style="color:var(--accent-emerald);" disabled>Application Already Submitted</button>
          ` : `
            <button class="btn-primary" onclick="closeModal('jobDetailModal'); window.openApplyModal(${job.id});">Apply Now</button>
          `}
        </div>
      </div>
    `;

    openModal('jobDetailModal');
  };

  window.openApplyModal = function (jobId) {
    const job = state.jobs.find(j => j.id === jobId);
    if (!job) return;

    document.getElementById('applyJobId').value = job.id;
    document.getElementById('applyModalJobTitle').innerText = `Apply: ${job.title}`;
    document.getElementById('applyModalCompany').innerText = `${job.company} • ${job.location}`;

    if (state.currentUser) {
      const nameInput = document.getElementById('applicantName');
      const emailInput = document.getElementById('applicantEmail');
      if (nameInput) nameInput.value = state.currentUser.name;
      if (emailInput) emailInput.value = state.currentUser.email;
    }

    openModal('applyModal');
  };

  // --- 2. PREPARATION HUB RENDERING ---
  function renderPrepMaterials() {
    const container = document.getElementById('prepNotesContainer');
    if (!container) return;

    const materials = state.prepMaterials.filter(m => m.category === state.activePrepCategory);

    if (materials.length === 0) {
      container.innerHTML = `<p style="color:var(--text-muted); padding:2rem;">No study materials found for this section.</p>`;
      return;
    }

    container.innerHTML = materials.map(mat => `
      <div class="note-card">
        <div class="note-header">
          <span class="note-tag">${escapeHtml(mat.subcategory)}</span>
          <span class="note-time">⏱️ ${escapeHtml(mat.read_time)}</span>
        </div>
        <h3 class="note-title">${escapeHtml(mat.title)}</h3>
        <p class="note-summary">${escapeHtml(mat.summary)}</p>

        <div class="note-content-rendered">
          ${renderMarkdown(mat.content_markdown)}
        </div>

        <div class="key-takeaways">
          <div class="key-takeaways-title">Key Placement Takeaways</div>
          <ul>
            ${(mat.key_takeaways || []).map(k => `<li>${escapeHtml(k)}</li>`).join('')}
          </ul>
        </div>
      </div>
    `).join('');
  }

  function renderQuiz() {
    const container = document.getElementById('quizContainer');
    if (!container) return;

    state.filteredQuizQuestions = state.prepQuestions.filter(q => q.category === state.activePrepCategory);
    if (state.filteredQuizQuestions.length === 0) {
      state.filteredQuizQuestions = state.prepQuestions;
    }

    if (state.currentQuizIndex >= state.filteredQuizQuestions.length) {
      state.currentQuizIndex = 0;
    }

    const q = state.filteredQuizQuestions[state.currentQuizIndex];
    if (!q) {
      container.innerHTML = `<p style="color:var(--text-muted);">No quiz questions currently available.</p>`;
      return;
    }

    container.innerHTML = `
      <div class="quiz-card">
        <div style="display:flex; justify-content:space-between; margin-bottom:0.6rem; font-size:0.75rem; color:var(--text-dim);">
          <span>Question ${state.currentQuizIndex + 1} of ${state.filteredQuizQuestions.length}</span>
          <span class="diff-badge ${q.difficulty === 'Easy' ? 'diff-easy' : 'diff-medium'}">${escapeHtml(q.difficulty)}</span>
        </div>
        <div class="question-text">${escapeHtml(q.question)}</div>

        <div class="options-list" id="quizOptionsList">
          ${(q.options || []).map((opt, idx) => `
            <button class="option-btn" onclick="window.checkQuizAnswer(${idx}, ${q.correct_index})">
              <strong>${String.fromCharCode(65 + idx)}.</strong> ${escapeHtml(opt)}
            </button>
          `).join('')}
        </div>

        <div id="quizExplanation" class="explanation-box">
          <div style="font-weight:700; margin-bottom:0.25rem; color:var(--text-main);">Explanation:</div>
          <div>${escapeHtml(q.explanation)}</div>
          <div style="margin-top:0.5rem; display:flex; flex-wrap:wrap; gap:0.3rem;">
            ${(q.company_tags || []).map(tag => `<span class="company-tag-pill">${escapeHtml(tag)}</span>`).join('')}
          </div>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:0.85rem;">
          <span style="font-size:0.75rem; color:var(--text-dim);">Score: ${state.quizScore}</span>
          <button class="btn-secondary" style="font-size:0.75rem; padding:0.35rem 0.65rem;" onclick="window.nextQuizQuestion()">Next Question →</button>
        </div>
      </div>
    `;
  }

  window.checkQuizAnswer = function (selectedIdx, correctIdx) {
    const options = document.querySelectorAll('#quizOptionsList .option-btn');
    options.forEach((btn, idx) => {
      btn.disabled = true;
      if (idx === correctIdx) {
        btn.classList.add('correct');
      } else if (idx === selectedIdx) {
        btn.classList.add('wrong');
      }
    });

    if (selectedIdx === correctIdx) {
      state.quizScore += 10;
      showToast('🎉 Correct Answer! +10 Points');
    } else {
      showToast('❌ Incorrect. Review explanation below.');
    }

    const expEl = document.getElementById('quizExplanation');
    if (expEl) expEl.style.display = 'block';
  };

  window.nextQuizQuestion = function () {
    state.currentQuizIndex = (state.currentQuizIndex + 1) % state.filteredQuizQuestions.length;
    renderQuiz();
  };

  // --- 3. COMPANIES HIRING PROCESS RENDERING ---
  function renderCompanies() {
    const container = document.getElementById('companiesGrid');
    if (!container) return;

    let filtered = state.companies.filter(c => {
      const matchQ = !state.companySearchQuery || 
        c.name.toLowerCase().includes(state.companySearchQuery.toLowerCase()) ||
        c.description.toLowerCase().includes(state.companySearchQuery.toLowerCase());
      const matchTier = !state.companyTierFilter || c.tier.includes(state.companyTierFilter);
      return matchQ && matchTier;
    });

    container.innerHTML = filtered.map(c => `
      <div class="company-card">
        <div class="company-card-top">
          <img src="${c.logo}" alt="${c.name}" class="company-card-logo" onerror="this.src='https://via.placeholder.com/50?text=${encodeURIComponent(c.name.substring(0,2))}'">
          <div style="flex:1;">
            <div style="display:flex; align-items:center; justify-content:space-between;">
              <h3 class="company-name">${escapeHtml(c.name)}</h3>
              <span class="company-tier-badge">${escapeHtml(c.tier)}</span>
            </div>
            <div style="font-size:0.8rem; color:var(--text-dim);">${escapeHtml(c.category)}</div>
          </div>
        </div>

        <div class="company-highlight-row">
          <div class="highlight-box">
            <span class="highlight-lbl">Fresher CTC Package</span>
            <span class="highlight-val" style="color:var(--accent-emerald);">${escapeHtml(c.package_range)}</span>
          </div>
          <div class="highlight-box">
            <span class="highlight-lbl">Min Eligibility</span>
            <span class="highlight-val">${escapeHtml(c.eligibility_cgpa.split('(')[0].trim())}</span>
          </div>
        </div>

        <div style="margin-bottom:0.75rem;">
          <div style="font-size:0.75rem; text-transform:uppercase; color:var(--text-dim); font-weight:700; margin-bottom:0.4rem;">Selection Rounds Flow</div>
          <div class="rounds-timeline">
            ${(c.rounds_breakdown || []).slice(0, 3).map((r, i) => `
              <div class="round-step">
                <span class="round-bullet">${i + 1}</span>
                <span style="color:var(--text-muted); font-size:0.8rem;">${escapeHtml(r.round)}</span>
              </div>
            `).join('')}
            ${(c.rounds_breakdown && c.rounds_breakdown.length > 3) ? `
              <div class="round-step">
                <span class="round-bullet">+</span>
                <span style="color:var(--text-dim); font-size:0.75rem;">${c.rounds_breakdown.length - 3} more round(s)</span>
              </div>
            ` : ''}
          </div>
        </div>

        <div style="margin-top:auto; padding-top:0.75rem; border-top:1px solid var(--border-light); display:flex; justify-content:space-between; align-items:center;">
          <span style="font-size:0.75rem; color:var(--accent-cyan);">${escapeHtml(c.eligibility_batch)}</span>
          <button class="btn-primary" onclick="window.showCompanyDetail('${c.slug}')">Full Blueprint →</button>
        </div>
      </div>
    `).join('');
  }

  window.showCompanyDetail = function (slug) {
    const c = state.companies.find(item => item.slug === slug);
    if (!c) return;

    const modalContent = document.getElementById('companyDetailContent');
    modalContent.innerHTML = `
      <div style="display:flex; align-items:center; gap:1rem; margin-bottom:1.5rem; border-bottom:1px solid var(--border-color); padding-bottom:1rem;">
        <img src="${c.logo}" alt="${c.name}" class="company-card-logo" style="width:60px; height:60px;" onerror="this.src='https://via.placeholder.com/60'">
        <div>
          <div style="display:flex; align-items:center; gap:0.6rem;">
            <h2 style="font-size:1.5rem; font-weight:800;">${escapeHtml(c.name)}</h2>
            <span class="company-tier-badge">${escapeHtml(c.tier)}</span>
          </div>
          <p style="font-size:0.875rem; color:var(--text-muted);">${escapeHtml(c.description)}</p>
        </div>
      </div>

      <!-- Eligibility Card -->
      <div style="background:var(--bg-secondary); border:1px solid var(--border-color); border-radius:var(--radius-sm); padding:1rem; margin-bottom:1.25rem;">
        <h4 style="font-size:0.9rem; font-weight:700; color:var(--accent-primary); text-transform:uppercase; margin-bottom:0.5rem;">📋 Eligibility & Compensation</h4>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.75rem; font-size:0.85rem;">
          <div><strong>Package (CTC):</strong> <span style="color:var(--accent-emerald); font-weight:700;">${escapeHtml(c.package_range)}</span></div>
          <div><strong>Target Batches:</strong> ${escapeHtml(c.eligibility_batch)}</div>
          <div><strong>Academic Cutoff:</strong> ${escapeHtml(c.eligibility_cgpa)}</div>
          <div><strong>Allowed Branches:</strong> ${escapeHtml(c.eligibility_branches)}</div>
        </div>
      </div>

      <!-- Exam Pattern & Rounds -->
      <div style="margin-bottom:1.25rem;">
        <h4 style="font-size:0.95rem; font-weight:700; margin-bottom:0.6rem;">Exam Pattern & Selection Rounds</h4>
        <div style="background:rgba(59,130,246,0.06); border-left:3px solid var(--accent-primary); padding:0.75rem 1rem; border-radius:0 var(--radius-sm) var(--radius-sm) 0; margin-bottom:0.85rem; font-size:0.85rem;">
          <strong>Round 1 Assessment Structure:</strong> ${escapeHtml(c.exam_pattern.online_assessment || 'Online test')}
          <br><span style="color:var(--text-dim); font-size:0.78rem;">Elimination Rule: ${escapeHtml(c.exam_pattern.elimination || 'Sectional cutoffs')}</span>
        </div>

        <div style="display:flex; flex-direction:column; gap:0.6rem;">
          ${(c.rounds_breakdown || []).map((r, i) => `
            <div style="background:var(--bg-secondary); border:1px solid var(--border-color); border-radius:var(--radius-sm); padding:0.75rem 1rem;">
              <div style="font-weight:700; font-size:0.875rem; color:var(--text-main); margin-bottom:0.2rem;">${escapeHtml(r.round)}</div>
              <div style="font-size:0.8rem; color:var(--text-muted);">${escapeHtml(r.details)}</div>
            </div>
          `).join('')}
        </div>
      </div>

      <!-- Syllabus & Topics -->
      <div style="margin-bottom:1.25rem;">
        <h4 style="font-size:0.95rem; font-weight:700; margin-bottom:0.6rem;">Syllabus Breakdown & Weightage</h4>
        <div style="display:flex; gap:0.6rem; flex-wrap:wrap; margin-bottom:0.75rem;">
          ${Object.entries(c.syllabus || {}).filter(([k]) => k !== 'key_topics').map(([k, v]) => `
            <span class="skill-tag" style="background:rgba(139,92,246,0.15); color:#c084fc; font-weight:600;">${escapeHtml(k.replace('_', ' ').toUpperCase())}: ${escapeHtml(v)}</span>
          `).join('')}
        </div>
        <div style="font-size:0.8rem; color:var(--text-muted);">
          <strong>High-Frequency Topics:</strong> ${(c.syllabus.key_topics || []).join(', ')}
        </div>
      </div>

      <!-- Interview Tips & FAQs -->
      <div style="margin-bottom:1.5rem; background:rgba(16,185,129,0.06); border:1px solid rgba(16,185,129,0.25); border-radius:var(--radius-sm); padding:1rem;">
        <h4 style="font-size:0.9rem; font-weight:700; color:var(--accent-emerald); margin-bottom:0.4rem;">💡 Insider Interview Tips</h4>
        <div style="font-size:0.85rem; color:var(--text-main); white-space:pre-line; line-height:1.5;">${escapeHtml(c.interview_tips)}</div>
      </div>

      <div style="display:flex; justify-content:space-between; align-items:center;">
        <button class="btn-secondary" onclick="window.jumpToCompanyDsa('${c.name}')">🎯 Practice ${escapeHtml(c.name)} Questions in DSA Sheet</button>
        <button class="btn-primary" onclick="closeModal('companyDetailModal')">Done</button>
      </div>
    `;

    openModal('companyDetailModal');
  };

  window.jumpToCompanyDsa = function (companyName) {
    closeModal('companyDetailModal');
    switchTab('dsa-tab');
    state.dsaSearchQuery = companyName;
    const searchInput = document.getElementById('dsaSearchInput');
    if (searchInput) searchInput.value = companyName;
    renderDsaProblems();
  };

  // --- 4. DEDICATED DSA SHEET RENDERING ---
  function renderDsaTopicChips() {
    const container = document.getElementById('dsaTopicChips');
    if (!container) return;

    container.innerHTML = `
      <button class="topic-chip ${state.activeDsaTopicId === 'all' ? 'active' : ''}" onclick="window.filterDsaByTopic('all')">
        All Topics (${state.dsaProblems.length})
      </button>
      ${state.dsaTopics.map(t => {
        const count = state.dsaProblems.filter(p => p.topic_id === t.id).length;
        return `
          <button class="topic-chip ${state.activeDsaTopicId === t.id ? 'active' : ''}" onclick="window.filterDsaByTopic(${t.id})">
            ${escapeHtml(t.name)} (${count})
          </button>
        `;
      }).join('')}
    `;
  }

  window.filterDsaByTopic = function (topicId) {
    state.activeDsaTopicId = topicId;
    renderDsaTopicChips();
    renderDsaProblems();
  };

  function renderDsaProblems() {
    const tbody = document.getElementById('dsaProblemsTbody');
    if (!tbody) return;

    let filtered = state.dsaProblems.filter(p => {
      const matchTopic = state.activeDsaTopicId === 'all' || p.topic_id === state.activeDsaTopicId;
      const matchQ = !state.dsaSearchQuery || 
        p.title.toLowerCase().includes(state.dsaSearchQuery.toLowerCase()) ||
        p.company_tags.some(t => t.toLowerCase().includes(state.dsaSearchQuery.toLowerCase()));
      const matchDiff = !state.dsaDiffFilter || p.difficulty === state.dsaDiffFilter;
      
      let matchStatus = true;
      if (state.dsaStatusFilter === 'solved') matchStatus = p.user_status === 'solved';
      else if (state.dsaStatusFilter === 'unsolved') matchStatus = p.user_status !== 'solved';
      else if (state.dsaStatusFilter === 'starred') matchStatus = !!p.is_starred;

      return matchTopic && matchQ && matchDiff && matchStatus;
    });

    // Update Progress calculations
    const total = state.dsaProblems.length;
    const solved = state.dsaProblems.filter(p => p.user_status === 'solved').length;
    const pct = total > 0 ? Math.round((solved / total) * 100) : 0;

    const progFill = document.getElementById('dsaProgressBarFill');
    if (progFill) progFill.style.width = `${pct}%`;

    const progText = document.getElementById('dsaProgressPercentage');
    if (progText) progText.innerText = `${pct}% Completed (${solved}/${total} Solved)`;

    const easySolved = state.dsaProblems.filter(p => p.difficulty === 'Easy' && p.user_status === 'solved').length;
    const medSolved = state.dsaProblems.filter(p => p.difficulty === 'Medium' && p.user_status === 'solved').length;
    const hardSolved = state.dsaProblems.filter(p => p.difficulty === 'Hard' && p.user_status === 'solved').length;

    const eb = document.getElementById('easyCountBadge');
    if (eb) eb.innerText = `Easy: ${easySolved} Solved`;
    const mb = document.getElementById('medCountBadge');
    if (mb) mb.innerText = `Medium: ${medSolved} Solved`;
    const hb = document.getElementById('hardCountBadge');
    if (hb) hb.innerText = `Hard: ${hardSolved} Solved`;

    if (filtered.length === 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="7" style="text-align: center; padding: 2.5rem; color: var(--text-dim);">
            No DSA problems match your filter. Try selecting 'All Topics' or clearing the search query.
          </td>
        </tr>
      `;
      return;
    }

    tbody.innerHTML = filtered.map(p => {
      const isSolved = p.user_status === 'solved';
      const isStarred = !!p.is_starred;
      const diffClass = p.difficulty === 'Easy' ? 'diff-easy' : (p.difficulty === 'Medium' ? 'diff-medium' : 'diff-hard');

      return `
        <tr>
          <td style="text-align:center;">
            <input type="checkbox" class="status-checkbox" ${isSolved ? 'checked' : ''} onchange="window.toggleDsaProblemSolved(${p.id}, this.checked)">
          </td>
          <td style="text-align:center;">
            <button class="star-btn ${isStarred ? 'active' : ''}" onclick="window.toggleDsaProblemStar(${p.id})">
              ${isStarred ? '★' : '☆'}
            </button>
          </td>
          <td>
            <div style="font-weight:600; color: ${isSolved ? 'var(--text-dim)' : 'var(--text-main)'}; text-decoration: ${isSolved ? 'line-through' : 'none'};">
              ${escapeHtml(p.title)}
            </div>
            <div style="font-size:0.75rem; color:var(--text-dim);">${escapeHtml(p.optimal_complexity)}</div>
          </td>
          <td>
            <span class="skill-tag">${escapeHtml(p.topic_name || 'DSA')}</span>
          </td>
          <td>
            <span class="diff-badge ${diffClass}">${escapeHtml(p.difficulty)}</span>
          </td>
          <td>
            <div style="display:flex; flex-wrap:wrap; gap:0.25rem;">
              ${(p.company_tags || []).slice(0, 3).map(tag => `<span class="company-tag-pill">${escapeHtml(tag)}</span>`).join('')}
              ${(p.company_tags && p.company_tags.length > 3) ? `<span class="company-tag-pill">+${p.company_tags.length - 3}</span>` : ''}
            </div>
          </td>
          <td style="text-align:right;">
            <div style="display:inline-flex; gap:0.4rem;">
              ${p.leetcode_url ? `<a href="${p.leetcode_url}" target="_blank" rel="noopener noreferrer" class="btn-secondary" style="padding:0.25rem 0.5rem; font-size:0.75rem;" title="Practice on LeetCode">LeetCode ↗</a>` : ''}
              <button class="btn-primary" style="padding:0.25rem 0.65rem; font-size:0.75rem;" onclick="window.showDsaProblemDetail(${p.id})">Solution & Code</button>
            </div>
          </td>
        </tr>
      `;
    }).join('');
  }

  window.toggleDsaProblemSolved = function (problemId, checked) {
    const p = state.dsaProblems.find(item => item.id === problemId);
    if (!p) return;
    p.user_status = checked ? 'solved' : 'unsolved';
    saveDsaProgress(problemId, p.user_status, p.is_starred, p.user_notes);
    renderDsaProblems();
    renderDashboard();
    if (checked) showToast(`🎯 Solved: ${p.title}! Keep up the momentum!`);
  };

  window.toggleDsaProblemStar = function (problemId) {
    const p = state.dsaProblems.find(item => item.id === problemId);
    if (!p) return;
    p.is_starred = p.is_starred ? 0 : 1;
    saveDsaProgress(problemId, p.user_status, p.is_starred, p.user_notes);
    renderDsaProblems();
    showToast(p.is_starred ? '⭐ Added to revision list' : 'Removed from revision list');
  };

  window.showDsaProblemDetail = function (problemId) {
    const p = state.dsaProblems.find(item => item.id === problemId);
    if (!p) return;

    const modalContent = document.getElementById('dsaProblemDetailContent');
    const diffClass = p.difficulty === 'Easy' ? 'diff-easy' : (p.difficulty === 'Medium' ? 'diff-medium' : 'diff-hard');

    modalContent.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:1rem; border-bottom:1px solid var(--border-color); padding-bottom:0.75rem;">
        <div>
          <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:0.25rem;">
            <h2 style="font-size:1.35rem; font-weight:800;">${escapeHtml(p.title)}</h2>
            <span class="diff-badge ${diffClass}">${escapeHtml(p.difficulty)}</span>
          </div>
          <div style="font-size:0.8rem; color:var(--text-muted);">${escapeHtml(p.topic_name || 'DSA')} • ${escapeHtml(p.optimal_complexity)}</div>
        </div>
        <div style="display:flex; gap:0.4rem;">
          ${p.leetcode_url ? `<a href="${p.leetcode_url}" target="_blank" rel="noopener noreferrer" class="btn-secondary" style="font-size:0.8rem;">LeetCode ↗</a>` : ''}
          ${p.gfg_url ? `<a href="${p.gfg_url}" target="_blank" rel="noopener noreferrer" class="btn-secondary" style="font-size:0.8rem;">GFG ↗</a>` : ''}
        </div>
      </div>

      <!-- Problem Statement -->
      <h4 style="font-size:0.9rem; font-weight:700; margin-bottom:0.35rem;">Problem Description</h4>
      <p style="font-size:0.875rem; color:var(--text-main); margin-bottom:1rem; line-height:1.5;">${escapeHtml(p.problem_statement)}</p>

      <!-- Examples -->
      ${(p.examples && p.examples.length > 0) ? `
        <h4 style="font-size:0.9rem; font-weight:700; margin-bottom:0.35rem;">Examples & Constraints</h4>
        <div style="background:var(--bg-secondary); border:1px solid var(--border-color); border-radius:var(--radius-sm); padding:0.75rem 1rem; margin-bottom:1rem; font-size:0.8rem;">
          ${p.examples.map(ex => `
            <div style="margin-bottom:0.4rem;">
              <div><strong>Input:</strong> <code>${escapeHtml(ex.input)}</code></div>
              <div><strong>Output:</strong> <code>${escapeHtml(ex.output)}</code></div>
            </div>
          `).join('')}
          <div style="color:var(--text-dim); font-size:0.75rem; margin-top:0.4rem;"><strong>Constraints:</strong> ${escapeHtml(p.constraints || 'Standard limits')}</div>
        </div>
      ` : ''}

      <!-- Solution Code -->
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
        <h4 style="font-size:0.9rem; font-weight:700;">Optimal Python 3 Solution</h4>
        <button class="btn-secondary" style="font-size:0.75rem; padding:0.2rem 0.55rem;" onclick="window.copySolutionCode()">Copy Code</button>
      </div>
      <div class="note-content-rendered" style="margin-bottom:1rem;">
        <pre><code id="dsaSolutionCodeBlock">${escapeHtml(p.solution_code)}</code></pre>
      </div>

      <!-- Personal Notes -->
      <div class="form-group" style="margin-bottom:1.25rem;">
        <label class="form-label">My Revision Notes / Edge Cases</label>
        <textarea id="problemPersonalNotes" class="form-control" rows="2" placeholder="Write reminders, edge-cases or intuition for revision...">${escapeHtml(p.user_notes || '')}</textarea>
        <button class="btn-secondary" style="font-size:0.75rem; margin-top:0.4rem;" onclick="window.saveCurrentProblemNotes(${p.id})">Save Notes</button>
      </div>

      <div style="display:flex; justify-content:space-between; align-items:center;">
        <button class="btn-secondary" onclick="closeModal('dsaProblemModal')">Close</button>
        <button class="btn-primary" onclick="window.toggleDsaProblemSolved(${p.id}, true); closeModal('dsaProblemModal');">
          Mark as Solved ✓
        </button>
      </div>
    `;

    openModal('dsaProblemModal');
  };

  window.copySolutionCode = function () {
    const codeEl = document.getElementById('dsaSolutionCodeBlock');
    if (codeEl) {
      navigator.clipboard.writeText(codeEl.innerText).then(() => {
        showToast('📋 Code copied to clipboard!');
      }).catch(() => {});
    }
  };

  window.saveCurrentProblemNotes = function (problemId) {
    const notesEl = document.getElementById('problemPersonalNotes');
    if (!notesEl) return;
    const val = notesEl.value;
    const p = state.dsaProblems.find(item => item.id === problemId);
    if (p) p.user_notes = val;
    saveDsaProgress(problemId, p ? p.user_status : 'unsolved', p ? p.is_starred : 0, val);
    showToast('💾 Revision notes saved!');
  };

  // --- 5. DASHBOARD & TRACKER RENDERING ---
  function renderDashboard() {
    const appListEl = document.getElementById('applicationsList');
    const savedListEl = document.getElementById('savedJobsList');
    const appPill = document.getElementById('appliedCountPill');
    const savedPill = document.getElementById('savedCountPill');

    if (appPill) appPill.innerText = `${state.applications.length} Applied`;
    if (savedPill) savedPill.innerText = `${state.bookmarks.length} Saved`;

    if (appListEl) {
      if (state.applications.length === 0) {
        appListEl.innerHTML = `<p style="color:var(--text-dim); font-size:0.85rem;">No applications submitted yet. Browse jobs in the Job Portal tab and click "Quick Apply"!</p>`;
      } else {
        appListEl.innerHTML = state.applications.map(app => `
          <div style="background:var(--bg-secondary); border:1px solid var(--border-color); border-radius:var(--radius-sm); padding:0.85rem; display:flex; justify-content:space-between; align-items:center;">
            <div>
              <div style="font-weight:700; font-size:0.9rem;">${escapeHtml(app.job_title)}</div>
              <div style="font-size:0.8rem; color:var(--text-muted);">${escapeHtml(app.company_name)} • Applied: ${new Date(app.applied_at || Date.now()).toLocaleDateString()}</div>
            </div>
            <span class="diff-badge diff-easy" style="text-transform:uppercase;">${escapeHtml(app.status || 'Applied')}</span>
          </div>
        `).join('');
      }
    }

    if (savedListEl) {
      const bookmarkedJobs = state.jobs.filter(j => state.bookmarks.includes(j.id));
      if (bookmarkedJobs.length === 0) {
        savedListEl.innerHTML = `<p style="color:var(--text-dim); font-size:0.85rem;">No saved jobs. Click the star icon on any job card to bookmark it.</p>`;
      } else {
        savedListEl.innerHTML = bookmarkedJobs.map(j => `
          <div style="background:var(--bg-secondary); border:1px solid var(--border-color); border-radius:var(--radius-sm); padding:0.85rem; display:flex; justify-content:space-between; align-items:center;">
            <div>
              <div style="font-weight:700; font-size:0.9rem;">${escapeHtml(j.title)}</div>
              <div style="font-size:0.8rem; color:var(--text-muted);">${escapeHtml(j.company)} • ${escapeHtml(j.salary)}</div>
            </div>
            <div style="display:flex; gap:0.4rem;">
              <button class="btn-primary" style="padding:0.3rem 0.6rem; font-size:0.75rem;" onclick="window.openApplyModal(${j.id})">Apply</button>
              <button class="btn-secondary" style="padding:0.3rem 0.5rem; font-size:0.75rem;" onclick="window.toggleJobBookmark(${j.id})">✕</button>
            </div>
          </div>
        `).join('');
      }
    }
  }

  // --- Tab Switching Logic ---
  function switchTab(tabId) {
    state.activeTab = tabId;
    document.querySelectorAll('.nav-btn').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-tab') === tabId);
    });
    document.querySelectorAll('.tab-pane').forEach(pane => {
      pane.classList.toggle('active', pane.id === tabId);
    });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
  window.switchTab = switchTab;

  // --- Modal Utilities ---
  window.openModal = function (modalId) {
    const el = document.getElementById(modalId);
    if (el) el.classList.add('open');
  };

  window.closeModal = function (modalId) {
    const el = document.getElementById(modalId);
    if (el) el.classList.remove('open');
  };

  // --- Toast System ---
  function showToast(message) {
    const container = document.getElementById('toastContainer');
    if (!container) return;
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<span>⚡</span><span>${escapeHtml(message)}</span>`;
    container.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3200);
  }

  // --- Helpers ---
  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function renderMarkdown(md) {
    if (!md) return '';
    let html = escapeHtml(md);
    // Headers
    html = html.replace(/^### (.*$)/gim, '<h3 style="font-size:1.05rem; font-weight:700; margin:0.8rem 0 0.3rem;">$1</h3>');
    html = html.replace(/^## (.*$)/gim, '<h2 style="font-size:1.15rem; font-weight:700; margin:1rem 0 0.4rem;">$1</h2>');
    html = html.replace(/^# (.*$)/gim, '<h1 style="font-size:1.25rem; font-weight:800; margin:1.2rem 0 0.5rem;">$1</h1>');
    // Bold
    html = html.replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>');
    // Bullet points
    html = html.replace(/^\* (.*$)/gim, '<li style="margin-left:1rem;">$1</li>');
    // Code blocks
    html = html.replace(/```([\s\S]*?)```/gim, '<pre style="background:#00000044; padding:0.75rem; border-radius:6px; overflow-x:auto;"><code>$1</code></pre>');
    // Inline code
    html = html.replace(/`([^`]+)`/gim, '<code style="background:#00000033; padding:2px 5px; border-radius:4px; color:#38bdf8;">$1</code>');
    return html;
  }

  // --- Event Listeners Setup ---
  function setupEventListeners() {
    // Nav tabs
    document.querySelectorAll('.nav-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const tabId = btn.getAttribute('data-tab');
        switchTab(tabId);
      });
    });

    // Theme Toggle
    const themeBtn = document.getElementById('themeToggleBtn');
    if (themeBtn) {
      themeBtn.addEventListener('click', () => {
        const nextTheme = state.theme === 'dark' ? 'light' : 'dark';
        applyTheme(nextTheme);
        showToast(nextTheme === 'light' ? '☀️ Switched to Light Mode' : '🌙 Switched to Dark Mode');
      });
    }

    // Job Search & Filters
    const jobSearch = document.getElementById('jobSearchInput');
    if (jobSearch) {
      jobSearch.addEventListener('input', (e) => {
        state.jobSearchQuery = e.target.value.trim();
        renderJobs();
      });
    }

    const jobTypeSelect = document.getElementById('jobTypeFilter');
    if (jobTypeSelect) {
      jobTypeSelect.addEventListener('change', (e) => {
        state.jobTypeFilter = e.target.value;
        renderJobs();
      });
    }

    const jobExpSelect = document.getElementById('jobExpFilter');
    if (jobExpSelect) {
      jobExpSelect.addEventListener('change', (e) => {
        state.jobExpFilter = e.target.value;
        renderJobs();
      });
    }

    const bookmarkToggleBtn = document.getElementById('showBookmarksOnlyBtn');
    if (bookmarkToggleBtn) {
      bookmarkToggleBtn.addEventListener('click', () => {
        state.bookmarksOnly = !state.bookmarksOnly;
        bookmarkToggleBtn.classList.toggle('btn-primary', state.bookmarksOnly);
        bookmarkToggleBtn.classList.toggle('btn-secondary', !state.bookmarksOnly);
        renderJobs();
      });
    }

    // Prep Hub Category Tabs
    document.querySelectorAll('.prep-tab-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.prep-tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        state.activePrepCategory = btn.getAttribute('data-category');
        renderPrepMaterials();
        renderQuiz();
      });
    });

    // Company Filters
    const compSearch = document.getElementById('companySearchInput');
    if (compSearch) {
      compSearch.addEventListener('input', (e) => {
        state.companySearchQuery = e.target.value.trim();
        renderCompanies();
      });
    }

    const compTierSelect = document.getElementById('companyTierFilter');
    if (compTierSelect) {
      compTierSelect.addEventListener('change', (e) => {
        state.companyTierFilter = e.target.value;
        renderCompanies();
      });
    }

    // DSA Filters
    const dsaSearch = document.getElementById('dsaSearchInput');
    if (dsaSearch) {
      dsaSearch.addEventListener('input', (e) => {
        state.dsaSearchQuery = e.target.value.trim();
        renderDsaProblems();
      });
    }

    const dsaDiff = document.getElementById('dsaDiffFilter');
    if (dsaDiff) {
      dsaDiff.addEventListener('change', (e) => {
        state.dsaDiffFilter = e.target.value;
        renderDsaProblems();
      });
    }

    const dsaStatus = document.getElementById('dsaStatusFilter');
    if (dsaStatus) {
      dsaStatus.addEventListener('change', (e) => {
        state.dsaStatusFilter = e.target.value;
        renderDsaProblems();
      });
    }

    // Quick Apply Form Submission
    const applyForm = document.getElementById('applyJobForm');
    if (applyForm) {
      applyForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const jobId = parseInt(document.getElementById('applyJobId').value, 10);
        const job = state.jobs.find(j => j.id === jobId);

        const application = {
          job_id: jobId,
          job_title: job ? job.title : 'Software Role',
          company_name: job ? job.company : 'Tech Company',
          applicant_name: document.getElementById('applicantName').value,
          applicant_email: document.getElementById('applicantEmail').value,
          phone: document.getElementById('applicantPhone').value,
          resume_link: document.getElementById('applicantResume').value,
          experience_level: document.getElementById('applicantExp').value,
          cover_note: document.getElementById('applicantCover').value,
          status: 'Applied',
          applied_at: new Date().toISOString()
        };

        state.applications.unshift(application);
        localStorage.setItem('career_applications', JSON.stringify(state.applications));

        // Submit to API
        fetch('/api/apply', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(application)
        }).catch(() => {});

        closeModal('applyModal');
        showToast('🎉 Application submitted successfully!');
        renderJobs();
        renderDashboard();
      });
    }

    // Post Job Modal Button
    const postJobBtn = document.getElementById('openPostJobModalBtn');
    if (postJobBtn) {
      postJobBtn.addEventListener('click', () => openModal('postJobModal'));
    }

    // Post Job Form
    const postJobForm = document.getElementById('postJobForm');
    if (postJobForm) {
      postJobForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const newJob = {
          id: Date.now(),
          title: document.getElementById('newJobTitle').value,
          company: document.getElementById('newJobCompany').value,
          company_logo: 'https://via.placeholder.com/44?text=JOB',
          location: document.getElementById('newJobLocation').value,
          job_type: document.getElementById('newJobType').value,
          experience: document.getElementById('newJobExp').value || 'Fresher',
          salary: document.getElementById('newJobSalary').value,
          skills: document.getElementById('newJobSkills').value.split(',').map(s => s.trim()),
          tags: ['Community Posted'],
          description: document.getElementById('newJobDesc').value || 'Direct recruiter opening.',
          requirements: 'Standard software engineering skills and problem solving.',
          eligibility: document.getElementById('newJobEligibility').value || 'All Engineering streams eligible.',
          posted_date: 'Today',
          deadline: '30 Days',
          apply_url: '#'
        };

        state.jobs.unshift(newJob);

        fetch('/api/jobs', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(newJob)
        }).catch(() => {});

        closeModal('postJobModal');
        showToast('🚀 New Job posted to the portal!');
        renderJobs();
        postJobForm.reset();
      });
    }

    // Sign In Form Submission
    const signInForm = document.getElementById('signInForm');
    if (signInForm) {
      signInForm.addEventListener('submit', (e) => {
        e.preventDefault();
        state.currentUser = {
          name: document.getElementById('authName').value || 'Candidate',
          email: document.getElementById('authEmail').value || 'user@lmtjobs.com',
          role: document.getElementById('authRole').value || 'Candidate'
        };
        localStorage.setItem('lmt_user', JSON.stringify(state.currentUser));
        renderAuthUI();
        closeModal('signInModal');
        showToast(`🎉 Signed in successfully as ${state.currentUser.name}!`);
      });
    }

    // Close modals on outside click
    document.querySelectorAll('.modal-overlay').forEach(overlay => {
      overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
          overlay.classList.remove('open');
        }
      });
    });
  }

  // --- Initialize Application ---
  document.addEventListener('DOMContentLoaded', loadInitialData);

})();
