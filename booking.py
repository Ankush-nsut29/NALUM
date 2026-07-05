from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from model import db, Booking, User, MentorProfile

booking_bp = Blueprint("booking", __name__)

@booking_bp.route("/book/<int:mentor_id>", methods=["POST"])
def book(mentor_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    user_id = session["user_id"]
    user = db.session.get(User, user_id)
    if user.role != "student":
        return "Only students can book mentors.", 403

    message = request.form.get("message")
    
    new_booking = Booking(
        student_id=user_id,
        mentor_id=mentor_id,
        message=message
    )
    db.session.add(new_booking)
    db.session.commit()

    return redirect(url_for("booking.my_bookings"))

@booking_bp.route("/my-bookings")
def my_bookings():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    user_id = session["user_id"]
    user = db.session.get(User, user_id)
    if user.role != "student":
        return "Only students have sent bookings.", 403

    bookings = Booking.query.filter_by(student_id=user_id).order_by(Booking.created_at.desc()).all()
    
    return render_template("booking/my_bookings.html", bookings=bookings)

@booking_bp.route("/booking/<int:id>/status", methods=["POST"])
def update_status(id):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    user_id = session["user_id"]
    user = db.session.get(User, user_id)
    if user.role != "mentor":
        return jsonify({"error": "Forbidden"}), 403

    booking = db.session.get(Booking, id)
    if not booking or booking.mentor_profile.user_id != user_id:
        return jsonify({"error": "Booking not found or not yours"}), 404
    
    data = request.get_json()
    status = data.get("status")
    
    if status in ["approved", "rejected"]:
        booking.status = status
        db.session.commit()
        return jsonify({"message": "Status updated successfully", "status": status}), 200
    
    return jsonify({"error": "Invalid status"}), 400
