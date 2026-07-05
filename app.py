import os
from flask import Flask, render_template, session
from werkzeug.security import generate_password_hash
from model import db, User, MentorProfile, Booking, ForumThread, ForumReply
from auth import auth_bp
from mentor import mentor_bp
from booking import booking_bp
from forum import forum_bp
from dashboard import dashboard_bp


def _seed_if_empty():
    if User.query.first() is not None:
        return

    mentor1 = User(name="Rahul Sharma",  email="mentor1@nsut.ac.in",
                   password=generate_password_hash("password123"), role="mentor")
    mentor2 = User(name="Sneha Gupta",   email="mentor2@nsut.ac.in",
                   password=generate_password_hash("password123"), role="mentor")
    student = User(name="Amit Kumar",    email="student@nsut.ac.in",
                   password=generate_password_hash("password123"), role="student")
    db.session.add_all([mentor1, mentor2, student])
    db.session.commit()

    profile1 = MentorProfile(
        user_id=mentor1.id, domain="Web Dev", company="Google",
        experience_years=4,
        bio="Passionate about building scalable web applications. Happy to guide juniors on full-stack development and system design.",
        availability="Available", linkedin="https://linkedin.com/"
    )
    profile2 = MentorProfile(
        user_id=mentor2.id, domain="ML/AI", company="Microsoft",
        experience_years=3,
        bio="Working on generative AI and natural language processing. I can help with ML interviews and research papers.",
        availability="Limited", linkedin="https://linkedin.com/"
    )
    db.session.add_all([profile1, profile2])
    db.session.commit()

    thread1 = ForumThread(title="How to prepare for Google STEP?",
                          body="I am a first-year student and want to apply for STEP internship next year. What should I study?",
                          user_id=student.id)
    thread2 = ForumThread(title="Best resources for System Design",
                          body="Could mentors share some good resources to practice system design for interviews?",
                          user_id=mentor1.id)
    thread3 = ForumThread(title="Resume Review Request",
                          body="Any mentor available to review my resume? I am targeting ML roles.",
                          user_id=student.id)
    db.session.add_all([thread1, thread2, thread3])
    db.session.commit()

    db.session.add(ForumReply(body="Focus on Data Structures and Algorithms. Practice on LeetCode.",
                              user_id=mentor1.id, thread_id=thread1.id))
    db.session.add(ForumReply(body="Also, make sure your resume highlights any personal projects you have built.",
                              user_id=mentor2.id, thread_id=thread1.id))
    db.session.add(ForumReply(body="I highly recommend 'Designing Data-Intensive Applications' by Martin Kleppmann.",
                              user_id=mentor2.id, thread_id=thread2.id))
    db.session.add(ForumReply(body="Grokking the System Design Interview is also a great starting point.",
                              user_id=mentor1.id, thread_id=thread2.id))
    db.session.add(ForumReply(body="Send it over, I can take a look this weekend.",
                              user_id=mentor2.id, thread_id=thread3.id))
    db.session.add(ForumReply(body="I can also review it if it's related to general software engineering.",
                              user_id=mentor1.id, thread_id=thread3.id))

    db.session.add(Booking(
        student_id=student.id, mentor_id=profile1.id,
        message="Hi Rahul, I would love to discuss web dev career paths with you.",
        status="pending"
    ))
    db.session.commit()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "nalum-secret-key")

    # On Render, DATABASE_URL is set automatically by the PostgreSQL addon.
    # Locally, fall back to SQLite so you don't need Postgres installed.
    db_url = os.environ.get("DATABASE_URL", "sqlite:///nalum.db")
    # Render provides postgres:// but SQLAlchemy 1.4+ needs postgresql://
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(mentor_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(forum_bp)
    app.register_blueprint(dashboard_bp)

    with app.app_context():
        db.create_all()
        _seed_if_empty()

    @app.route("/")
    def index():
        mentor_count     = MentorProfile.query.count()
        session_count    = Booking.query.filter_by(status="approved").count()
        discussion_count = ForumThread.query.count()
        return render_template(
            "index.html",
            mentor_count=mentor_count,
            session_count=session_count,
            discussion_count=discussion_count
        )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
