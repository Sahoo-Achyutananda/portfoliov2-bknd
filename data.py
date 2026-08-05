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
    "socials": {
        "github": "https://github.com/Sahoo-Achyutananda",
        "linkedin": "https://www.linkedin.com/in/achyutananda-sahoo",
        "leetcode": "https://leetcode.com/u/Achyutananda_Sahoo/",
        "geeksforgeeks": "https://www.geeksforgeeks.org/user/achu23022002/",
        "email": "sahoo.official.work@gmail.com",
    },
    "location": "Kendujhar, Odisha, India",
    "hobbies": "Painting and graphic design",
    "currentStatus": "Pursuing an M.Tech in Computer Science and Information Security (CSIS) at IIIT-Hyderabad",
    "mostRecentRole": "Technology Program Intern at Wells Fargo International, Hyderabad (May 2026 – Jul 2026)",
    "education": [
        {
            "institution": "International Institute of Information Technology, Hyderabad (IIIT-H)",
            "degree": "M.Tech, Computer Science and Information Security",
            "period": "2025 - present",
            "honors": "CGPA 8.76/10 (Combining 1st and 2nd semester)"
        },
        {
            "institution": "Saveetha School of Engineering, Chennai",
            "degree": "B.E., Computer Science and Engineering",
            "period": "2020 - 2024",
            "honors": "CGPA 9.44/10, 1st rank (2nd-4th yr), Best Outgoing Student 2024",
        },
        {
            "institution": "Rabindra Vidya Niketan, Keonjhar, Odisha",
            "degree": "11th and 12th, CBSE (Science - PCMB)",
            "period": "Apr 2017 - Jul 2019",
            "honors": "Grade: 85.6%",
        },
        {
            "institution": "Atmiya Vidyapeeth, Gandhidham, Gujarat",
            "degree": "7th to 10th, CBSE",
            "period": "May 2013 - Mar 2017",
            "honors": "Grade: 10 CGPA",
        },
        {
            "institution": "Mangadu Public School, Kovur, Tamil Nadu",
            "degree": "5th and 6th, CBSE",
            "period": "Mar 2011 - Mar 2013",
        },
        {
            "institution": "St John's Matriculation Higher Secondary School, Chennai, Tamil Nadu",
            "degree": "1st to 4th, State Board (Tamil Nadu)",
            "period": "Mar 2007 - Mar 2011",
        },
    ],
    "skills": {
        "languages": ["C/C++", "Python", "TypeScript", "JavaScript"],
        "mlAi": [
            "Google ADK",
        ],
        "backend": ["Node.js", "PostgreSQL", "FastAPI"],
        "tools": ["Git", "GitHub", "VS Code", "Postman"],
    },
    "summary": (
        "Software engineer pursuing an M.Tech in CSIS at IIIT-Hyderabad (GATE CS 2025 AIR "
        "1814). Most recently built a generative AI system at Wells Fargo to digitize a manual banking workflow, cutting "
        "turnaround time from hours to minutes."
    ),
}


def get_profile() -> dict:
    return {**PROFILE, "age": get_age()}


PROJECTS = [
    {
        "title": "mygit",
        "tech": "TypeScript, Node.js, PostgreSQL",
        "description": (
            "Implementing Git's core object model (blob/tree/commit) with SHA-1 "
            "content-addressed storage and zlib compression, including a staging area, refs, "
            "and 7 core commands. Building push/pull/clone over a custom JSON/HTTP protocol "
            "with compare-and-swap for non-fast-forward rejection. Also implemented diff (using Myer's diff algorithm) and merge (3 way merge algorithm)"
        ),
        "github": "https://github.com/Sahoo-Achyutananda/mygit",
        "demo": None,
        "thumbnail": None,
    },
    {
        "title": "P2P File Transfer System",
        "tech": "C++, STL",
        "description": "A BitTorrent-style peer-to-peer file sharing system with a central tracker for coordination and direct peer-to-peer piece transfer. Supports multi-tracker fault tolerance via Primary-Secondary replication with automatic failover, SHA1-verified chunked file transfer, and concurrent downloads via a custom thread pool. Built with raw POSIX sockets and pthreads for full control over the networking and concurrency layers.",
        "github": None,
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
        "title": "Sort It Out - A Sorting Visualizer",
        "tech": "React, Tailwind CSS, Vite",
        "description": "A React + Tailwind sorting visualizer with a Race Mode (algorithms compete in real-time) and Play Mode.",
        "github": "https://github.com/Sahoo-Achyutananda/sort_it_out_v4",
        "demo": "https://sort-it-out-v4.netlify.app/",
        "thumbnail": None,
    },
    {
        "title": "Snake Game (C++)",
        "tech": "C++, Console",
        "description": "A console-based snake game written in C++, no graphics, just terminal fun.",
        "github": "https://github.com/yourusername/snake-game-cpp",
        "demo": None,
        "thumbnail": None,
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
        "category": "Internships",
        "duration": "May 2026 – Jul 2026",
        "location": "Hyderabad, India",
        "highlights": [
            "Built an autonomous generative AI system to digitize a manual banking inquiry workflow",
            "Reduced turnaround time from 2+ hours to 20 minutes, optimized existing workflows by reducing total token consumption per llm call and updating system architecture",
        ],
    },
    {
        "title": "Software Engineer Intern - Ciranta IT Services (formerly Aspirant Labs)",
        "category": "Internships",
        "duration": "Oct 2023 – Apr 2024",
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
        "category": "Freelance",
        "duration": "Sep 2024 – Nov 2024",
        "location": "Remote",
        "highlights": [
            "Developed workout and nutrition guides",
            "Designed branding templates for digital services",
        ],
    },
    {
        "title": "Graphic Designer - Lose Kilo",
        "category": "Freelance",
        "duration": "Mar 2023 – May 2023",
        "location": "Remote",
        "highlights": [
            "Designed logo, ad creatives, and digital manuals",
            "Worked remotely with a fitness startup",
        ],
    },
    {
        "title": "Graphic Designer - Being Assured",
        "category": "Freelance",
        "duration": "Aug 2022 – Jan 2023",
        "location": "Remote",
        "highlights": [
            "Designed social media posts and ad creatives",
            "Created landing page designs and performed market research",
        ],
    },
]

CERTIFICATES = [
    {"src": "/certs/Picture1.jpg", "title": "Udemy C++ Certification"},
    {"src": "/certs/Picture2.jpg", "title": "Udemy C++ DSA Certificate"},
    {"src": "/certs/Picture4.png", "title": "Cisco – Python Essentials Certification"},
    {"src": "/certs/Picture6.png", "title": "Rising STAR Award – Ciranta IT Services"},
    {"src": "/certs/Picture7.jpg", "title": "Third Year College Topper"},
    {"src": "/certs/Picture8.jpg", "title": "Second Year College Topper"},
]

AWARDS = [
    {"title": "GATE CS 2025", "description": "AIR 1814 (98.94 percentile)"},
    {"title": "PGEE", "description": "Rank 150"},
    {"title": "Rising Star Award", "description": "Ciranta IT Services (2023)"},
    {"title": "800+ DSA Problems", "description": "Solved across LeetCode & GeeksforGeeks"},
]

PAINTINGS = [
    {"src": "/paintings/oldman.jpg", "title": "Old Man"},
    {"src": "/paintings/tamasha.jpg", "title": "Agar Tum SAaaathh Hoo .. "},
    {"src": "/paintings/captain.jpg", "title": "Oh Captain My Captain"},
    {"src": "/paintings/john.png", "title": "Babayaga"},
    {"src": "/paintings/kiara.png", "title": "Kaira nahi, it's Kiara"},
    {"src": "/paintings/infinity.jpg", "title": "Mudhal Nee Mudivum Nee"},
]

RESUME = {
    "title": "Resume.pdf",
    "description": "View or download my full resume.",
    "link": "/RESUME_ACHYUTANANDA_SAHOO.pdf",
    "linkLabel": "Open Resume",
}


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
        subtitle = f"{e['category']} · {e['duration']}"
        if e["location"]:
            subtitle += f" · {e['location']}"
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


def education_to_cards() -> list[dict]:
    return [
        {
            "title": e["degree"],
            "subtitle": f"{e['institution']} · {e['period']}",
            "description": e.get("honors"),
            "link": None,
            "linkLabel": None,
            "image": None,
        }
        for e in PROFILE["education"]
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


def paintings_to_cards() -> list[dict]:
    return [
        {
            "title": p["title"],
            "subtitle": None,
            "description": None,
            "link": None,
            "linkLabel": None,
            "image": p["src"],
        }
        for p in PAINTINGS
    ]


def resume_to_cards() -> list[dict]:
    return [{**RESUME, "subtitle": None, "image": None}]
