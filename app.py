from flask import Flask
from ordered_map import OrderedMap

app = Flask(__name__)

@app.route('/')
def hello_world():
    my_map = OrderedMap()
    my_map["George Kittle"] = "49ers"
    my_map["AJ Brown"] = "Eagles"
    my_map["Jarred Goff"] = "Lions"
    my_map["Anthony Richardson"] = "Colts"
    return my_map["AJ Brown"]