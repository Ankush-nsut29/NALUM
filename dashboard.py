from flask import Blueprint, render_template, session, redirect, url_for, request
from model import db, User, Booking, ForumThread, ForumReply

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
def index():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    user_id = session["user_id"]
    user = db.session.get(User, user_id)
    
    context = {
        "user": user,
    }
    
    if user.role == "mentor":
        if user.mentor_profile:
            bookings = Booking.query.filter_by(mentor_id=user.mentor_profile.id).order_by(Booking.created_at.desc()).all()
            context["bookings"] = bookings
        else:
            context["bookings"] = []
    else:
        bookings = Booking.query.filter_by(student_id=user.id).order_by(Booking.created_at.desc()).all()
        context["bookings"] = bookings
        
    threads = ForumThread.query.filter_by(user_id=user.id).order_by(ForumThread.created_at.desc()).all()
    replies = ForumReply.query.filter_by(user_id=user.id).order_by(ForumReply.created_at.desc()).all()
    
    context["threads"] = threads
    context["replies"] = replies
    
    return render_template("dashboard/index.html", **context)

@dashboard_bp.route("/dashboard/profile/edit", methods=["POST"])
def edit_profile():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    user = db.session.get(User, session["user_id"])
    if user.role == "mentor" and user.mentor_profile:
        domains = request.form.getlist("domain")
        user.mentor_profile.domain = ", ".join(domains)
        user.mentor_profile.company = request.form.get("company")
        user.mentor_profile.experience_years = request.form.get("experience_years", type=int, default=0)
        user.mentor_profile.availability = request.form.get("availability")
        user.mentor_profile.linkedin = request.form.get("linkedin")
        user.mentor_profile.bio = request.form.get("bio")
        db.session.commit()
    
    return redirect(url_for("dashboard.index"))
