import csv
from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
import statsmodels.api as sm
from ordered_map import OrderedMap
from unordered_map import unordered_map

# get data
df = pd.read_csv("temp_data.csv")

app = Dash(__name__)            # initialize app

# app layout
app.layout = html.Div([
    html.Div(children="The Next Facebook v6"),
    # dcc.Graph(figure=fig)
    dcc.Graph(
        id="line-plot",
        figure=px.scatter(df,
                          x="Year",
                          y="Usage",
                          trendline_color_override="blue",
                          title="keyword usage vs year"
                          ).add_trace(px.line(df, x="Year", y="Usage").data[0])
    )
])

# running the app
if __name__ == "__main__":
    app.run(debug=True)
