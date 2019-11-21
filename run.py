import os                               # import files safely for any os
import json                             # for parsing javascript object notation
from flask import Flask, jsonify        # for serving web app
from flask_cors import CORS             # stop CORS errors

import reader
import literature

app = Flask(__name__)
CORS(app)

@app.route('/test')
def test():
    """Confirms Flask App is running."""

    return "<title>Running!</title>"


@app.route('/api/<key>')
def api(key):
    """API to return citation graph"""
    get = reader.Bib(key)
    return jsonify(get.json_graph())

if __name__ == "__main__":
    
    app.run()
