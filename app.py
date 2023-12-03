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
                         html.H3("Created by Shane Downs, Leonardo Cobaleda, and Wilson Goins"),
                     ]),

            html.Div(
                className="graph",
                children=[
                    html.Div([
                        html.Div(className="graph-input",
                                 children=[
                                     dcc.Input(
                                         className="input-field",
                                         id='start-year-input',
                                         type='number',
                                         placeholder='Start Year (1853-2023)', min=1853, max=2023),
                                     dcc.Input(
                                         className="input-field",
                                         id='end-year-input',
                                         type='number',
                                         placeholder='End Year (1853-2023)', min=1853, max=2023),

                                     dcc.Input(
                                         className="input-field",
                                         id='keyword-input',
                                         type='text',
                                         placeholder='Enter Keyword'),

                                     html.Button(
                                         className="submit-button",
                                         id='submit-val',
                                         children="Submit",
                                         n_clicks=0),

                                 ]),

                        html.Button(
                            className="random-button",
                            id='randomize-val',
                            children="Generate Random Input",
                            n_clicks=0),

                        dcc.Graph(id="line-plot"),
                    ]),
                ]),

            html.Div(className="side-nav",
                     children=[
                         html.Img(src="assets/logo.png", className="logo"),
                     ])
        ]
    )
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
def handleChange(submit_val_clicks, randomize_val_clicks, start_year, end_year, keyword):
    if submit_val_clicks > 0:  # if they clicked submit
        if (start_year is None) or (end_year is None) or (start_year > end_year) or (
                keyword is None):  # if something is wrong
            return no_update
        else:  # if all is good
            if (len(nyt_unordered_map[keyword]) > 0):  # if the keyword exists
                getArticlesFromMapsAndInsertToCSV(keyword, start_year, end_year, nyt_unordered_map, nyt_ordered_map)
                return update_graph(start_year, end_year)  # update graph
            else:  # if it is length 0, the keyword doesn't exist
                return no_update
    elif randomize_val_clicks > 0:  # if they click the randomize button
        randomInput = randomizeInput()
        getArticlesFromMapsAndInsertToCSV(randomInput[0], randomInput[1], randomInput[2], nyt_unordered_map,
                                          nyt_ordered_map)
        return update_graph(randomInput[1], randomInput[2])  # update graph
    else:
        return no_update


def randomizeInput():
    result = [nyt_unordered_map.GetRandomKeyword()]  # add random keyword as first thing in list
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
