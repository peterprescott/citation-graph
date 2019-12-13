"""
This is the main file intended to be run. 
It first opens static_gui/index.html in your default webbrowser, 
and then serves the Flask API which is called from that static interface.
When called it responds with the required graph data 
by returning a JSON object with the necessary nodes and edges.
"""

import os                               # import files safely for any os
import sys
import json                             # for parsing javascript object notation
from flask import Flask, jsonify        # for serving web app
from flask_cors import CORS             # stop CORS errors
import webbrowser                       # to load static gui without hassle

import db_commands as db
import literature as lit

webbrowser.open(".\static_gui\index.html")

app = Flask(__name__)
CORS(app)


@app.route('/test')
def test():
    """Confirms Flask App is running for tests.py"""

    return "<title>Running!</title>"


@app.route('/api/<key>/<radius>')
def api(key, radius):
    """API to return citation graph"""
    
    print(f"API called for {key}")
    
    db_file = os.path.join(sys.path[0], 'citation_graph.db')
    q = db.Query(db_file)
    graph_data = q.json_graph(key, int(radius))

    return jsonify(graph_data)

if __name__ == "__main__":

    app.run()
