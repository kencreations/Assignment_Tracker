from flask import Blueprint, request, jsonify, make_response
from db import get_db_connection
from extensions import bcrypt
assignment_bp = Blueprint("assignment", __name__)

def add_assignment():
    title = request.form.get('title')
    subject = request.form.get('subject')
    due_date = request.form.get('due_date')
    description = request.form.get('description')
    status = request.form.get('status')
    username = request.cookies.get('username')

    if not all([title, subject, due_date, description, status, username]):
        return jsonify({"message": "All fields are required"}), 400
    conn = get_db_connection(with_db=True)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if user is None:
        cursor.close()
        conn.close()
        return jsonify({"message": "User not found"}), 404
    user_id = user[0]
    cursor.execute("""
        INSERT INTO assignments (user_id, title, subject_id, due_date, description, status)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (user_id, title, subject, due_date, description, status))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Assignment added successfully"}), 201   

def get_assignments():
    username = request.cookies.get('username')
    if not username:
        return jsonify({"message": "Unauthorized"}), 401
    conn = get_db_connection(with_db=True)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if user is None:
        cursor.close()
        conn.close()
        return jsonify({"message": "User not found"}), 404
    user_id = user["id"]
    cursor.execute("""
        SELECT a.id, a.title, s.name AS subject, a.due_date, a.description, a.status
        FROM assignments a
        JOIN subjects s ON a.subject_id = s.id
        WHERE a.user_id = %s
    """, (user_id,))
    assignments = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"data": assignments}), 200

@assignment_bp.route('/assignment', methods=["POST", "GET"])
def assignment():
    if request.method == "GET":
        return get_assignments()   # <-- must return
    elif request.method == "POST":
        return add_assignment()