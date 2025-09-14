from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/', methods=['GET'])
def home():
    return render_template('public/index.php')

if __name__ == '__main__':
    app.run(debug=True)
    