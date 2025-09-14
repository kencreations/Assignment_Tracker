from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from db import get_db_connection

auth_bp = Blueprint("auth", __name__)
@auth_bp.route('/auth', methods=["POST", "GET"])
def auth():
    if request.method == "GET":
        return jsonify({"message": "GET not allowed on this route"}), 400
    
    username = request.form.get('username')
    password = request.form.get('password')

    conn = get_db_connection(with_db=True)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    conn.commit()
    user = cursor.fetchall

    cursor.close()
    conn.close()
    