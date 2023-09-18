from flask import Flask, logging, render_template, jsonify, request
from dbconn import BB_db
import pandas as pd

app = Flask(__name__, static_url_path='/static', static_folder='static')

countries = []
players = []

## Link a la parte visual, de aqui llamaremos a las otras clases para realizar funcionalidades con los botones
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/equipos')
def equipos():
    bb_db_conn = BB_db('ilovebasket14')
    global countries
    countries = bb_db_conn.get_countries()
    bb_db_conn.close()
    return render_template('equipos.html', countries=countries)

@app.route('/operaciones')
def operaciones():
    return render_template('operaciones.html')

@app.route('/get_players/<country>')
def get_players(country):
    bb_db_conn = BB_db('ilovebasket14')
    global players
    players = bb_db_conn.query_country_export(country)
    bb_db_conn.close()
    return jsonify(players)



if __name__ == '__main__':
    app.run(host='127.0.0.1', port='80', debug=True)