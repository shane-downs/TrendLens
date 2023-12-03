import csv
import random

from dash import Dash, html, dcc, callback, Output, Input, State, no_update
import pandas as pd
import plotly.express as px
import statsmodels.api as sm
from create_maps import *
from fetch import getArticlesFromMapsAndInsertToCSV


app = Dash(__name__)

# app layout
app.layout = html.Div([
    html.Link(rel="stylesheet", href="style.css"),
    html.Div(
        className="homepage",
        children=[
            html.Div(className="text-box",
                     children=[
                         html.H1("Your Personal Tool for Analyzing Trends in the News"),
                     ]),

            html.Div(
                className="Graph",
                children=[
                    dcc.Input(id='start-year-input', type='number', placeholder='Start Year (1853-2023)', min=1853,
                              max=2023),
                    dcc.Input(id='end-year-input', type='number', placeholder='End Year (1853-2023)', min=1853,
                              max=2023),
                    dcc.Input(id='keyword-input', type='text', placeholder='Enter Keyword', style={'width': '200px'}),
                    html.Button('Submit', id='submit-val', n_clicks=0),
                    html.Div([
                        html.Button('Randomize Keyword', id='randomize-val', n_clicks=0,
                                    style={'width': '208px', 'marginLeft': '339px'})
                    ]),
                    dcc.Graph(id="line-plot"),
                ]),

            html.Div(className="side-nav",
                     children=[
                         html.Img(src="assets/logo.png", className="logo")
                     ])
        ]
    ),
    # html div for the randomize button below keyword input
])


def update_graph(start_year, end_year, _keyword):
    titleString = _keyword + " Usage Between " + str(start_year) + " and " + str(end_year)
    df = pd.read_csv("formatted_nyt_data.csv")

    # scanning csv
    filtered_df = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]

    fig = px.scatter(filtered_df, x="Year", y="Usage", trendline_color_override="blue", title=titleString)
    fig.add_trace(px.line(filtered_df, x="Year", y="Usage").data[0])

    return fig


@app.callback(      # call back for submit button
    Output("line-plot", "figure", allow_duplicate=True),
    [Input('submit-val', 'n_clicks')],
    [
        State('start-year-input', 'value'),
        State('end-year-input', 'value'),
        State('keyword-input', 'value')
    ],
    prevent_initial_call=True
)
def handleSubmit(submit_val_clicks, start_year, end_year, keyword):
    if submit_val_clicks > 0:       # if they clicked submit
        if (start_year is None) or (end_year is None) or (start_year > end_year) or (keyword is None):      # if something bad
            return no_update
        else:   # if all is good
            if (len(nyt_unordered_map[keyword]) > 0):       # if the keyword exists
                print("collecting data!")
                getArticlesFromMapsAndInsertToCSV(keyword, start_year, end_year, nyt_unordered_map, nyt_ordered_map)
                return update_graph(start_year, end_year, keyword)       # update graph
            else:       # if it is length 0, the keyword doesn't exist
                print("empty  :(")
                return no_update
    else:
        return no_update


@app.callback(      # call back for randomize button
    Output("line-plot", "figure", allow_duplicate=True),
    [Input('randomize-val', 'n_clicks')],
    [
        State('start-year-input', 'value'),
        State('end-year-input', 'value'),
        State('keyword-input', 'value')
    ],
    prevent_initial_call=True
)
def handleRandomize(randomize_val_clicks, start_year, end_year, keyword):
    if randomize_val_clicks > 0:
        randomInput = randomizeInput()
        getArticlesFromMapsAndInsertToCSV(randomInput[0], randomInput[1], randomInput[2], nyt_unordered_map, nyt_ordered_map)
        return update_graph(randomInput[1], randomInput[2], randomInput[0])  # update graph
    else:
        return no_update


def randomizeInput():
    result = [nyt_unordered_map.GetRandomKeyword()]     # add random keyword as first thing in list
    while True:
        startYear = random.randint(1862, 2022)
        endYear = random.randint(1862, 2022)
        if (startYear < (endYear - 10)):
            result.append(startYear)
            result.append(endYear)
            return result
        else:
            continue


if __name__ == "__main__":
    articles_list = read_csv_to_list()
    nyt_ordered_map = create_ordered_map(articles_list)
    nyt_unordered_map = create_unordered_map(articles_list)
    app.run(debug=True)


