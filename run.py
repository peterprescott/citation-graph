import os                               # import files safely for any os
import json                             # for parsing javascript object notation
from pybtex.database import parse_file  # for parsing .bib files
from flask import Flask, jsonify        # for serving web app
from flask_cors import CORS             # stop CORS errors

def prettify_json(file):
    """
    Reads in a minified JSON file and writes a more readable, prettified version.
    
    Args:
        file (string): Location of the JSON file.
    """
    
    with open(f"prettified_{file}", 'w') as prettified_JSON:
        with open(file, 'r') as minified_JSON:
            prettified_JSON.write(json.dumps(json.load(minified_JSON), sort_keys=False, indent=4))
            
########################################################################
############ 
########################################################################

def get_citations(key):

    bib_data = parse_file(os.path.join('bib_files',f'{key}_citations.bib'))
    return bib_data

def get_references(key):

    bib_data = parse_file(os.path.join('bib_files',f'{key}_references.bib'))
    return bib_data


def generate_graph_json(key):

    node_list = []
    edge_list = []
    
    ref_data = get_references(key)
    
    for entry in ref_data.entries:
        node_list.append(
                        dict(id = entry, 
                                 title = str(ref_data.entries[entry].fields['title']).strip('{}'), 
                                 #author = str(ref_data.entries[entry].fields['author']).strip('{}'), 
                                 #year = str(ref_data.entries[entry].fields['year']).strip('{}'), 
                                 type = ref_data.entries[entry].type,
                                 group = 1
                                )
                        )
        
        if entry != key:
            edge_list.append(dict(source = key, target = entry, value = 1))

    
    cite_data = get_citations(key)
    
    for entry in cite_data.entries:
        if entry != key:
            node_list.append(
                            dict(id = entry, 
                                 title = str(cite_data.entries[entry].fields['title']).strip('{}'), 
                                 #author = str(cite_data.entries[entry].fields['author']).strip('{}'), 
                                 #year = str(cite_data.entries[entry].fields['year']).strip('{}'), 
                                 type = cite_data.entries[entry].type,
                                 group = 2
                                )
                            )
            if entry != key:
                edge_list.append(dict(source = key, target = entry, value = 1))
    
    return {"nodes": node_list, "links": edge_list}


# ~ class CitationNode():
    
    
    # ~ def __init__(self, cite_key, title, lit_type):
        # ~ self = dict()
        # ~ self["id"]      = cite_key
        # ~ self["title"]   = title
        # ~ self["author"]  = author
        # ~ self["year"]    = year
        # ~ self["type"]    = lit_type
    


# ~ class CitationEdge(dict):
    
    # ~ def __init__(self, source, target):
        
        # ~ self = dict()
        # ~ self["source"] = source
        # ~ self["target"] = target

########################################################################
############ 
########################################################################


app = Flask(__name__)
CORS(app)

example_json = {"nodes":
                    [{"name":"Predictive Postcode", "group":1}], 
                "links":
                    []
                }

@app.route('/api/<key>')
def api(key):
    """API to return citation graph"""

    return jsonify(generate_graph_json(key))


########################################################################
############ 
########################################################################

if __name__ == "__main__":
    
    generate_graph_json('RWebberBurrows2018')

    

    
    app.run()
