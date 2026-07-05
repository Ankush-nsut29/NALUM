from flask import Blueprint, render_template, request, session, redirect, url_for
from model import db, MentorProfile, User, Booking

mentor_bp = Blueprint("mentor", __name__)

@mentor_bp.route("/mentors")
def list():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    mentors = MentorProfile.query.join(User).filter(User.role == "mentor").all()
    return render_template("mentor/list.html", mentors=mentors)

@mentor_bp.route("/mentor/<int:id>")
def detail(id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    mentor = MentorProfile.query.get_or_404(id)
    
    existing_booking = None
    if session.get("user_id"):
        user = db.session.get(User, session["user_id"])
        if user and user.role == "student":
            existing_booking = Booking.query.filter_by(
                student_id=user.id,
                mentor_id=mentor.id,
                status="pending"
            ).first()

    return render_template("mentor/detail.html", mentor=mentor, existing_booking=existing_booking)
