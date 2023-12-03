import csv
from dash import Dash, html, dcc, callback, Output, Input, State, no_update
import pandas as pd
import plotly.express as px
import statsmodels.api as sm
from create_maps import *
from fetch import getArticlesFromMapsAndInsertToCSV


app = Dash(__name__)

# app layout
app.layout = html.Div([
    html.Div(children="The Next Facebook v8"),
    dcc.Input(id='start-year-input', type='number', placeholder='Start Year (1853-2023)', min=1853, max=2023),
    dcc.Input(id='end-year-input', type='number', placeholder='End Year (1853-2023)', min=1853, max=2023),
    dcc.Input(id='keyword-input', type='text', placeholder='Enter Keyword', style={'width': '200px'}),
    html.Button('Submit', id='submit-val', n_clicks=0),
    # html div for the randomize button below keyword input
    html.Div([
        html.Button('Randomize Keyword', id='randomize-val', n_clicks=0,
                    style={'width': '208px', 'marginLeft': '339px'})
    ]),
    dcc.Graph(id="line-plot"),
    html.Div(id='output-div')
])


def update_graph(start_year, end_year):
    df = pd.read_csv("formatted_nyt_data.csv")

    # scanning csv
    filtered_df = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]

    fig = px.scatter(filtered_df, x="Year", y="Usage", trendline_color_override="blue", title="keyword usage vs year")
    fig.add_trace(px.line(filtered_df, x="Year", y="Usage").data[0])

    return fig


@app.callback(
    Output("line-plot", "figure"),
    [
        Input('submit-val', 'n_clicks'),
        Input('randomize-val', 'n_clicks')
    ],
    [
        State('start-year-input', 'value'),
        State('end-year-input', 'value'),
        State('keyword-input', 'value')
    ]
)
def handleSubmit(submit_val_clicks, randomize_val_clicks, start_year, end_year, keyword):
    if submit_val_clicks > 0:       # if they clicked submit
        if (start_year is None) or (end_year is None) or (start_year > end_year) or (keyword is None):
            return no_update
        else:
            getArticlesFromMapsAndInsertToCSV(keyword, start_year,end_year, nyt_unordered_map, nyt_ordered_map)
            return update_graph(start_year, end_year)
    elif randomize_val_clicks > 0:
        print("rando")
    else:
        return no_update


if __name__ == "__main__":
    articles_list = read_csv_to_list()
    nyt_ordered_map = create_ordered_map(articles_list)
    nyt_unordered_map = create_unordered_map(articles_list)
    app.run(debug=True)


