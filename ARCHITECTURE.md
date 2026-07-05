# NALUM Platform Architecture & Structure

This document outlines the complete structure of the NALUM (NSUT Alumni Mentorship Platform) Flask application. It explains the purpose of every backend Python file, static asset, and HTML template in the repository.

---

## 🏗️ Project Root

### `app.py`
The main entry point of the Flask application. It initializes the Flask app, configures the SQLite database (`nalum.db`), registers all the different feature blueprints (auth, mentor, booking, forum, dashboard), and contains a CLI command to initialize the database with dummy data.

### `model.py`
Contains the SQLAlchemy database schemas. It defines the tables and relationships:
- **User**: Base account for everyone (Stores `id`, `name`, `email`, `password`, `role`).
- **MentorProfile**: Extended details exclusively for mentors (Stores `domain`, `company`, `experience_years`, `bio`, `availability`, `linkedin`).
- **Booking**: Represents a mentorship session request between a student and a mentor (Stores `status`, `message`, etc.).
- **ForumThread**: A top-level post in the discussion forum.
- **ForumReply**: A reply attached to a specific `ForumThread`.

---

## ⚙️ Backend Blueprints (Features)

The backend logic is modularized into Blueprints for clean code separation:

### `auth.py`
Handles all authentication logic.
- **Routes**: `/login`, `/register`, `/logout`.
- **Purpose**: Validates user credentials, creates new accounts, hashes passwords securely, and manages the user's session state.

### `mentor.py`
Handles the core mentorship browsing experience.
- **Routes**: `/mentors` (list all mentors), `/mentor/<id>` (view a specific mentor).
- **Purpose**: Fetches mentor profiles from the database and passes them to the templates for display.

### `booking.py`
Handles the session scheduling logic.
- **Routes**: `/book/<mentor_id>` (submit a request), `/booking/<id>/status` (accept/reject a request).
- **Purpose**: Allows students to send a message requesting a session, and exposes an API endpoint for mentors to approve or reject those requests.

### `dashboard.py`
Handles the user's personal hub.
- **Routes**: `/dashboard`, `/dashboard/profile/edit`
- **Purpose**: Aggregates all data relevant to the logged-in user. It fetches their profile details, their bookings (incoming for mentors, outgoing for students), and their recent forum activity. It also handles the form submission to update a mentor's profile.

### `forum.py`
Handles the community discussion boards.
- **Routes**: `/forum`, `/forum/new`, `/forum/<id>`, `/forum/<id>/reply`.
- **Purpose**: Fetches threads, handles creating new discussion topics, viewing a thread, and posting replies via a JSON API endpoint.

---

## 🎨 Static Assets (`/static/`)

### `style.css`
The master stylesheet for the entire application.
- Uses **CSS Variables** (custom properties) at the `:root` level to define the NALUM design system (deep crimson brand colors, spacing tokens, border radii, shadows).
- Implements a modern, clean, utility-first-like component system (`.card`, `.btn`, `.flex-col`) without relying on heavy external frameworks.

### `main.js`
The master JavaScript file handling all client-side interactivity.
- **Forum Replies**: Submits replies asynchronously using `fetch` and dynamically injects the new reply into the DOM without a page reload.
- **Domain Filtering**: Handles the logic for filtering mentor cards on the "Browse Mentors" page when a domain pill is clicked.
- **Booking Status**: Handles the Accept/Reject buttons on the dashboard, making a `fetch` request and updating the UI badge color instantly.
- **Dashboard Tabs**: Handles the logic for switching between the Profile, Bookings, and Forum tabs on the dashboard.

---

## 🖼️ HTML Templates (`/templates/`)

The views are constructed using Jinja2 templating, allowing for dynamic data injection and layout inheritance.

### Core Layout
- **`base.html`**: The master wrapper for every page. It contains the standard `<html>`, `<head>`, the top navigation bar, and the site footer. It defines a `{% block content %}` where other templates inject their specific page content.
- **`index.html`**: The landing page. Features a hero section introducing the platform and a "Bento Box" style call-to-action for logging in or signing up.

### Authentication (`/auth/`)
- **`login.html`**: A clean, centered card form for users to log into their account.
- **`register.html`**: The sign-up form. Includes a dropdown to select the account type (Student or Mentor).

### Mentorship (`/mentor/`)
- **`list.html`**: The "Browse Mentors" page. Displays a grid of mentor cards and interactive domain filter pills at the top.
- **`detail.html`**: The full profile view for a single mentor. Shows their bio, experience, LinkedIn link, and includes a text area form for a student to write a session request message.

### User Dashboard (`/dashboard/`)
- **`index.html`**: A multi-tab interface acting as the user's control center:
  - **My Profile**: Shows user details. If the user is a mentor, it includes a toggleable inline form to edit their domains (checkboxes), company, bio, etc.
  - **Bookings**: Lists all pending, approved, and rejected session requests. Mentors see Action buttons here.
  - **Forum Activity**: Lists all the threads the user has created and the replies they've posted.

### Community Forum (`/forum/`)
- **`list.html`**: Displays a list of all active discussion threads, showing the title, author, date, and a snippet of the conversation, along with a "View Replies" button.
- **`new.html`**: A simple form to input a title and body to start a brand new discussion thread.
- **`thread.html`**: The detail view of a discussion. Shows the original post at the top, followed by a chronological list of replies, and a form at the bottom to submit a new reply.
