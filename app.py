from flask import Flask, jsonify, request, render_template
from routes.auth import auth
from model import create_app
from flask_bcrypt import Bcrypt

app = create_app()
if __name__ == '__main__':
    app.run(debug=True)
