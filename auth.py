from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from model import db, User, MentorProfile

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role", "student")

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "User with this email already exists."

        new_user = User(
            name=name,
            email=email,
            password=generate_password_hash(password),
            role=role
        )
        db.session.add(new_user)
        db.session.commit()

        if role == "mentor":
            profile = MentorProfile(
                user_id=new_user.id,
                domain="",
                company="",
                experience_years=0,
                bio="",
                availability="Limited",
                linkedin=""
            )
            db.session.add(profile)
            db.session.commit()

        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            return redirect(url_for("mentor.list"))
        
        return "Invalid email or password."

    return render_template("auth/login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
