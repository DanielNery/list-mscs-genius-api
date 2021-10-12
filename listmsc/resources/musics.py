from flask_restful import Resource, reqparse, request
from flask_uuid import uuid
from datetime import datetime

import requests
import json
import os
import redis
import logging

_logger = logging.getLogger(__name__)

HEADER = {
	'User-Agent': 'CompuServe Classic/1.22',
	'Accept': 'application/json',
	'Host': os.getenv("HOST"),
	'Authorization': f'Bearer {os.getenv("ACESS_TOKEN")}'
}

redis_conn = redis.Redis()

class Musics(Resource):
	"""Recurso responsável por retornar 10 músicas mais populares do artista passado"""

	def _get_cache_args(self):
		"""Retorna True ou False se usará cache"""
		
		args = dict(request.args)
		if 'cache' in args:
			return eval(args.get('cache'))

		return True

	def _search_artist(self, artist_name):
		"""Retorna o conteúdo do cache referente ao artista"""
		
		try:
			cache_data = redis_conn.get(artist_name)
			return cache_data

		except Exception as e:
			_logger.error(f"An error occurred while search in cache.\n{e}")
			return False

	def _update_cache(self, artist_name, data):
		"""Atualiza cache com novos dados, retorna True ou False"""
		try:
			artist_name = artist_name.replace('-', ' ').replace('+', ' ').replace('_', ' ')
			return redis_conn.set(artist_name, data, 604800)
		
		except Exception as e:
			_logger.error(f"An error occurred while updating the cache.\n{e}")
			return False

	def get(self, artist_id, artist_name):
		"""
			Retorna lista de artistas
		"""

		cache = self._get_cache_args()
		cache_data = self._search_artist(artist_name) if cache else False
		if not cache_data:
			_logger.warning("No Cached.")
			querystring = {"q": artist_id}
			url = f"https://{os.getenv('HOST')}/artists/{artist_id}/songs?sort=popularity&per_page=10"
			response = requests.get(url=url, headers=HEADER, params=querystring)
			data = json.loads(response.text)
			
			if response.status_code == 200:
				
				for song in data['response']['songs']:
					if song['primary_artist']['name'] == artist_name:
						self._update_cache(artist_name, response.text)
						break

				#self._update_dynamodb(self, data)
				return data, 200
			return data, response.status_code

		_logger.warning("Returning Cached data.")
		data = json.loads(cache_data)
		return data, 200

				


	