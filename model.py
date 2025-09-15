from flask import Flask, request, render_template, make_response
from routes.auth import auth_bp
from routes.assignment import assignment_bp
from routes.subjects import subjects_bp
import os
from extensions import bcrypt
from db import get_db_connection
def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), 'templates')  # ✅ point to app/templates
    )
    bcrypt.init_app(app)
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    app.register_blueprint(auth_bp)
    app.register_blueprint(assignment_bp, url_prefix='/api')
    app.register_blueprint(subjects_bp, url_prefix='/api')

    @app.route('/', methods=['GET'])
    def home():
        return render_template('public/index.html')

    @app.route("/dashboard", methods=['GET'])
    def dashboard():
        user_id = request.cookies.get('user_id')
        if not user_id:
            return make_response(render_template('public/index.html'))

        conn = get_db_connection(with_db=True)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT username, email FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user:
            return make_response(render_template('public/index.html'))

        return render_template('public/dashboard.html', user=user)

    
    return app