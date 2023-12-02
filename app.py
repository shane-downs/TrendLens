from flask import Flask, jsonify
from ordered_map import OrderedMap
from unordered_map import unordered_map
from fetch import *

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


class GraphData:
    def __init__(self):
        self.ordered_map = OrderedMap()
        self.unordered_map = unordered_map()

    def insert_all_ordered(self):
        pass

    def insert_all_unordered(self):
        pass


@app.route('/')
def hello_world():
    my_map = OrderedMap()
    my_map["George Kittle"] = "49ers"
    my_map["AJ Brown"] = "Eagles"
    my_map["Jarred Goff"] = "Lions"
    my_map["Anthony Richardson"] = "Colts"
    return my_map["AJ Brown"]