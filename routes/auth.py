from flask import Blueprint, request, jsonify
from db import get_db_connection
auth_bp = Blueprint("auth", __name__)


@auth_bp.route('/auth', methods=["POST", "GET"])
def auth():
    if request.method == "GET":
        return jsonify({"message": "GET not allowed on this route"}), 400
    
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    conn = get_db_connection(with_db=True)
    cursor = conn.cursor(dictionary=True)  # return dict instead of tuple

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()  

    cursor.close()
    conn.close()

    if user is None:
        return jsonify({"error": "User not found"}), 404

    password_hash = bcrypt.check_password_hash(user["password_hash"], password)
    if password_hash is False:
        return jsonify({"error": "Invalid password"}), 401

    return jsonify({"message": "Login successful", "user": user}), 200
