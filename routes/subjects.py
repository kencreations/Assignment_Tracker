from flask import Blueprint, jsonify
from db import get_db_connection

subjects_bp = Blueprint("subjects", __name__)

@subjects_bp.route("/subjects", methods=["GET"])
def get_subjects():

    conn = get_db_connection(with_db=True)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, description FROM subjects")
    subjects = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"data": subjects}), 200
