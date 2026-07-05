from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from model import db, ForumThread, ForumReply, User

forum_bp = Blueprint("forum", __name__)

@forum_bp.route("/forum")
def list():
    threads = ForumThread.query.order_by(ForumThread.created_at.desc()).all()
    return render_template("forum/list.html", threads=threads)

@forum_bp.route("/forum/new", methods=["GET", "POST"])
def new():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    
    if request.method == "POST":
        title = request.form.get("title")
        body = request.form.get("body")
        user_id = session["user_id"]
        
        new_thread = ForumThread(
            title=title,
            body=body,
            user_id=user_id
        )
        db.session.add(new_thread)
        db.session.commit()
        return redirect(url_for("forum.thread", id=new_thread.id))
        
    return render_template("forum/new.html")

@forum_bp.route("/forum/<int:id>")
def thread(id):
    thread_obj = ForumThread.query.get_or_404(id)
    return render_template("forum/thread.html", thread=thread_obj)

@forum_bp.route("/forum/<int:id>/reply", methods=["POST"])
def reply(id):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    user_id = session["user_id"]
    user = db.session.get(User, user_id)
    
    data = request.get_json()
    body = data.get("body")
    
    if not body:
        return jsonify({"error": "Body cannot be empty"}), 400
        
    new_reply = ForumReply(
        body=body,
        user_id=user_id,
        thread_id=id
    )
    db.session.add(new_reply)
    db.session.commit()
    
    return jsonify({
        "id": new_reply.id,
        "body": new_reply.body,
        "author": user.name,
        "created_at": new_reply.created_at.isoformat()
    }), 201
