from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        return redirect('/portal')
    else:
        return render_template('index.html')


@app.route('/portal')
def portal():
    return 'Login Successful!'

@app.route('/register')
def register():
    return 'Register Here!'



if __name__ == "__main__":
    app.run(debug=True)
