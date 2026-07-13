# -*- coding: utf-8 -*-
"""
LearnMate – Agentic AI for Personalized Course Pathways
========================================================
A Streamlit frontend application ready to integrate with IBM Granite APIs.
All pages are modular functions; session_state is used to persist data.
"""

import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

# ─────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="LearnMate – Personalized Course Pathways",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL CSS  – blue/white theme, rounded cards
# ─────────────────────────────────────────────
def inject_css():
    st.markdown(
        """
        <style>
        /* ── Base ── */
        html, body, [class*="css"] {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        }
        .main { background-color: #f0f4ff; }

        /* ── Sidebar ── */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a3c8f 0%, #0d2260 100%);
        }
        [data-testid="stSidebar"] * { color: #e8eeff !important; }
        [data-testid="stSidebar"] .stRadio label { font-size: 15px; font-weight: 500; }

        /* ── Cards ── */
        .card {
            background: #ffffff;
            border-radius: 14px;
            padding: 22px 24px;
            margin-bottom: 18px;
            box-shadow: 0 2px 12px rgba(26,60,143,0.10);
            border-left: 5px solid #1a3c8f;
        }
        .card-title {
            font-size: 17px;
            font-weight: 700;
            color: #1a3c8f;
            margin-bottom: 6px;
        }
        .card-sub { color: #555; font-size: 13px; }

        /* ── Hero ── */
        .hero {
            background: linear-gradient(135deg, #1a3c8f 0%, #2563eb 60%, #3b82f6 100%);
            border-radius: 18px;
            padding: 50px 40px;
            color: #fff;
            text-align: center;
            margin-bottom: 32px;
        }
        .hero h1 { font-size: 2.4rem; font-weight: 800; margin-bottom: 14px; }
        .hero p  { font-size: 1.1rem; opacity: 0.9; max-width: 680px; margin: 0 auto 28px; }

        /* ── Badge ── */
        .badge {
            display: inline-block;
            padding: 4px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
            margin: 2px;
        }
        .badge-blue   { background:#dbeafe; color:#1e40af; }
        .badge-green  { background:#dcfce7; color:#166534; }
        .badge-orange { background:#fff7ed; color:#c2410c; }
        .badge-purple { background:#ede9fe; color:#6d28d9; }

        /* ── Stat box ── */
        .stat-box {
            background: #fff;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(26,60,143,0.09);
        }
        .stat-num { font-size: 2rem; font-weight: 800; color: #1a3c8f; }
        .stat-lbl { font-size: 13px; color: #666; margin-top: 4px; }

        /* ── Chat ── */
        .chat-user {
            background: #dbeafe;
            border-radius: 14px 14px 4px 14px;
            padding: 10px 16px;
            margin: 8px 0 8px auto;
            max-width: 70%;
            color: #1e3a8a;
            font-size: 14px;
        }
        .chat-bot {
            background: #f0f4ff;
            border: 1px solid #c7d2fe;
            border-radius: 14px 14px 14px 4px;
            padding: 10px 16px;
            margin: 8px auto 8px 0;
            max-width: 70%;
            color: #1f2937;
            font-size: 14px;
        }
        .chat-wrap { max-height: 420px; overflow-y: auto; padding: 8px 4px; }

        /* ── Section header ── */
        .section-header {
            font-size: 1.5rem;
            font-weight: 800;
            color: #1a3c8f;
            border-bottom: 3px solid #3b82f6;
            padding-bottom: 6px;
            margin-bottom: 22px;
        }

        /* ── Footer ── */
        .footer {
            text-align: center;
            color: #888;
            font-size: 13px;
            padding: 24px 0 8px;
            border-top: 1px solid #e2e8f0;
            margin-top: 40px;
        }

        /* ── Stage card ── */
        .stage-card {
            background: #fff;
            border-radius: 12px;
            padding: 18px 20px;
            box-shadow: 0 2px 10px rgba(26,60,143,0.08);
            border-top: 4px solid #3b82f6;
            height: 100%;
        }
        .stage-title { font-size: 15px; font-weight: 700; color: #1a3c8f; margin-bottom: 10px; }

        /* ── Course card ── */
        .course-card {
            background: #fff;
            border-radius: 14px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(26,60,143,0.08);
            border-top: 4px solid #2563eb;
            margin-bottom: 16px;
        }
        .course-title { font-size: 16px; font-weight: 700; color: #1e3a8a; }
        .course-meta  { font-size: 12px; color: #64748b; margin: 6px 0; }
        .star { color: #f59e0b; }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# SESSION STATE  initialisation
# ─────────────────────────────────────────────
def init_session_state():
    defaults = {
        "page": "Home",
        "profile": {},
        "assessment_scores": {},
        "completed_stages": {},
        "chat_history": [
            {
                "role": "assistant",
                "content": (
                    "👋 Hi! I'm your AI Learning Coach powered by IBM Granite. "
                    "Tell me your goal and I'll build a personalised pathway for you!"
                ),
            }
        ],
        "dark_mode": False,
        "notifications": True,
        "courses_completed": 3,
        "skills_learned": 8,
        "weekly_hours": 12,
        "streak": 7,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ─────────────────────────────────────────────
# SIDEBAR  navigation
# ─────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown(
            "<h2 style='text-align:center;color:#fff;font-size:1.4rem;'>🎓 LearnMate</h2>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='text-align:center;font-size:12px;opacity:.7;margin-top:-10px;'>Agentic AI Pathways</p>",
            unsafe_allow_html=True,
        )
        st.divider()

        pages = [
            ("🏠", "Home"),
            ("👤", "Profile"),
            ("📊", "Skill Assessment"),
            ("🗺️", "Learning Roadmap"),
            ("📚", "Course Recommendations"),
            ("📈", "Progress Tracker"),
            ("🤖", "AI Chat Coach"),
            ("⚙️", "Settings"),
        ]

        for icon, label in pages:
            if st.sidebar.button(
                f"{icon}  {label}",
                key=f"nav_{label}",
                use_container_width=True,
            ):
                st.session_state.page = label
                st.rerun()

        st.divider()
        # Quick profile summary
        name = st.session_state.profile.get("name", "Student")
        goal = st.session_state.profile.get("career_goal", "Not set")
        st.markdown(
            f"<div style='font-size:12px;opacity:.8;'>"
            f"<b>👋 {name}</b><br>🎯 {goal}</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div class='footer' style='color:#aaa;'>Powered by IBM Granite AI</div>",
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────
# PAGE 1 – HOME / LANDING
# ─────────────────────────────────────────────
def page_home():
    st.markdown(
        """
        <div class="hero">
            <h1>🎓 LearnMate</h1>
            <p>
                Your Agentic AI for Personalized Course Pathways.<br>
                Discover the best learning journey based on your interests,
                current skills, and career goals — powered by IBM Granite AI.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("🚀  Get Started", type="primary", use_container_width=True):
            st.session_state.page = "Profile"
            st.rerun()
    with col2:
        if st.button("📊  Take Skill Assessment", use_container_width=True):
            st.session_state.page = "Skill Assessment"
            st.rerun()
    with col3:
        if st.button("🤖  Chat with AI Coach", use_container_width=True):
            st.session_state.page = "AI Chat Coach"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Feature highlights
    st.markdown('<div class="section-header">✨ Why LearnMate?</div>', unsafe_allow_html=True)
    f1, f2, f3, f4 = st.columns(4)
    features = [
        ("🧠", "AI-Powered", "Personalised roadmaps built by IBM Granite LLM based on your unique profile."),
        ("🎯", "Goal-Oriented", "Every recommendation is aligned with your specific career destination."),
        ("📈", "Track Progress", "Visual dashboards keep you motivated with streaks and milestones."),
        ("💬", "Chat Coach", "24/7 AI coach to answer questions and keep you on track."),
    ]
    for col, (icon, title, desc) in zip([f1, f2, f3, f4], features):
        with col:
            st.markdown(
                f'<div class="card"><div class="card-title">{icon} {title}</div>'
                f'<div class="card-sub">{desc}</div></div>',
                unsafe_allow_html=True,
            )

    # Quick stats
    st.markdown('<div class="section-header">📊 Platform Stats</div>', unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    stats = [("10K+", "Students"), ("500+", "Courses"), ("50+", "Pathways"), ("98%", "Satisfaction")]
    for col, (num, lbl) in zip([s1, s2, s3, s4], stats):
        with col:
            st.markdown(
                f'<div class="stat-box"><div class="stat-num">{num}</div>'
                f'<div class="stat-lbl">{lbl}</div></div>',
                unsafe_allow_html=True,
            )

    render_footer()


# ─────────────────────────────────────────────
# PAGE 2 – STUDENT PROFILE
# ─────────────────────────────────────────────
def page_profile():
    st.markdown('<div class="section-header">👤 Student Profile</div>', unsafe_allow_html=True)

    p = st.session_state.profile  # shorthand

    with st.form("profile_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full Name", value=p.get("name", ""))
            email = st.text_input("Email Address", value=p.get("email", ""))
            college = st.text_input("College / University", value=p.get("college", ""))
            branch = st.text_input("Branch / Department", value=p.get("branch", ""))

        with col2:
            year = st.selectbox(
                "Year of Study",
                ["1st Year", "2nd Year", "3rd Year", "4th Year", "Post Graduate"],
                index=["1st Year", "2nd Year", "3rd Year", "4th Year", "Post Graduate"].index(
                    p.get("year", "1st Year")
                ),
            )
            skill_level = st.selectbox(
                "Current Skill Level",
                ["Beginner", "Intermediate", "Advanced"],
                index=["Beginner", "Intermediate", "Advanced"].index(
                    p.get("skill_level", "Beginner")
                ),
            )
            career_goal = st.text_input(
                "Career Goal (e.g. Full Stack Developer)",
                value=p.get("career_goal", ""),
            )
            learning_style = st.selectbox(
                "Preferred Learning Style",
                ["Video Tutorials", "Reading Docs", "Hands-on Projects", "Peer Learning"],
                index=["Video Tutorials", "Reading Docs", "Hands-on Projects", "Peer Learning"].index(
                    p.get("learning_style", "Video Tutorials")
                ),
            )

        study_hours = st.slider(
            "Available Study Hours per Week",
            min_value=1,
            max_value=40,
            value=p.get("study_hours", 10),
        )

        st.markdown("#### 🏷️ Interests (select all that apply)")
        interest_options = [
            "Frontend Development", "Backend Development", "Full Stack Development",
            "Python", "Java", "Data Structures", "Machine Learning",
            "Artificial Intelligence", "Cybersecurity", "Cloud Computing",
            "DevOps", "UI/UX Design", "Data Science", "Mobile App Development",
        ]
        saved_interests = p.get("interests", [])
        interests = st.multiselect(
            "Select your interests",
            options=interest_options,
            default=saved_interests,
        )

        submitted = st.form_submit_button("💾  Save Profile", type="primary", use_container_width=True)

    if submitted:
        st.session_state.profile = {
            "name": name,
            "email": email,
            "college": college,
            "branch": branch,
            "year": year,
            "skill_level": skill_level,
            "career_goal": career_goal,
            "learning_style": learning_style,
            "study_hours": study_hours,
            "interests": interests,
        }
        st.success("✅ Profile saved successfully!")
        st.balloons()

    # Display current profile summary if saved
    if st.session_state.profile:
        st.markdown("---")
        st.markdown('<div class="section-header">📋 Profile Summary</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(
                f'<div class="card">'
                f'<div class="card-title">👤 {p.get("name","—")}</div>'
                f'<div class="card-sub">📧 {p.get("email","—")}<br>'
                f'🏫 {p.get("college","—")} | {p.get("branch","—")} | {p.get("year","—")}<br>'
                f'🎯 {p.get("career_goal","—")}</div></div>',
                unsafe_allow_html=True,
            )
        with c2:
            badge_color = {"Beginner": "badge-orange", "Intermediate": "badge-blue", "Advanced": "badge-green"}
            level = p.get("skill_level", "Beginner")
            badges = " ".join(
                [f'<span class="badge badge-purple">{i}</span>' for i in p.get("interests", [])]
            )
            st.markdown(
                f'<div class="card">'
                f'<span class="badge {badge_color.get(level,"badge-blue")}">{level}</span>'
                f'<div class="card-sub" style="margin-top:8px;">'
                f'📚 {p.get("learning_style","—")}<br>'
                f'⏰ {p.get("study_hours",0)} hrs/week</div>'
                f'<div style="margin-top:10px;">{badges}</div></div>',
                unsafe_allow_html=True,
            )

    render_footer()


# ─────────────────────────────────────────────
# PAGE 3 – SKILL ASSESSMENT
# ─────────────────────────────────────────────
def page_skill_assessment():
    st.markdown('<div class="section-header">📊 Skill Assessment</div>', unsafe_allow_html=True)
    st.info("Rate yourself honestly. These scores power your personalised roadmap.")

    skills = {
        "Programming Knowledge": (
            "How comfortable are you with writing code?",
            ["No experience", "Can write basic code", "Comfortable", "Proficient", "Expert"],
        ),
        "Problem Solving": (
            "How well do you solve algorithmic problems?",
            ["Struggling", "Basic problems", "Moderate", "Advanced", "Competitive level"],
        ),
        "HTML/CSS": (
            "Your HTML & CSS proficiency?",
            ["Never used", "Know basics", "Can build layouts", "Responsive design", "Advanced animations"],
        ),
        "JavaScript": (
            "Your JavaScript level?",
            ["Never used", "Basic syntax", "DOM manipulation", "Async/frameworks", "Expert"],
        ),
        "Python": (
            "Your Python proficiency?",
            ["Never used", "Basic scripts", "OOP & libraries", "Data/ML libraries", "Expert"],
        ),
        "SQL": (
            "Your SQL knowledge?",
            ["Never used", "Basic SELECT", "JOINs & subqueries", "Stored procs", "Query optimisation"],
        ),
        "Communication Skills": (
            "Your technical communication?",
            ["Poor", "Basic", "Moderate", "Good", "Excellent"],
        ),
    }

    scores = {}
    with st.form("assessment_form"):
        for skill, (question, options) in skills.items():
            st.markdown(f"**{skill}**")
            val = st.radio(
                question,
                options=options,
                key=f"assess_{skill}",
                horizontal=True,
                index=st.session_state.assessment_scores.get(skill, 0),
            )
            scores[skill] = options.index(val) if val is not None else 0
            st.markdown("---")

        submitted = st.form_submit_button("📊  Submit Assessment", type="primary", use_container_width=True)

    if submitted:
        st.session_state.assessment_scores = scores
        st.success("✅ Assessment submitted!")

    # Show results
    if st.session_state.assessment_scores:
        st.markdown('<div class="section-header">📈 Assessment Results</div>', unsafe_allow_html=True)
        total = sum(st.session_state.assessment_scores.values())
        max_score = len(skills) * 4  # 0-4 scale
        overall_pct = int((total / max_score) * 100)

        col1, col2 = st.columns([1, 2])
        with col1:
            # Overall gauge
            if overall_pct >= 75:
                badge_cls, level_txt = "badge-green", "Advanced"
            elif overall_pct >= 45:
                badge_cls, level_txt = "badge-blue", "Intermediate"
            else:
                badge_cls, level_txt = "badge-orange", "Beginner"

            st.markdown(
                f'<div class="card" style="text-align:center;">'
                f'<div class="card-title">Overall Score</div>'
                f'<div style="font-size:3rem;font-weight:900;color:#1a3c8f;">{overall_pct}%</div>'
                f'<span class="badge {badge_cls}" style="font-size:14px;padding:6px 20px;">'
                f'{level_txt}</span></div>',
                unsafe_allow_html=True,
            )
            st.progress(overall_pct / 100)

        with col2:
            # Per-skill bars
            for skill, score in st.session_state.assessment_scores.items():
                pct = int((score / 4) * 100)
                st.markdown(f"**{skill}** — {pct}%")
                st.progress(pct / 100)

    render_footer()


# ─────────────────────────────────────────────
# PAGE 4 – LEARNING ROADMAP
# ─────────────────────────────────────────────
def page_learning_roadmap():
    st.markdown('<div class="section-header">🗺️ Personalized Learning Roadmap</div>', unsafe_allow_html=True)

    goal = st.session_state.profile.get("career_goal", "Full Stack Developer")
    st.markdown(f"**Career Goal:** `{goal}`  |  Pathway curated by IBM Granite AI (demo data)")

    # Roadmap data – structured so IBM Granite API can replace it later
    roadmap = [
        {
            "stage": "Stage 1",
            "title": "Web Foundations",
            "color": "#3b82f6",
            "topics": ["HTML5", "CSS3", "Flexbox / Grid", "Git & GitHub"],
            "duration": "3 weeks",
        },
        {
            "stage": "Stage 2",
            "title": "JavaScript Core",
            "color": "#8b5cf6",
            "topics": ["JS Fundamentals", "DOM Manipulation", "ES6+", "Async / Promises"],
            "duration": "4 weeks",
        },
        {
            "stage": "Stage 3",
            "title": "Frontend Framework",
            "color": "#06b6d4",
            "topics": ["React.js", "State Management", "REST APIs", "React Router"],
            "duration": "5 weeks",
        },
        {
            "stage": "Stage 4",
            "title": "Backend Development",
            "color": "#10b981",
            "topics": ["Node.js", "Express", "MongoDB / SQL", "Authentication"],
            "duration": "5 weeks",
        },
        {
            "stage": "Stage 5",
            "title": "DevOps & Deployment",
            "color": "#f59e0b",
            "topics": ["Docker", "CI/CD", "IBM Cloud", "Portfolio & Projects"],
            "duration": "3 weeks",
        },
    ]

    completed_count = 0

    for i, stage in enumerate(roadmap):
        key = f"stage_{i}"
        if key not in st.session_state.completed_stages:
            st.session_state.completed_stages[key] = False

        col_check, col_card = st.columns([0.5, 9.5])
        with col_check:
            checked = st.checkbox("", key=key, value=st.session_state.completed_stages[key])
            st.session_state.completed_stages[key] = checked
        with col_card:
            if checked:
                completed_count += 1

            status_html = (
                '<span class="badge badge-green">✓ Completed</span>'
                if checked
                else '<span class="badge badge-blue">In Progress</span>'
            )
            topics_html = " ".join(
                [f'<span class="badge badge-purple">{t}</span>' for t in stage["topics"]]
            )
            st.markdown(
                f'<div class="card" style="border-left-color:{stage["color"]};">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                f'<div><span style="font-size:11px;color:#64748b;">{stage["stage"]}</span>'
                f'<div class="card-title">{stage["title"]}</div></div>'
                f'{status_html}'
                f'</div>'
                f'<div style="margin:10px 0;">{topics_html}</div>'
                f'<div class="card-sub">⏱ Estimated: <b>{stage["duration"]}</b></div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # Overall roadmap progress
    progress_pct = completed_count / len(roadmap)
    st.markdown("---")
    st.markdown(f"**Overall Roadmap Progress — {int(progress_pct * 100)}%**")
    st.progress(progress_pct)

    render_footer()


# ─────────────────────────────────────────────
# PAGE 5 – COURSE RECOMMENDATIONS
# ─────────────────────────────────────────────
def page_course_recommendations():
    st.markdown('<div class="section-header">📚 Course Recommendations</div>', unsafe_allow_html=True)
    st.caption("Recommendations powered by IBM Granite AI (demo data)")

    # Dummy course data – swap with IBM API response later
    courses = [
        {
            "title": "The Complete Web Developer Bootcamp",
            "platform": "Udemy",
            "difficulty": "Beginner",
            "duration": "65 hrs",
            "rating": 4.8,
            "link": "#",
            "badge": "badge-orange",
            "image_color": "#3b82f6",
        },
        {
            "title": "JavaScript Algorithms & Data Structures",
            "platform": "freeCodeCamp",
            "difficulty": "Intermediate",
            "duration": "300 hrs",
            "rating": 4.9,
            "link": "#",
            "badge": "badge-blue",
            "image_color": "#8b5cf6",
        },
        {
            "title": "React – The Complete Guide",
            "platform": "Udemy",
            "difficulty": "Intermediate",
            "duration": "49 hrs",
            "rating": 4.7,
            "link": "#",
            "badge": "badge-blue",
            "image_color": "#06b6d4",
        },
        {
            "title": "IBM Full Stack Software Developer",
            "platform": "Coursera / IBM",
            "difficulty": "Intermediate",
            "duration": "6 months",
            "rating": 4.6,
            "link": "#",
            "badge": "badge-blue",
            "image_color": "#1a3c8f",
        },
        {
            "title": "Machine Learning Specialisation",
            "platform": "Coursera / Stanford",
            "difficulty": "Advanced",
            "duration": "3 months",
            "rating": 4.9,
            "link": "#",
            "badge": "badge-green",
            "image_color": "#10b981",
        },
        {
            "title": "IBM AI Engineering Professional",
            "platform": "Coursera / IBM",
            "difficulty": "Advanced",
            "duration": "8 months",
            "rating": 4.7,
            "link": "#",
            "badge": "badge-green",
            "image_color": "#f59e0b",
        },
    ]

    # Filter controls
    difficulty_filter = st.multiselect(
        "Filter by Difficulty",
        options=["Beginner", "Intermediate", "Advanced"],
        default=["Beginner", "Intermediate", "Advanced"],
    )
    filtered = [c for c in courses if c["difficulty"] in difficulty_filter]

    cols = st.columns(2)
    for idx, course in enumerate(filtered):
        with cols[idx % 2]:
            stars = "⭐" * int(course["rating"])
            st.markdown(
                f'<div class="course-card">'
                f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;">'
                f'<div style="width:44px;height:44px;border-radius:10px;background:{course["image_color"]};'
                f'display:flex;align-items:center;justify-content:center;color:white;font-weight:800;">📖</div>'
                f'<div><div class="course-title">{course["title"]}</div>'
                f'<div class="course-meta">🏫 {course["platform"]}</div></div>'
                f'</div>'
                f'<span class="badge {course["badge"]}">{course["difficulty"]}</span>'
                f'<span class="badge badge-purple">⏱ {course["duration"]}</span>'
                f'<div style="margin-top:10px;" class="card-sub">'
                f'<span class="star">{stars}</span> {course["rating"]}/5</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            st.button(
                "📋  Enroll Now",
                key=f"enroll_{idx}",
                type="primary",
                use_container_width=True,
            )

    render_footer()


# ─────────────────────────────────────────────
# PAGE 6 – PROGRESS DASHBOARD
# ─────────────────────────────────────────────
def page_progress_tracker():
    st.markdown('<div class="section-header">📈 Progress Dashboard</div>', unsafe_allow_html=True)

    # KPI stat boxes
    k1, k2, k3, k4, k5 = st.columns(5)
    kpis = [
        ("72%", "Overall Progress"),
        (str(st.session_state.courses_completed), "Courses Completed"),
        (str(st.session_state.skills_learned), "Skills Learned"),
        (str(st.session_state.weekly_hours) + " hrs", "This Week"),
        ("🔥 " + str(st.session_state.streak), "Day Streak"),
    ]
    for col, (num, lbl) in zip([k1, k2, k3, k4, k5], kpis):
        with col:
            st.markdown(
                f'<div class="stat-box"><div class="stat-num">{num}</div>'
                f'<div class="stat-lbl">{lbl}</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts ──────────────────────────────────────────────
    chart_col1, chart_col2 = st.columns(2)

    # Bar chart – weekly study hours
    with chart_col1:
        st.markdown("**📊 Weekly Study Hours (last 8 weeks)**")
        dates = [
            (datetime.today() - timedelta(weeks=7 - i)).strftime("%b %d")
            for i in range(8)
        ]
        hours = [random.randint(5, 20) for _ in range(8)]
        df_bar = pd.DataFrame({"Week": dates, "Hours": hours})
        st.bar_chart(df_bar.set_index("Week"))

    # Line chart – skill growth
    with chart_col2:
        st.markdown("**📈 Skill Growth Over Time**")
        weeks = [f"Wk {i+1}" for i in range(10)]
        skill_scores = sorted(random.sample(range(30, 100), 10))
        df_line = pd.DataFrame({"Week": weeks, "Score": skill_scores})
        st.line_chart(df_line.set_index("Week"))

    # Pie chart – time per topic (using bar chart as Streamlit has no native pie)
    st.markdown("**🥧 Time Spent per Topic (hrs)**")
    topics = {
        "HTML/CSS": 12,
        "JavaScript": 18,
        "React": 14,
        "Python": 10,
        "SQL": 6,
        "DevOps": 4,
    }
    df_pie = pd.DataFrame(
        {"Topic": list(topics.keys()), "Hours": list(topics.values())}
    )
    st.bar_chart(df_pie.set_index("Topic"))

    # Skills progress bars
    st.markdown("---")
    st.markdown("**🎯 Skill Proficiency**")
    skill_levels = {
        "HTML/CSS": 85,
        "JavaScript": 65,
        "React.js": 50,
        "Python": 70,
        "SQL": 45,
        "Git/GitHub": 80,
        "Node.js": 35,
    }
    s1, s2 = st.columns(2)
    items = list(skill_levels.items())
    for i, (skill, pct) in enumerate(items):
        with s1 if i % 2 == 0 else s2:
            st.markdown(f"**{skill}** — {pct}%")
            st.progress(pct / 100)

    render_footer()


# ─────────────────────────────────────────────
# PAGE 7 – AI CHAT COACH
# ─────────────────────────────────────────────

# Dummy AI responses – replace with IBM Granite API call
def get_ai_response(user_message: str) -> str:
    """
    IBM Granite integration point.
    Replace the dummy responses below with an IBM Granite API call:
        from ibm_watsonx_ai import Credentials
        from ibm_watsonx_ai.foundation_models import ModelInference
        ...
    """
    responses = [
        "Great choice! Based on your profile, I recommend learning Python before Machine Learning.",
        "I noticed you're interested in Full Stack Development. Start with HTML, CSS, then JavaScript.",
        "For your career goal, IBM's Full Stack Developer Certification on Coursera is excellent!",
        "Consistency beats intensity — even 2 hours daily will get you to your goal faster.",
        "Try building a small project after each stage. It cements your learning effectively.",
        "You're making great progress! Next, I recommend exploring React.js for frontend mastery.",
        "Based on your skill level, you're ready to tackle intermediate JavaScript concepts.",
        "IBM Cloud Lite offers free resources to deploy your projects — highly recommended!",
    ]
    # Simple keyword matching for slightly smarter dummy responses
    msg_lower = user_message.lower()
    if "python" in msg_lower:
        return "Python is a fantastic choice! Start with basics, then move to NumPy, Pandas, and eventually scikit-learn for ML."
    if "machine learning" in msg_lower or "ml" in msg_lower:
        return "For ML, ensure you have strong Python and math fundamentals first. IBM's AI Engineering certification is a great structured path."
    if "web" in msg_lower or "frontend" in msg_lower:
        return "For web development: HTML → CSS → JavaScript → React is the proven pathway. Build projects at every stage!"
    if "job" in msg_lower or "career" in msg_lower:
        return "Focus on building a strong portfolio with 3-5 projects. GitHub presence + IBM certifications will make you stand out."
    return random.choice(responses)


def page_ai_chat_coach():
    st.markdown('<div class="section-header">🤖 AI Chat Coach</div>', unsafe_allow_html=True)
    st.caption("Powered by IBM Granite AI · Ask anything about your learning journey")

    # Display chat history
    chat_html = '<div class="chat-wrap">'
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            chat_html += f'<div class="chat-user">👤 {msg["content"]}</div>'
        else:
            chat_html += f'<div class="chat-bot">🤖 {msg["content"]}</div>'
    chat_html += "</div>"
    st.markdown(chat_html, unsafe_allow_html=True)

    # Input row
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        user_input = st.text_input(
            "Message",
            placeholder="Ask me about courses, skills, career paths…",
            label_visibility="collapsed",
            key="chat_input",
        )
    with col_btn:
        send = st.button("Send ➤", type="primary", use_container_width=True)

    if send and user_input.strip():
        # Append user message
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        # Get AI response (swap with IBM Granite API here)
        ai_reply = get_ai_response(user_input)
        st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
        st.rerun()

    # Suggested prompts
    st.markdown("**💡 Suggested Prompts**")
    sp1, sp2, sp3 = st.columns(3)
    prompts = [
        "What should I learn for Machine Learning?",
        "How do I become a Full Stack Developer?",
        "Recommend IBM Cloud courses for me",
    ]
    for col, prompt in zip([sp1, sp2, sp3], prompts):
        with col:
            if st.button(f"💬 {prompt}", use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": get_ai_response(prompt)}
                )
                st.rerun()

    render_footer()


# ─────────────────────────────────────────────
# PAGE 8 – SETTINGS
# ─────────────────────────────────────────────
def page_settings():
    st.markdown('<div class="section-header">⚙️ Settings</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="card"><div class="card-title">🎨 Appearance</div>', unsafe_allow_html=True)
        dark_mode = st.toggle(
            "Dark Mode",
            value=st.session_state.dark_mode,
            key="toggle_dark",
            help="Dark mode UI (coming soon – requires page refresh)",
        )
        st.session_state.dark_mode = dark_mode
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title">🔔 Notifications</div>', unsafe_allow_html=True)
        notifs = st.toggle(
            "Enable Notifications",
            value=st.session_state.notifications,
            key="toggle_notif",
        )
        st.session_state.notifications = notifs
        st.toggle("Weekly Email Digest", value=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card"><div class="card-title">📥 Data & Export</div>', unsafe_allow_html=True)

        # Generate learning plan content
        plan_lines = [
            "LearnMate – Personalized Learning Plan",
            "=" * 40,
            f"Name: {st.session_state.profile.get('name', 'N/A')}",
            f"Career Goal: {st.session_state.profile.get('career_goal', 'N/A')}",
            f"Skill Level: {st.session_state.profile.get('skill_level', 'N/A')}",
            f"Study Hours/Week: {st.session_state.profile.get('study_hours', 0)}",
            "",
            "Interests:",
        ]
        for interest in st.session_state.profile.get("interests", []):
            plan_lines.append(f"  • {interest}")
        plan_lines += [
            "",
            "Assessment Scores:",
        ]
        for skill, score in st.session_state.assessment_scores.items():
            plan_lines.append(f"  • {skill}: {int((score/4)*100)}%")
        plan_content = "\n".join(plan_lines)

        st.download_button(
            label="📥  Download Learning Plan (.txt)",
            data=plan_content,
            file_name="learnmate_plan.txt",
            mime="text/plain",
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title">🔐 Account</div>', unsafe_allow_html=True)
        if st.button("🚪  Logout", use_container_width=True, type="secondary"):
            # Reset session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # IBM Cloud integration section
    st.markdown("---")
    st.markdown('<div class="section-header">☁️ IBM Cloud Integration</div>', unsafe_allow_html=True)
    with st.expander("Configure IBM Granite API (Future Integration)"):
        st.text_input("IBM Cloud API Key", placeholder="Enter your IBM Cloud API Key", type="password")
        st.text_input("Watson API URL", placeholder="https://us-south.ml.cloud.ibm.com")
        st.selectbox(
            "Model",
            ["ibm/granite-13b-chat-v2", "ibm/granite-34b-code-instruct", "ibm/granite-3-8b-instruct"],
        )
        st.info(
            "🔒 API keys are not stored. Connect your IBM Cloud Lite account to enable "
            "AI-powered personalised recommendations via IBM Granite LLM."
        )
        st.button("🔗  Test Connection", use_container_width=True)

    render_footer()


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
def render_footer():
    st.markdown(
        '<div class="footer">Powered by IBM Granite AI &nbsp;|&nbsp; '
        "IBM Cloud Lite &nbsp;|&nbsp; LearnMate &copy; 2025</div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────
def route():
    page = st.session_state.page
    if page == "Home":
        page_home()
    elif page == "Profile":
        page_profile()
    elif page == "Skill Assessment":
        page_skill_assessment()
    elif page == "Learning Roadmap":
        page_learning_roadmap()
    elif page == "Course Recommendations":
        page_course_recommendations()
    elif page == "Progress Tracker":
        page_progress_tracker()
    elif page == "AI Chat Coach":
        page_ai_chat_coach()
    elif page == "Settings":
        page_settings()
    else:
        page_home()


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__" or True:
    inject_css()
    init_session_state()
    render_sidebar()
    route()
