#! /usr/bin/python
# -*- coding: utf-8 -*-
from optparse import OptionParser
from flask import Flask, jsonify, request
import ratebeer


def main(host, port):
    rb = ratebeer.RateBeer()
    app = Flask(__name__)
    setupFlask(app, rb)
    app.run(host=host, port=port)


def setupFlask(app, rb):
    @app.route('/search/<criteria>', methods=['GET'])
    def search(criteria):
        beers = []
        breweries = []
        rbresult = rb.search(criteria)
        for beer in rbresult['beers']:
            beers.append({beer.name: beer.__dict__})
        for brewery in rbresult['breweries']:
            breweries.append({brewery.name: brewery.__dict__})

        return jsonify({'beers': beers, 'breweries': breweries})

    @app.route('/beer', methods=['POST'])
    def beer():
        post_data = request.get_json()
        url = post_data.get('url', None)
        if not url:
            return
        result = rb.beer(url)
        return jsonify(result)

    @app.route('/brewery', methods=['POST'])
    def brewery():
        post_data = request.get_json()
        url = post_data.get('url', None)
        if not url:
            return
        result = rb.brewery(url)
        return jsonify(result)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-p", "--port", dest="port", default=5100, help="Server port")
    parser.add_option("-s", "--host", dest="host", default="127.0.0.1", help="Server host (127.0.0.1/0.0.0.0)")

    (options, args) = parser.parse_args()

    main(options.host, int(options.port))
