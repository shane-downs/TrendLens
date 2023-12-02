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
# variables
# df = px.data.stocks(index=True, dateTimes=True)
# fig = px.scatter(df, trendline="rolling", trendline_options=dict(window=5), title="Results for keyword")
# fig.data = [t for t in fig.data if t.mode == "lines"]
# fig.update_traces(showlegend=True)
# fig.show()

app.layout = html.Div([
    html.Div(html.H1("TrendLens"), style={
        'textAlign': 'center',
        'color': 'blue'
    }),
    html.Div(children="The Next Facebook v4"),
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
