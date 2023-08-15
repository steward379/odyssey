from flask import request, redirect, url_for, jsonify, session, Blueprint
from app.models.comment import Comment
from app.models.member import Member
from app import db

# bp = Blueprint("comments", __name__, url_prefix="/api")
bp = Blueprint("comments", __name__)

@bp.route("/createMessage", methods=["POST"])
def create_message():
    content = request.form.get("content")
    user_id = session.get("user_id")

    if not content or content.strip() == "":
        return jsonify({"status": "error", "message": "Please enter content"}), 400
    elif content and user_id:
        comment = Comment(content=content, member_id=user_id, like_count = 0)
        db.session.add(comment)
        db.session.commit()
        rreturn jsonify({"status": "success", "message": "Message created successfully!"})
    # elif not user_id:
    #     return redirect(url_for("error", message="3: Please sign in first"))
    else:
        return jsonify({"status": "error", "message": "Unknown error"}), 500
 
@bp.route('/deleteMessage', methods=['POST'])
def delete_message():
    comment_id = request.form.get('comment_id')
    comment = Comment.query.get(comment_id)
    user_id = session.get('user_id')

    if comment and comment.member_id == user_id :
        db.session.delete(comment)
        db.session.commit()
        return jsonify({"status": "success", "message": "Message deleted successfully!"})
    elif not user_id:
        return jsonify({"status": "error", "message": "Please sign in first"}), 401
    elif not comment:
        return jsonify({"status": "error", "message": "Comment not found"}), 404
    
     return jsonify({"status": "error", "message": "Unknown error"}), 500