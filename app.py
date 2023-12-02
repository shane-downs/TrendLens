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

app.layout = html.Div([
    html.Div(children="The Next Facebook v6"),
    dcc.Input(id='start-year-input', type='number', placeholder='Start Year (1853-2023)', min=1853, max=2023),
    dcc.Input(id='end-year-input', type='number', placeholder='End Year (1853-2023)', min=1853, max=2023),
    dcc.Input(id='keyword-input', type='text', placeholder='Enter Keyword',
              style={'width': '200px'}),
    html.Button('Submit', id='submit-val', n_clicks=0),
    # html div for the randomize button below keyword input
    html.Div([
        html.Button('Randomize Keyword', id='randomize-keyword', n_clicks=0,
                    style={'width': '208px', 'marginLeft': '339px'})
    ]),
    dcc.Graph(id="line-plot"),
    html.Div(id='output-div')
])
# app layout


def update_graph(start_year, end_year, keyword):
    # scanning csv
    filtered_df = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]
    
    # if keyword:
    #     filtered_df = filtered_df[filtered_df['Keyword'] == keyword]

    fig = px.scatter(filtered_df, x="Year", y="Usage", trendline_color_override="blue", title="keyword usage vs year")
    fig.add_trace(px.line(filtered_df, x="Year", y="Usage").data[0])

    return fig


@app.callback(
    Output('line-plot', 'figure'),
    Output('output-div', 'children'),
    [Input('submit-val', 'n_clicks')],
    [Input('randomize-val', 'n_clicks')],
    [Input('start-year-input', 'value'),
     Input('end-year-input', 'value'),
     Input('keyword-input', 'value')]
)
def handleSubmit(clicked, start_year, end_year, keyword):
    if clicked == 0:
        return Dash.no_update
    else:
        clicked = 0
        if (start_year is None) or (end_year is None) or (start_year > end_year) or (keyword is None):
            return Dash.no_update
        
        return update_graph(start_year, end_year, keyword)


if __name__ == "__main__":
    app.run(debug=True)
