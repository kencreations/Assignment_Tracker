from flask import Blueprint, request, jsonify, make_response
from db import get_db_connection
from extensions import bcrypt
auth_bp = Blueprint("auth", __name__)


@auth_bp.route('/auth', methods=["POST", "GET"])
def auth():
    if request.method == "GET":
        return jsonify({"message": "GET not allowed on this route"}), 400
    
    Email = request.form.get('email')
    password = request.form.get('password')

    if not Email or not password:
        return jsonify({"message": "Email and password required"}), 400

    conn = get_db_connection(with_db=True)
    cursor = conn.cursor(dictionary=True)  # return dict instead of tuple

    cursor.execute("SELECT * FROM users WHERE email = %s", (Email,))
    user = cursor.fetchone()  

    cursor.close()
    conn.close()

    if user is None:
        return jsonify({"message": "User not found"}), 404

    password_hash = bcrypt.check_password_hash(user["password_hash"], password)
    if password_hash is False:
        return jsonify({"message": "Invalid password"}), 401
    
    response = jsonify({"success":  True,"message": "Login successful", "user": user["username"]})
    setCookie = make_response(response)
    setCookie.set_cookie('username', user["username"], httponly=True, samesite='Lax', secure=False, max_age=60*60*24)
    return response



def 