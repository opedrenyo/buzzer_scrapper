from flask import Flask, render_template
from dbconn import BB_db
import pandas as pd

app = Flask(__name__)

## Link a la parte visual, de aqui llamaremos a las otras clases para realizar funcionalidades con los botones
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/equipos')
def equipos():
    #select aqui de countries
    bb_db_conn = BB_db('ilovebasket14')
    countries = bb_db_conn.get_countries()
    print(countries)
    return render_template('equipos.html', countries=countries)

@app.route('/operaciones')
def operaciones():
    return render_template('operaciones.html')

def get_players(id_country):
    print('entramos en get players')
    return ''



if __name__ == '__main__':
    app.run(host='127.0.0.1', port='80', debug=True)