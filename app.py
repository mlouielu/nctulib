# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
import requests_cache


from nctulib import library

app = Flask(__name__)
api = Api(app)
CORS(app)
requests_cache.install_cache()

app.config['JSON_AS_ASCII'] = False


class BookSearch(Resource):
    lib = library.NCTULibrary()

    def get(self, q):
        return jsonify([e.json() for e in self.lib.search(q)])


class BookLocation(Resource):
    lib = library.NCTULibrary()

    def get(self, bid):
        with requests_cache.disabled():
            return jsonify(self.lib.get_locations_by_bid(bid))


api.add_resource(BookSearch, '/books/<string:q>')
api.add_resource(BookLocation, '/location/<string:bid>')

if __name__ == '__main__':
    app.run(debug=True)
