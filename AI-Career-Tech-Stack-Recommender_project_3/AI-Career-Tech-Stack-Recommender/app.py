import pandas as pd
import streamlit as st

from recommender import CareerRecommender


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI Career Navigator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------------------
# CUSTOM CSS - DIGITAL / CREATIVE UI
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(0, 170, 255, 0.20), transparent 35%),
            radial-gradient(circle at top right, rgba(170, 0, 255, 0.18), transparent 35%),
            linear-gradient(135deg, #08111f 0%, #111827 45%, #030712 100%);
        color: #f8fafc;
    }

    section[data-testid="stSidebar"] {
        background: rgba(3, 7, 18, 0.88);
        border-right: 1px solid rgba(148, 163, 184, 0.20);
    }

    section[data-testid="stSidebar"] * {
        color: #f8fafc;
    }

    .main-title {
        font-size: 3.4rem;
        font-weight: 800;
        line-height: 1.08;
        background: linear-gradient(90deg, #38bdf8, #a78bfa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .subtitle {
        font-size: 1.08rem;
        color: #cbd5e1;
        max-width: 900px;
        line-height: 1.7;
    }

    .hero-card {
        padding: 2rem;
        border-radius: 28px;
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.24);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.35);
        margin-bottom: 1.2rem;
    }

    .glass-card {
        padding: 1.25rem;
        border-radius: 22px;
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.22);
        box-shadow: 0 14px 35px rgba(0, 0, 0, 0.25);
        height: 100%;
    }

    .field-card {
        padding: 1.35rem;
        border-radius: 24px;
        background: linear-gradient(145deg, rgba(14, 165, 233, 0.15), rgba(168, 85, 247, 0.13));
        border: 1px solid rgba(125, 211, 252, 0.22);
        box-shadow: inset 0 0 35px rgba(56, 189, 248, 0.06), 0 16px 42px rgba(0, 0, 0, 0.28);
        min-height: 210px;
    }

    .pill {
        display: inline-block;
        padding: 0.45rem 0.75rem;
        border-radius: 999px;
        margin: 0.18rem;
        background: rgba(56, 189, 248, 0.13);
        border: 1px solid rgba(56, 189, 248, 0.25);
        color: #e0f2fe;
        font-size: 0.88rem;
        font-weight: 600;
    }

    .pink-pill {
        background: rgba(244, 114, 182, 0.13);
        border: 1px solid rgba(244, 114, 182, 0.25);
        color: #fce7f3;
    }

    .green-pill {
        background: rgba(34, 197, 94, 0.13);
        border: 1px solid rgba(34, 197, 94, 0.25);
        color: #dcfce7;
    }

    .warning-box {
        padding: 1rem;
        border-radius: 18px;
        background: rgba(245, 158, 11, 0.12);
        border: 1px solid rgba(245, 158, 11, 0.28);
        color: #fde68a;
        margin: 1rem 0;
    }

    .success-box {
        padding: 1rem;
        border-radius: 18px;
        background: rgba(34, 197, 94, 0.12);
        border: 1px solid rgba(34, 197, 94, 0.28);
        color: #dcfce7;
        margin: 1rem 0;
    }

    .step-box {
        padding: 1rem;
        border-left: 4px solid #38bdf8;
        background: rgba(15, 23, 42, 0.72);
        border-radius: 14px;
        margin-bottom: 0.75rem;
    }

    div[data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.20);
        padding: 1rem;
        border-radius: 18px;
    }

    .stButton > button {
        border-radius: 999px;
        font-weight: 700;
        padding: 0.65rem 1.3rem;
        border: 1px solid rgba(56, 189, 248, 0.45);
        background: linear-gradient(90deg, #0284c7, #7c3aed);
        color: white;
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.28);
    }

    .stButton > button:hover {
        border: 1px solid rgba(244, 114, 182, 0.65);
        box-shadow: 0 14px 40px rgba(168, 85, 247, 0.38);
    }

    h1, h2, h3 {
        color: #f8fafc;
    }

    p, li {
        color: #cbd5e1;
    }

    .small-muted {
        color: #94a3b8;
        font-size: 0.92rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# DATA LOADING
# ---------------------------------------------------------
@st.cache_resource
def load_recommender():
    return CareerRecommender("career_dataset.csv")


@st.cache_data
def load_dataset():
    return pd.read_csv("career_dataset.csv")


recommender = load_recommender()
dataset = load_dataset()


# ---------------------------------------------------------
# CAREER SIDE KNOWLEDGE BASE
# ---------------------------------------------------------
CAREER_SIDES = {
    "Artificial Intelligence": {
        "icon": "🤖",
        "tagline": "Build systems that can understand, predict, generate, and automate decisions.",
        "what": "Artificial Intelligence focuses on creating systems that can perform tasks that normally need human intelligence, such as prediction, language understanding, image recognition, and decision making.",
        "best_for": "Students who enjoy Python, mathematics, problem solving, research, automation, and intelligent systems.",
        "subjects": [
            "Python Programming", "Linear Algebra", "Probability & Statistics",
            "Machine Learning", "Deep Learning", "Natural Language Processing",
            "Computer Vision", "Model Evaluation", "AI Ethics"
        ],
        "tools": [
            "Python", "NumPy", "Pandas", "Scikit-learn", "TensorFlow",
            "PyTorch", "Hugging Face", "OpenCV", "Jupyter Notebook"
        ],
        "projects": [
            "AI chatbot for students",
            "Image classification system",
            "Resume skill extractor",
            "AI career recommendation system"
        ],
        "roadmap": [
            "Learn Python basics and data handling.",
            "Study statistics, linear algebra, and machine learning fundamentals.",
            "Build small ML projects using Scikit-learn.",
            "Move to deep learning with TensorFlow or PyTorch.",
            "Create a portfolio project with deployment."
        ]
    },
    "Data Science": {
        "icon": "📊",
        "tagline": "Turn raw data into useful predictions, insights, and decisions.",
        "what": "Data Science combines programming, statistics, machine learning, and domain knowledge to solve real-world problems using data.",
        "best_for": "Students who like data, analysis, prediction, storytelling, and problem solving.",
        "subjects": [
            "Python", "Statistics", "Data Cleaning", "Exploratory Data Analysis",
            "Machine Learning", "Data Visualization", "Feature Engineering", "Model Evaluation"
        ],
        "tools": [
            "Python", "Pandas", "NumPy", "Matplotlib", "Seaborn",
            "Scikit-learn", "Jupyter", "SQL", "Power BI"
        ],
        "projects": [
            "Customer churn prediction",
            "Student performance analysis",
            "Rainfall prediction model",
            "Sales forecasting dashboard"
        ],
        "roadmap": [
            "Master Python, Pandas, and NumPy.",
            "Learn statistics and data visualization.",
            "Practice EDA on real datasets.",
            "Train ML models and compare performance.",
            "Deploy a Streamlit data science app."
        ]
    },
    "Data Analytics": {
        "icon": "📈",
        "tagline": "Analyze business data and communicate clear insights.",
        "what": "Data Analytics focuses on cleaning, analyzing, visualizing, and explaining data to support better decisions.",
        "best_for": "Students who enjoy Excel, SQL, dashboards, business problems, and clear communication.",
        "subjects": [
            "Excel", "SQL", "Statistics", "Data Cleaning", "Dashboard Design",
            "Business Analysis", "Data Visualization", "Report Writing"
        ],
        "tools": [
            "Excel", "SQL", "Power BI", "Tableau", "Python", "Pandas", "Google Sheets"
        ],
        "projects": [
            "Sales dashboard",
            "Student marks analysis",
            "Company KPI dashboard",
            "Customer behavior report"
        ],
        "roadmap": [
            "Learn Excel formulas and pivot tables.",
            "Master SQL queries and joins.",
            "Learn Power BI or Tableau.",
            "Create dashboards using real datasets.",
            "Write insight-focused reports."
        ]
    },
    "Web Development": {
        "icon": "🌐",
        "tagline": "Build websites, dashboards, and online systems.",
        "what": "Web Development is about creating websites and web applications that users can interact with through a browser.",
        "best_for": "Students who like visual design, coding, user interfaces, and building practical online tools.",
        "subjects": [
            "HTML", "CSS", "JavaScript", "Responsive Design", "Frontend Frameworks",
            "Backend Development", "Databases", "APIs", "Deployment"
        ],
        "tools": [
            "HTML", "CSS", "JavaScript", "React", "Node.js",
            "Python", "Flask", "Django", "GitHub", "VS Code"
        ],
        "projects": [
            "Personal portfolio website",
            "Student management system",
            "Career recommender website",
            "AI chatbot web app"
        ],
        "roadmap": [
            "Learn HTML, CSS, and JavaScript.",
            "Build static websites first.",
            "Learn frontend framework basics.",
            "Connect backend and database.",
            "Deploy on GitHub Pages, Render, or Streamlit Cloud."
        ]
    },
    "Cloud Computing": {
        "icon": "☁️",
        "tagline": "Run applications and data systems on cloud platforms.",
        "what": "Cloud Computing focuses on deploying, scaling, storing, and managing applications using cloud services.",
        "best_for": "Students who like infrastructure, deployment, automation, networking, and scalable systems.",
        "subjects": [
            "Networking Basics", "Linux", "Cloud Services", "Virtual Machines",
            "Storage", "Databases", "Containers", "Security", "Monitoring"
        ],
        "tools": [
            "AWS", "Azure", "Google Cloud", "Docker", "Linux",
            "GitHub Actions", "Terraform", "Kubernetes"
        ],
        "projects": [
            "Deploy a Streamlit app on cloud",
            "Host a database-backed web app",
            "Create cloud storage pipeline",
            "Build CI/CD deployment workflow"
        ],
        "roadmap": [
            "Learn Linux and networking basics.",
            "Understand cloud compute, storage, and databases.",
            "Deploy simple apps to the cloud.",
            "Learn Docker and CI/CD.",
            "Practice monitoring and security basics."
        ]
    },
    "Cybersecurity": {
        "icon": "🛡️",
        "tagline": "Protect systems, networks, and data from attacks.",
        "what": "Cybersecurity focuses on identifying vulnerabilities, protecting systems, and responding to security threats.",
        "best_for": "Students who enjoy investigation, networking, Linux, ethical hacking, and security thinking.",
        "subjects": [
            "Networking", "Linux", "Security Fundamentals", "Web Security",
            "Cryptography Basics", "Threat Analysis", "Digital Forensics", "Ethical Hacking"
        ],
        "tools": [
            "Linux", "Wireshark", "Nmap", "Burp Suite", "Metasploit",
            "Python", "SIEM Tools", "TryHackMe"
        ],
        "projects": [
            "Network vulnerability scan report",
            "Password strength checker",
            "Phishing awareness demo",
            "Secure login system"
        ],
        "roadmap": [
            "Learn networking and Linux.",
            "Study security fundamentals.",
            "Practice with safe labs only.",
            "Learn web security and common vulnerabilities.",
            "Create security reports and portfolio writeups."
        ]
    },
    "IoT": {
        "icon": "📡",
        "tagline": "Connect sensors, devices, and software to solve physical-world problems.",
        "what": "IoT combines hardware, sensors, microcontrollers, communication, and software to monitor and control real-world systems.",
        "best_for": "Students who like electronics, sensors, embedded systems, automation, and hardware projects.",
        "subjects": [
            "Electronics Basics", "Microcontrollers", "Sensors", "Embedded C/Python",
            "Wireless Communication", "Cloud IoT", "Data Logging", "PCB Basics"
        ],
        "tools": [
            "Arduino", "ESP32", "Raspberry Pi", "MQTT", "Blynk",
            "Proteus", "Firebase", "ThingsBoard", "Python"
        ],
        "projects": [
            "Smart dairy cold-chain monitor",
            "Food quality monitoring device",
            "Air quality monitoring system",
            "IoT attendance system"
        ],
        "roadmap": [
            "Learn electronics and sensor basics.",
            "Practice Arduino or ESP32 projects.",
            "Send sensor data to a dashboard.",
            "Add alerts and cloud storage.",
            "Design a simple PCB and enclosure."
        ]
    },
    "DevOps": {
        "icon": "⚙️",
        "tagline": "Automate development, testing, deployment, and monitoring.",
        "what": "DevOps connects software development and operations. It focuses on automation, CI/CD, containers, cloud deployment, and monitoring.",
        "best_for": "Students who like systems, automation, deployment, GitHub, Linux, and cloud platforms.",
        "subjects": [
            "Linux", "Git", "CI/CD", "Docker", "Cloud Deployment",
            "Monitoring", "Scripting", "Infrastructure as Code"
        ],
        "tools": [
            "Git", "GitHub Actions", "Docker", "Jenkins", "Linux",
            "AWS", "Kubernetes", "Terraform", "Prometheus"
        ],
        "projects": [
            "CI/CD pipeline for a Python app",
            "Dockerized Streamlit app",
            "Automated deployment workflow",
            "Monitoring dashboard"
        ],
        "roadmap": [
            "Learn Git and Linux commands.",
            "Understand deployment basics.",
            "Dockerize a simple app.",
            "Create a GitHub Actions pipeline.",
            "Deploy and monitor the application."
        ]
    }
}


DEFAULT_SIDE = "Artificial Intelligence"


# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------
def pills(items, class_name="pill"):
    html = "".join([f"<span class='{class_name}'>{item}</span>" for item in items])
    st.markdown(html, unsafe_allow_html=True)


def show_roadmap(steps):
    for i, step in enumerate(steps, start=1):
        st.markdown(
            f"""
            <div class="step-box">
                <b>Step {i}</b><br>
                <span>{step}</span>
            </div>
            """,
            unsafe_allow_html=True
        )


def show_field_overview(side_name):
    side = CAREER_SIDES[side_name]

    st.markdown(
        f"""
        <div class="hero-card">
            <div class="main-title">{side["icon"]} {side_name}</div>
            <div class="subtitle">{side["tagline"]}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    left, right = st.columns([1.3, 1])

    with left:
        st.markdown(
            f"""
            <div class="glass-card">
                <h3>What is this side?</h3>
                <p>{side["what"]}</p>
                <h3>Who should choose this?</h3>
                <p>{side["best_for"]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with right:
        st.markdown(
            """
            <div class="glass-card">
                <h3>Career Readiness Check</h3>
                <p class="small-muted">Do not choose a side only because it sounds popular. Choose it if you are willing to study the core subjects and build projects consistently.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.metric("Learning Depth", "High")
        st.metric("Portfolio Importance", "Very High")

    st.markdown("## 📚 Subjects You Should Learn")
    pills(side["subjects"])

    st.markdown("## 🧰 Tools and Technologies")
    pills(side["tools"], "green-pill")

    st.markdown("## 💡 Beginner Project Ideas")
    pcols = st.columns(2)
    for index, project in enumerate(side["projects"]):
        with pcols[index % 2]:
            st.markdown(
                f"""
                <div class="field-card">
                    <h3>0{index + 1}</h3>
                    <h3>{project}</h3>
                    <p class="small-muted">Build this as a small portfolio project. Keep a README, screenshots, and GitHub link.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("## 🛣️ Simple Learning Path")
    show_roadmap(side["roadmap"])


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("## 🚀 AI Career Navigator")
    st.caption("Digital career exploration + AI recommender")

    page = st.radio(
        "Navigation",
        ["🏠 Home", "🧭 Explore Career Sides", "🎯 AI Recommendation", "📊 Dataset"],
        index=0
    )

    st.markdown("---")
    st.markdown("### ⚙️ Recommendation Settings")
    top_n = st.slider("Number of recommendations", 3, 8, 3)

    st.markdown("### Score Weights")
    skill_weight = st.slider("Skill Similarity", 0.0, 1.0, 0.65, 0.05)
    goal_weight = st.slider("Career Goal", 0.0, 1.0, 0.20, 0.05)
    difficulty_weight = st.slider("Difficulty Level", 0.0, 1.0, 0.10, 0.05)
    interest_weight = st.slider("Interest Match", 0.0, 1.0, 0.05, 0.05)

    total_weight = skill_weight + goal_weight + difficulty_weight + interest_weight

    if total_weight == 0:
        st.error("At least one weight must be greater than zero.")
    else:
        st.success(f"Total weight: {total_weight:.2f}")


weights = {
    "skill": skill_weight / total_weight if total_weight else 0,
    "goal": goal_weight / total_weight if total_weight else 0,
    "difficulty": difficulty_weight / total_weight if total_weight else 0,
    "interest": interest_weight / total_weight if total_weight else 0
}


# ---------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------
if page == "🏠 Home":
    st.markdown(
        """
        <div class="hero-card">
            <div class="main-title">Build Your Digital Tech Career Path</div>
            <div class="subtitle">
                Explore different technology sides, understand what subjects to learn,
                choose your direction, and get AI-powered career recommendations based on your skills.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """
            <div class="glass-card">
                <h2>01</h2>
                <h3>Explore Sides</h3>
                <p>Understand AI, Data Science, Web Development, Cybersecurity, IoT, Cloud, and more.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            """
            <div class="glass-card">
                <h2>02</h2>
                <h3>Learn Subjects</h3>
                <p>See the exact subjects, tools, technologies, and project ideas for each career side.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            """
            <div class="glass-card">
                <h2>03</h2>
                <h3>Get Recommendation</h3>
                <p>Enter your skills and get matched career roles with missing skills and roadmaps.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("## 🔥 Popular Career Sides")

    side_names = list(CAREER_SIDES.keys())
    rows = [side_names[i:i + 4] for i in range(0, len(side_names), 4)]

    for row in rows:
        cols = st.columns(4)
        for col, side_name in zip(cols, row):
            side = CAREER_SIDES[side_name]
            with col:
                st.markdown(
                    f"""
                    <div class="field-card">
                        <h1>{side["icon"]}</h1>
                        <h3>{side_name}</h3>
                        <p>{side["tagline"]}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.markdown(
        """
        <div class="warning-box">
            <b>Mentor note:</b> Do not just make the UI beautiful. Your project becomes strong only when the explanation,
            recommendation logic, dataset, and roadmap are also clear.
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# EXPLORE CAREER SIDES PAGE
# ---------------------------------------------------------
elif page == "🧭 Explore Career Sides":
    selected_side = st.selectbox(
        "Select a technology side",
        list(CAREER_SIDES.keys()),
        index=list(CAREER_SIDES.keys()).index(DEFAULT_SIDE)
    )

    show_field_overview(selected_side)

    st.session_state["selected_goal"] = selected_side

    st.markdown(
        """
        <div class="success-box">
            This selected side is saved for your recommendation page. Open <b>AI Recommendation</b> from the sidebar and continue.
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# RECOMMENDATION PAGE
# ---------------------------------------------------------
elif page == "🎯 AI Recommendation":
    st.markdown(
        """
        <div class="hero-card">
            <div class="main-title">AI Career Recommendation Engine</div>
            <div class="subtitle">
                Enter your current skills and interests. The system ranks career paths using skill similarity,
                goal similarity, difficulty alignment, and interest overlap.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    default_goal = st.session_state.get("selected_goal", DEFAULT_SIDE)

    col1, col2 = st.columns(2)

    with col1:
        skills = st.text_area(
            "Your skills",
            value="Python, SQL, Machine Learning",
            help="Enter skills separated by commas. Example: Python, SQL, Machine Learning"
        )

        career_goal = st.selectbox(
            "Career goal",
            [
                "Artificial Intelligence",
                "Data Science",
                "Data Analytics",
                "Cloud Computing",
                "DevOps",
                "Web Development",
                "Cybersecurity",
                "Mobile Development",
                "IoT",
                "Research",
                "Product Management",
                "Design"
            ],
            index=[
                "Artificial Intelligence",
                "Data Science",
                "Data Analytics",
                "Cloud Computing",
                "DevOps",
                "Web Development",
                "Cybersecurity",
                "Mobile Development",
                "IoT",
                "Research",
                "Product Management",
                "Design"
            ].index(default_goal) if default_goal in [
                "Artificial Intelligence",
                "Data Science",
                "Data Analytics",
                "Cloud Computing",
                "DevOps",
                "Web Development",
                "Cybersecurity",
                "Mobile Development",
                "IoT",
                "Research",
                "Product Management",
                "Design"
            ] else 0
        )

    with col2:
        level = st.selectbox(
            "Current level",
            ["beginner", "intermediate", "advanced"],
            index=1
        )

        interests = st.text_area(
            "Extra interests or preferences",
            value="AI projects, real-world applications, data-driven systems",
            help="Example: automation, research, dashboards, deployment"
        )

    run = st.button("🔍 Generate My Career Roadmap", type="primary")

    if run:
        try:
            results = recommender.recommend(
                skills=skills,
                career_goal=career_goal,
                level=level,
                interests=interests,
                top_n=top_n,
                weights=weights
            )

            st.markdown("## 🎯 Top Career Matches")

            chart_data = results[["role", "match_percentage"]].set_index("role")
            st.bar_chart(chart_data)

            for idx, row in results.iterrows():
                with st.container(border=True):
                    st.markdown(f"## {idx + 1}. {row['role']} — {row['match_percentage']}% Match")

                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Skill", f"{row['skill_similarity']:.2f}")
                    m2.metric("Goal", f"{row['goal_similarity']:.2f}")
                    m3.metric("Difficulty", f"{row['difficulty_alignment']:.2f}")
                    m4.metric("Interest", f"{row['interest_overlap']:.2f}")

                    st.markdown("### 🧠 Why this role matched")
                    st.info(row["explanation"])

                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown("### ✅ Matched Skills")
                        pills(str(row["matched_skills"]).split(","), "green-pill")

                    with c2:
                        st.markdown("### ⚠️ Missing Skills")
                        pills(str(row["missing_skills"]).split(","), "pink-pill")

                    st.markdown("### 🧰 Recommended Tech Stack")
                    pills(str(row["tools"]).split(","))

                    st.markdown("### 🛣️ Personalized Learning Roadmap")
                    roadmap_steps = [step.strip() for step in str(row["roadmap"]).split("→")]
                    show_roadmap(roadmap_steps)

            st.markdown("## 📊 Detailed Score Table")
            st.dataframe(
                results[
                    [
                        "role", "match_percentage", "difficulty",
                        "skill_similarity", "goal_similarity",
                        "difficulty_alignment",
                        "interest_overlap", "matched_skills", "missing_skills"
                    ]
                ],
                use_container_width=True
            )

        except Exception as e:
            st.error(str(e))

    with st.expander("📌 How this system works"):
        st.write(
            """
            This project uses a content-based recommendation approach.

            1. The user enters skills, career goal, level, and interests.
            2. Skills and role requirements are converted into numerical vectors using TF-IDF.
            3. Cosine similarity measures how closely the user profile matches each career role.
            4. A hybrid score combines skill similarity, career goal match, difficulty alignment, and interests.
            5. The system ranks roles and shows recommendations with explanations, missing skills, and a roadmap.
            """
        )


# ---------------------------------------------------------
# DATASET PAGE
# ---------------------------------------------------------
elif page == "📊 Dataset":
    st.markdown(
        """
        <div class="hero-card">
            <div class="main-title">Dataset Explorer</div>
            <div class="subtitle">
                This table contains the career role profiles used by the recommender.
                Improve the system by adding more roles, skill variations, tools, and roadmaps.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.metric("Total Career Roles", len(dataset))
    st.dataframe(dataset, use_container_width=True)

    st.markdown(
        """
        <div class="warning-box">
            <b>Critical improvement:</b> Your recommendation quality depends heavily on this dataset.
            A beautiful UI cannot hide a weak dataset. Add more roles and better skill descriptions for stronger results.
        </div>
        """,
        unsafe_allow_html=True
    )
