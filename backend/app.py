from flask import Flask, request, jsonify
from flask_cors import CORS
import config
from postgresql_api import *


app = Flask(__name__)


if __name__ == "__main__":
    app.run(debug=True)

