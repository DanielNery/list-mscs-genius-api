from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from resources.search import Search
from resources.musics import Musics

import redis
import dotenv
import os
dotenv.load_dotenv()

app = Flask(__name__)
api = Api(app)

CORS(app, origins=os.getenv("ALLOWED_HOSTS"), allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
    supports_credentials=True)

api.add_resource(Search, '/search/<string:artist_name>')
api.add_resource(Musics, '/artist/<string:artist_id>/<string:artist_name>')

@app.route('/')
def index():
    return "Bem-Vindo(a) a API!!"

if __name__ == '__main__':
    app.run()