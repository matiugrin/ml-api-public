# from flask import flask, escape, request

# app = Flask(__name__)

# @app.route('/')
# def hello():
#     name = request.args.get("name", "World")
#     return f'Hello, {escape(name)}'


# env FLASK_APP=hello.py flask run
# de esa forma puedo atender de a una request, y no puedo tomar una segunda hasta que no termine el servidor.

# gunicorn -w 4 hello.py
# esto ya es un servidor de aplicaciones, para servir el codigo este con 4 threads que esperan escuchar peticiones.

