from flask import Flask
from route import route

def main():

    app = Flask(__name__, template_folder='Fontend')
    route(app)
    app.run('0.0.0.0', 5000, debug=True) #Inicia la app en la dirección

main()