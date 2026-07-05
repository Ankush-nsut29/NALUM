from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="student")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    mentor_profile = db.relationship("MentorProfile", backref="user", uselist=False)
    bookings_sent = db.relationship("Booking", foreign_keys="[Booking.student_id]", backref="student")
    threads = db.relationship("ForumThread", backref="author")
    replies = db.relationship("ForumReply", backref="author")


class MentorProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    domain = db.Column(db.String(100))
    company = db.Column(db.String(100))
    experience_years = db.Column(db.Integer)
    bio = db.Column(db.Text)
    availability = db.Column(db.String(50))
    linkedin = db.Column(db.String(200))

    bookings = db.relationship("Booking", foreign_keys="[Booking.mentor_id]", backref="mentor_profile")


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    mentor_id = db.Column(db.Integer, db.ForeignKey("mentor_profile.id"), nullable=False)
    message = db.Column(db.Text)
    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ForumThread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    replies = db.relationship("ForumReply", backref="thread")


class ForumReply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    thread_id = db.Column(db.Integer, db.ForeignKey("forum_thread.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
