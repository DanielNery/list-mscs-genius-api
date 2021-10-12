from flask_restful import Resource

import requests
import json
import os
import redis


HEADER = {
    'User-Agent': 'CompuServe Classic/1.22',
    'Accept': 'application/json',
    'Host': os.getenv("HOST"),
    'Authorization': f'Bearer {os.getenv("ACESS_TOKEN")}'
}

class Search(Resource):
    """Recurso responsável por retornar lista de artistas, para o usuário escolher"""

    def get(self, artist_name):
        """
            Retorna lista de artistas
        """


        querystring = {"q": artist_name}
        url = f"https://{os.getenv('HOST')}/search"

        try:
            response = requests.get(url=url, headers=HEADER, params=querystring)
            if response.status_code != '200':
                return json.loads(response.text), response.status_code

        except Exception as e:
            print(e)
            return {"message": "Internal server error."}, 500

        data = json.loads(response.text)
        return data, 200