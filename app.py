import csv
from dash import Dash, html, dcc, callback, Output, Input, State
import pandas as pd
import plotly.express as px
import statsmodels.api as sm
from ordered_map import OrderedMap
from unordered_map import unordered_map

# get data
df = pd.read_csv("temp_data.csv")

app = Dash(__name__)

# app layout
app.layout = html.Div([
    html.Div(children="Homepage"),
    dcc.Input(id='start-year-input', type='number', placeholder='Start Year (1853-2023)', min=1853, max=2023),
    dcc.Input(id='end-year-input', type='number', placeholder='End Year (1853-2023)', min=1853, max=2023),
    dcc.Input(id='keyword-input', type='text', placeholder='Enter Keyword'),
    html.Button('Submit', id='submit-val', n_clicks=0),
    dcc.Graph(id="line-plot")
])


def update_graph(start_year, end_year, keyword):
    # scanning csv
    filtered_df = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]

    # if keyword:
    #     filtered_df = filtered_df[filtered_df['Keyword'] == keyword]

    fig = px.scatter(filtered_df, x="Year", y="Usage", trendline_color_override="blue", title="keyword usage vs year")
    fig.add_trace(px.line(filtered_df, x="Year", y="Usage").data[0])

    return fig


@app.callback(
    Output("line-plot", "figure"),
    [Input('submit-val', 'n_clicks')],
    [State('start-year-input', 'value'),
     State('end-year-input', 'value'),
     State('keyword-input', 'value')]

)
def updateOutput(clicked, start_year, end_year, keyword):
    if clicked == 0:
        return Dash.no_update
    else:
        clicked = 0
        if start_year is None or end_year is None or start_year > end_year:
            return Dash.no_update

        return update_graph(start_year, end_year, keyword)


if __name__ == "__main__":
    app.run(debug=True)
