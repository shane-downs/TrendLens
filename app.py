import csv
import random

from dash import Dash, html, dcc, callback, Output, Input, State, no_update, exceptions
import pandas as pd
import plotly.express as px
import statsmodels.api as sm
from create_maps import *
from fetch import getArticlesFromMapsAndInsertToCSV


app = Dash(__name__)

# app layout
app.layout = html.Div([
    html.Meta(charSet="UTF-8"),
    html.Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
    html.Link(rel="stylesheet", href="style.css"),
    html.Link(rel="stylesheet", href="https://fonts.googleapis.com/css2?family=Lato&display=swap"),
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
                                         placeholder='Enter Keyword',
                                         persistence=False, 
                                         autoComplete="off", 
                                         list = 'list-suggested-inputs',
                                     ),
                                     html.Datalist(id='list-suggested-inputs', children=[html.Option(value='')]),

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


def update_graph(start_year, end_year, _keyword):
    # the title of the graph (not the entire website)
    titleString = "\'" + _keyword + "\'" + " Usage Between " + str(start_year) + " and " + str(end_year)
    # read the first line from the csv (which has the time taken to retrieve data for both the maps)
    first_line = pd.read_csv("formatted_nyt_data.csv", nrows=1, header=None)

    # gets retrieval time from file and adds it to time taken to insert for the result "total runtime"
    elapsed_times = first_line.values.flatten()
    subtitle = "Total Unordered Map Runtime: {} vs Total Ordered Map Runtime: {}".format(
        (elapsed_times[0] + unorderedRuntime), (elapsed_times[1] + orderedRuntime))

    df = pd.read_csv("formatted_nyt_data.csv", skiprows=1)
    # scanning csv
    filtered_df = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]
    fig = px.scatter(filtered_df, x="Year", y="Usage", trendline_color_override="blue", title=titleString)
    fig.add_trace(px.line(filtered_df, x="Year", y="Usage").data[0])

    # subtitle
    fig.update_layout(
        annotations=[
            dict(
                xref="paper",
                yref="paper",
                x=0.5,
                y=1.15,
                text=subtitle,
                showarrow=False,
                font=dict(
                    family='Arial, sans-serif',
                    size=14,
                    color='black'
                ),
            )
        ]
    )
    return fig


@app.callback(      
    Output('list-suggested-inputs', 'children'),
    Input('keyword-input', 'value'),
    # prevent_initial_call=True
)
def suggest_keywords(value):
    if not value or len(value) < 3:
        return no_update
    filtered_suggestions = [suggestion for suggestion in suggestions if value.lower() in suggestion.lower()]

    return [html.Option(value=suggestion) for suggestion in filtered_suggestions]




@app.callback(      
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
                # get the data from the maps and write it to the csv
                getArticlesFromMapsAndInsertToCSV(keyword, start_year, end_year, nyt_unordered_map, nyt_ordered_map)
                return update_graph(start_year, end_year, keyword)       # update graph
            else:       # if it is length 0, the keyword doesn't exist
                return no_update
    else:
        return no_update


@app.callback(      # call back for randomize button
    [
        Output("line-plot", "figure", allow_duplicate=True),
        Output('start-year-input', 'value'),
        Output('end-year-input', 'value'),
        Output('keyword-input', 'value')
    ],
    [Input('randomize-val', 'n_clicks')],
    [
        State('start-year-input', 'value'),
        State('end-year-input', 'value'),
        State('keyword-input', 'value')
    ],
    prevent_initial_call=True
)
def handleRandomize(randomize_val_clicks, start_year, end_year, keyword):       # when randomize button is clicked
    if randomize_val_clicks > 0:
        randomInput = randomizeInput()          # get a random input
        # get the information for this input out of the map and put it in the csv, so it can be read my update_graph
        getArticlesFromMapsAndInsertToCSV(randomInput[0], randomInput[1], randomInput[2], nyt_unordered_map, nyt_ordered_map)
        return update_graph(randomInput[1], randomInput[2], randomInput[0]), "","",""  # update graph
    else:
        return no_update


def randomizeInput():
    result = []     # result to return later
    subList = []
    # loop to get random keyword
    while True:
        currSubList = nyt_unordered_map.GetRandomKeyword()      # get the random sub list
        if (len(currSubList) >= 10):        # the list has over 10 years of data points
            result.append(currSubList[0].keyword)       # add the keyword to result
            subList = currSubList
            break
        else:
            continue
    # get max and min year from data
    minYr = 2023
    maxYr = 1862
    for data in subList:
        if (int(data.year) < minYr):       # if current year is less than current minimum year
            minYr = int(data.year)
        elif (int(data.year) > maxYr):     # if current year is greater than maximum year
            maxYr = int(data.year)
    # now we have the max and minimum year, add to list and return
    result.append(minYr)
    result.append(maxYr)
    return result       # and return result


if __name__ == "__main__":
    # articles_list = read_csv_to_list()
    # nyt_ordered_map = create_ordered_map(articles_list)
    # nyt_unordered_map = create_unordered_map(articles_list)

    # get articles from csv file
    articles_list = read_csv_to_list()
<<<<<<< Updated upstream
    # get information for ordered map
    orderedResult = create_ordered_map(articles_list)
    nyt_ordered_map = orderedResult[0]      # returns a tuple, so item 0 is the map
    orderedRuntime = orderedResult[1]       # item 1 is the time taken to insert the items
    # get information for unordered map
    unorderedResult = create_unordered_map(articles_list)
    nyt_unordered_map = unorderedResult[0]      # item 0 is the map
    unorderedRuntime = unorderedResult[1]       # item 1 is the runtime to do all the insertion

    # now run the app
    app.run(debug=True)
=======
    nyt_ordered_map = create_ordered_map(articles_list)
    nyt_unordered_map = create_unordered_map(articles_list)
    suggestions = create_map_of_keywords()
    app.run(debug=True)
    
>>>>>>> Stashed changes
