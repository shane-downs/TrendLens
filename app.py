# from flask import Flask, jsonify
from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
from ordered_map import OrderedMap
from unordered_map import unordered_map

# get data
df = pd.read_csv("alt_data_DONTUSE.csv")


app = Dash(__name__)            # initialize app
# app layout
# variables
# df = px.data.stocks(index=True, dateTimes=True)
# fig = px.scatter(df, trendline="rolling", trendline_options=dict(window=5), title="Results for keyword")
# fig.data = [t for t in fig.data if t.mode == "lines"]
# fig.update_traces(showlegend=True)
# fig.show()

app.layout = html.Div([
    html.Div(children="Version 1"),
    # dcc.Graph(figure=fig)
    dcc.Graph(figure=px.histogram(df, x="year", y="year"))
])

# running the app
if __name__ == "__main__":
    app.run(debug=True)


# app = Flask(__name__)     OLD
# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False     OLD
    # @app.route('/')
    # def hello_world():
    #     my_map = OrderedMap()
    #     my_map["George Kittle"] = "49ers"
    #     my_map["AJ Brown"] = "Eagles"
    #     my_map["Jarred Goff"] = "Lions"
    #     my_map["Anthony Richardson"] = "Colts"
    #     return my_map["AJ Brown"]

# class GraphData:
#     def __init__(self):
#         self.ordered_map = OrderedMap()
#         self.unordered_map = unordered_map()
#
#     def insert_all_ordered(self):
#         pass
#
#     def insert_all_unordered(self):
#         pass













