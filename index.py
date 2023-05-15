from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/equipos')
def equipos():
    return render_template('equipos.html')

@app.route('/')
def operaciones():
    return render_template('operaciones.html')