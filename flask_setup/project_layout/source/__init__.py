import logging

from flask import Flask, render_template
from flask_cors import CORS
from flask_restplus import Resource, Api

app = Flask(__name__)
CORS(app)
api = Api(app)

# a simple page that says hello
@api.route('/hello')
class Hello(Resource):
    def get(self):
        return "Hello, World!"


@api.route('/Home')
class Home(Resource):
    def get(self):
        return render_template('index.html')


if __name__ == "__main__":
    logging.warning("Warning: you should use api.sh to run the server.")
    app.run(host="127.0.0.1", port=8000, debug=True)
