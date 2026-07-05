<div align="center">
  <img src="https://www.guidanceforever.org/wp-content/uploads/2023/10/netaji-subhas-university-of-technology-nsut-delhi-logo.png" alt="NSUT Logo" height="100"/>

  <h1>NALUM</h1>
  <p><strong>NSUT Alumni Mentorship Platform</strong></p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white"/>
    <img src="https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask&logoColor=white"/>
    <img src="https://img.shields.io/badge/PostgreSQL-Render-336791?style=flat-square&logo=postgresql&logoColor=white"/>
    <img src="https://img.shields.io/badge/Deployed-Render-46E3B7?style=flat-square&logo=render&logoColor=white"/>
  </p>

  <p>Connect NSUT students with alumni mentors for career guidance, 1-on-1 sessions, and community discussions.</p>
</div>

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 **Auth** | Secure login & registration with hashed passwords (Werkzeug) |
| 👩‍🏫 **Mentor Browse** | Filter alumni by Tech / Non-Tech / Core / Fintech |
| 📅 **Session Booking** | Students request 1-on-1 sessions; mentors accept or reject |
| 💬 **Community Forum** | Post threads, reply in real-time (async fetch, no page reload) |
| 📊 **Dashboard** | Personalized hub — profile, bookings, forum activity |

---

## 🛠️ Tech Stack

### Backend
| Layer | Technology |
|---|---|
| **Language** | Python 3.11 |
| **Framework** | Flask 3.0 (modular Blueprints) |
| **ORM** | Flask-SQLAlchemy 3.1 |
| **Database** | PostgreSQL (Render) / SQLite (local dev) |
| **Auth** | Session-based auth + Werkzeug password hashing |
| **Server** | Gunicorn (WSGI production server) |

### Frontend
| Layer | Technology |
|---|---|
| **Templating** | Jinja2 (server-side rendering) |
| **Styling** | Vanilla CSS with custom design system (CSS variables) |
| **Interactivity** | Vanilla JavaScript (Fetch API, DOM manipulation) |
| **Typography** | Google Fonts — Inter |

### Infrastructure
| Layer | Technology |
|---|---|
| **Hosting** | Render (Web Service + PostgreSQL) |
| **Version Control** | GitHub |
| **Python Version** | Pinned via `.python-version` |

---

## 🏗️ Architecture

```
NALUM/
├── app.py              # App factory — initializes Flask, DB, Blueprints, seed data
├── model.py            # SQLAlchemy models (User, MentorProfile, Booking, ForumThread, ForumReply)
│
├── auth.py             # Blueprint: /login  /register  /logout
├── mentor.py           # Blueprint: /mentors  /mentor/<id>
├── booking.py          # Blueprint: /book/<mentor_id>  /booking/<id>/status
├── forum.py            # Blueprint: /forum  /forum/new  /forum/<id>  /forum/<id>/reply
├── dashboard.py        # Blueprint: /dashboard  /dashboard/profile/edit
│
├── static/
│   ├── style.css       # Design system — CSS variables, components, layout utilities
│   └── main.js         # Client-side: domain filtering, async replies, booking status, tabs
│
└── templates/
    ├── base.html        # Master layout (navbar, footer, block content)
    ├── index.html       # Landing page — hero, features, stats
    ├── auth/            # login.html, register.html
    ├── mentor/          # list.html (browse + filter), detail.html (profile + booking form)
    ├── dashboard/       # index.html (tabs: Profile / Bookings / Forum Activity)
    └── forum/           # list.html, new.html, thread.html
```

---

## 🔄 Application Flow

```
User visits /
    │
    ├── Not logged in → Landing page → Login / Register
    │
    └── Logged in
            │
            ├── [Student]
            │     ├── /mentors → Browse & filter by domain → View profile
            │     ├── /mentor/<id> → Send booking request with message
            │     └── /dashboard → See pending/approved/rejected bookings + forum activity
            │
            ├── [Mentor]
            │     ├── /dashboard → See incoming booking requests
            │     ├── Accept / Reject via PATCH API (no page reload)
            │     └── Edit profile: domain, company, bio, LinkedIn, availability
            │
            └── [Both]
                  ├── /forum → Browse community threads
                  ├── /forum/new → Start a new discussion
                  └── /forum/<id> → Read thread + post reply (async, no reload)
```

---

## 🗃️ Database Models

```
User
 ├── id, name, email, password (hashed), role (student/mentor), created_at
 ├── → MentorProfile (one-to-one)
 ├── → Booking (one-to-many, as student)
 ├── → ForumThread (one-to-many)
 └── → ForumReply (one-to-many)

MentorProfile
 ├── user_id (FK), domain, company, experience_years, bio, availability, linkedin
 └── → Booking (one-to-many, as mentor)

Booking
 └── student_id (FK), mentor_id (FK), message, status (pending/approved/rejected)

ForumThread
 ├── title, body, user_id (FK), created_at
 └── → ForumReply (one-to-many)

ForumReply
 └── body, user_id (FK), thread_id (FK), created_at
```

---

## 🚀 Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/Ankush-nsut29/NALUM.git
cd NALUM

# 2. Create a virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run locally (uses SQLite automatically)
python app.py
```

Open `http://127.0.0.1:5000` — the DB is seeded with demo mentors and a student on first run.

**Demo accounts:**
| Role | Email | Password |
|------|-------|----------|
| Mentor | mentor1@nsut.ac.in | password123 |
| Mentor | mentor2@nsut.ac.in | password123 |
| Student | student@nsut.ac.in | password123 |

---

## ☁️ Deployment (Render)

The app auto-switches between **SQLite** (local) and **PostgreSQL** (production) via the `DATABASE_URL` environment variable.

| Service | Config |
|---|---|
| **Web Service** | Runtime: Python, Start: `gunicorn app:app` |
| **Database** | Render PostgreSQL (Free tier) |
| **Env Vars** | `DATABASE_URL` (from Render DB), `SECRET_KEY` |

---

## 👤 Author

**Ankush Marwaha** — NSUT  
[GitHub](https://github.com/Ankush-nsut29)
