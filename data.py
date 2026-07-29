"""Python mirror of the frontend's src/data/*.ts content.

Kept in sync by hand for now. This is what the /chat endpoint's keyword
matcher uses today, and what the LangGraph agent's tools will read from
once it exists (see README.md "Implementation Order").
"""

PROJECTS = [
    {
        "title": "SORT IT OUT - The Baby Version",
        "tech": "HTML, CSS, JavaScript",
        "description": "Visualizes classic sorting algorithms using raw HTML, CSS, and vanilla JavaScript.",
        "github": "https://github.com/Sahoo-Achyutananda/Sorting_Algorithm_Visualizer",
        "demo": "https://sorting-visualizer-achyutananda-sahoo.netlify.app/index.html",
        "thumbnail": "/projects/sortv1.png",
    },
    {
        "title": "SORT IT OUT - React Version",
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
        "title": "2 Colors",
        "tech": "HTML, CSS, JavaScript",
        "description": "Generates 2 random colors per refresh with hex/RGB values and linear/conic/radial gradients.",
        "github": "https://github.com/Sahoo-Achyutananda/2_Colors",
        "demo": "https://sahoo-achyutananda.github.io/2_Colors/",
        "thumbnail": "/projects/2colors.png",
    },
    {
        "title": "Detection of Customer Churn in the Banking Sector",
        "tech": "Python",
        "description": "ML model comparing XGBoost, Random Forest, SVM, Decision Tree, and Logistic Regression for churn prediction.",
        "github": None,
        "demo": None,
        "thumbnail": None,
    },
]

EXPERIENCE = [
    {
        "title": "Software Engineer Intern - Ciranta IT Services (formerly Aspirant Labs)",
        "duration": "Oct 2023 - Apr 2024",
        "location": "Chennai, India",
        "highlights": [
            "Customized Odoo ERP systems for clients",
            "Built custom modules like Appraisal System and Employee Portal",
            "Integrated APIs and customized CRM, Sales, and Marketing modules",
            "Received Rising Star Award",
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
