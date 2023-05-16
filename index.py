from flask import Flask, render_template

app = Flask(__name__)

## Link a la parte visual, de aqui llamaremos a las otras clases para realizar funcionalidades con los botones

#consultamos los players que hay
players = []

#consultamos los paises que hay
countries = []

#consultamos las temporadas que hay
seasons = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/equipos')
def equipos():
    #select aqui de countries
    return render_template('equipos.html', countries=countries, players=players)

@app.route('/operaciones')
def operaciones():
    return render_template('operaciones.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='80', debug=True)