from flask import Flask, request, render_template
from routes.auth import auth_bp
import os
from extensions import bcrypt

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), 'templates')  # ✅ point to app/templates
    )
    bcrypt.init_app(app)
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    app.register_blueprint(auth_bp)

    @app.route('/', methods=['GET'])
    def home():
        return render_template('public/index.html')

    @app.route("/dashboard", methods=['GET'])
    def dashboard():
        return render_template('public/dashboard.php')
    return app