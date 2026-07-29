"""Python mirror of the frontend's src/data/*.ts content.

Kept in sync by hand for now. This is what the /chat endpoint's keyword
matcher uses today, and what the LangGraph agent's tools will read from
once it exists (see README.md "Implementation Order").
"""

from datetime import date

DOB = date(2002, 2, 23)


def get_age() -> int:
    today = date.today()
    years = today.year - DOB.year
    if (today.month, today.day) < (DOB.month, DOB.day):
        years -= 1
    return years


PROFILE = {
    "name": "Achyutananda Sahoo",
    "email": "sahoo.official.work@gmail.com",
    "linkedin": "https://www.linkedin.com/in/achyutananda-sahoo",
    "website": "https://iamsahoo.netlify.app",
    "location": "Kendujhar, Odisha, India",
    "currentStatus": "Pursuing an M.Tech in Computer Science and Information Security (CSIS) at IIIT-Hyderabad",
    "mostRecentRole": "Technology Program Intern at Wells Fargo International, Hyderabad (May 2026 - Jul 2026)",
    "education": [
        {
            "institution": "International Institute of Information Technology, Hyderabad (IIIT-H)",
            "degree": "M.Tech, Computer Science and Information Security",
            "period": "2025 - present",
        },
        {
            "institution": "Saveetha School of Engineering, Chennai",
            "degree": "B.E., Computer Science and Engineering",
            "period": "2020 - 2024",
            "honors": "CGPA 9.44/10, 1st rank (2nd-4th yr), Best Outgoing Student 2024",
        },
    ],
    "skills": {
        "languages": ["C/C++", "Python", "TypeScript", "JavaScript"],
        "mlAi": [
            "Google ADK",
        ],
        "backend": ["Node.js", "PostgreSQL", "pgvector", "FastAPI"],
        "tools": ["Git", "GitHub", "VS Code", "Postman"],
    },
    "summary": (
        "Software engineer pursuing an M.Tech in CSIS at IIIT-Hyderabad (GATE CS 2025 AIR "
        "1814). Most recently built an autonomous agentic AI system at Wells Fargo using "
        "Google ADK, LangChain, and LangGraph to digitize a manual banking workflow, cutting "
        "turnaround time from hours to minutes. Also works across ML (FAISS, "
        "sentence-transformers), backend (Python, TypeScript, PostgreSQL), and occasionally "
        "freelances as a graphic designer."
    ),
}


def get_profile() -> dict:
    return {**PROFILE, "age": get_age()}


PROJECTS = [
    {
        "title": "mygit - Git Implementation from Scratch with RAG",
        "tech": "TypeScript, Node.js, PostgreSQL, pgvector, OpenAI API",
        "description": (
            "Implementing Git's core object model (blob/tree/commit) with SHA-1 "
            "content-addressed storage and zlib compression, including a staging area, refs, "
            "and 7 core commands. Building push/pull/clone over a custom JSON/HTTP protocol "
            "with compare-and-swap for non-fast-forward rejection. Planning a RAG pipeline to "
            "embed code blobs on push and answer natural-language codebase questions via "
            "pgvector similarity search and GPT-4o synthesis."
        ),
        "github": "https://github.com/Sahoo-Achyutananda/mygit",
        "demo": None,
        "thumbnail": None,
    },
    {
        "title": "Personalised Indian Recipe Recommender",
        "tech": "Python, Sentence-Transformers, FAISS, Streamlit",
        "description": (
            "A content-based recommender over 6,865 Indian recipes using sentence-transformer "
            "embeddings (all-MiniLM-L6-v2) and FAISS-accelerated cosine similarity search. A "
            "hybrid semantic + keyword scoring formula fixes ingredient-dilution issues; FAISS "
            "reduced query latency from 18ms to under 1ms. Shipped as a multi-page Streamlit "
            "app with live parameter tuning, favourites, and explainable recommendations."
        ),
        "github": None,
        "demo": None,
        "thumbnail": None,
    },
    {
        "title": "Mini POSIX Shell",
        "tech": "C++, STL",
        "description": "A terminal REPL supporting commands (cd, ls, echo, pinfo), I/O redirection, and pipelining.",
        "github": None,
        "demo": None,
        "thumbnail": None,
    },
    {
        "title": "SORT IT OUT",
        "tech": "React, Tailwind CSS, Vite",
        "description": "A React + Tailwind sorting visualizer with a Race Mode (algorithms compete in real-time) and Play Mode.",
        "github": "https://github.com/Sahoo-Achyutananda/sort_it_out_v4",
        "demo": "https://sort-it-out-v4.netlify.app/",
        "thumbnail": "/projects/sortv4.png",
    },
    {
        "title": "Snake Game (C++)",
        "tech": "C++, Console",
        "description": "A console-based snake game written in C++, no graphics, just terminal fun.",
        "github": "https://github.com/yourusername/snake-game-cpp",
        "demo": None,
        "thumbnail": "/projects/snake.png",
    },
    {
        "title": "Customer Churn Prediction in Banking Sector",
        "tech": "Python, Scikit-learn, XGBoost, Pandas",
        "description": (
            "Built and benchmarked ML models for churn prediction with Target Driven Encoding "
            "on categorical features. Random Forest achieved 86.14% accuracy, outperforming "
            "XGBoost (85.25%), SVM (79.81%), Logistic Regression (79.81%), and Decision Tree "
            "(78.62%). Validated with independent-sample T-tests (p=0.001) across 30 "
            "randomized train-test splits."
        ),
        "github": None,
        "demo": None,
        "thumbnail": None,
    },
]

EXPERIENCE = [
    {
        "title": "Technology Program Intern - Wells Fargo International",
        "duration": "May 2026 - Jul 2026",
        "location": "Hyderabad, India",
        "highlights": [
            "Built an autonomous Agentic AI system (Google ADK, LangChain, LangGraph) to digitize a manual banking inquiry workflow",
            "Reduced turnaround time from 2-8 hours to 20 minutes",
        ],
    },
    {
        "title": "Software Engineer Intern - Ciranta IT Services (formerly Aspirant Labs)",
        "duration": "Oct 2023 - Apr 2024",
        "location": "Chennai, India",
        "highlights": [
            "Developed and customized Odoo ERP modules across HR, CRM, and marketing domains",
            "Built an Employee Portal for attendance tracking, replacing a third-party tool (100% internal adoption)",
            "Designed a Custom Appraisal System to digitize manual processes",
            "Integrated Zoom API and exposed custom REST APIs for Odoo module data",
        ],
    },
    {
        "title": "Graphic Designer - Lose Kilo",
        "duration": "Sep 2024 - Nov 2024",
        "location": None,
        "highlights": [
            "Developed workout and nutrition guides",
            "Designed branding templates for digital services",
        ],
    },
    {
        "title": "Graphic Designer - Lose Kilo",
        "duration": "Mar 2023 - May 2023",
        "location": None,
        "highlights": [
            "Designed logo, ad creatives, and digital manuals",
            "Worked remotely with a fitness startup",
        ],
    },
    {
        "title": "Graphic Designer - Being Assured",
        "duration": "Aug 2022 - Jan 2023",
        "location": None,
        "highlights": [
            "Designed social media posts and ad creatives",
            "Created landing page designs and performed market research",
        ],
    },
]

CERTIFICATES = [
    {"src": "/certs/Picture1.jpg", "title": "Udemy C++ Certification"},
    {"src": "/certs/Picture2.jpg", "title": "Udemy C++ DSA Certificate"},
    {"src": "/certs/Picture4.png", "title": "Cisco - Python Essentials Certification"},
    {"src": "/certs/Picture6.png", "title": "Rising STAR Award - Ciranta IT Services"},
    {"src": "/certs/Picture7.jpg", "title": "Third Year College Topper"},
    {"src": "/certs/Picture8.jpg", "title": "Second Year College Topper"},
]

AWARDS = [
    {"title": "GATE CS 2025", "description": "AIR 1814 (98.94 percentile)"},
    {"title": "PGEE", "description": "Rank 150"},
    {"title": "Rising Star Award", "description": "Ciranta IT Services (2023)"},
    {"title": "800+ DSA Problems", "description": "Solved across LeetCode & GeeksforGeeks"},
]


def projects_to_cards() -> list[dict]:
    cards = []
    for p in PROJECTS:
        link = p["github"] or p["demo"]
        link_label = "GitHub" if link == p["github"] else "Live Demo"
        cards.append(
            {
                "title": p["title"],
                "subtitle": p["tech"],
                "description": p["description"],
                "link": link,
                "linkLabel": link_label if link else None,
                "image": p["thumbnail"],
            }
        )
    return cards


def experience_to_cards() -> list[dict]:
    cards = []
    for e in EXPERIENCE:
        subtitle = e["duration"] + (f" · {e['location']}" if e["location"] else "")
        cards.append(
            {
                "title": e["title"],
                "subtitle": subtitle,
                "description": " · ".join(e["highlights"]),
                "link": None,
                "linkLabel": None,
                "image": None,
            }
        )
    return cards


def certificates_to_cards() -> list[dict]:
    return [
        {
            "title": c["title"],
            "subtitle": None,
            "description": None,
            "link": None,
            "linkLabel": None,
            "image": c["src"],
        }
        for c in CERTIFICATES
    ]


def awards_to_cards() -> list[dict]:
    return [
        {
            "title": a["title"],
            "subtitle": None,
            "description": a["description"],
            "link": None,
            "linkLabel": None,
            "image": None,
        }
        for a in AWARDS
    ]
