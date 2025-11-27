import os
from flask import Flask, session
from route import route

def main():

    app = Flask(__name__, template_folder='../../Frontend/html', static_folder='../../Frontend/static')

    app.config['SECRET_KEY'] = 'some random string' 
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 
    
    route(app)
    app.run('0.0.0.0', 5000, debug=True) #Inicia la app en la dirección
    
main()