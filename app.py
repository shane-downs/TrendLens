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
    html.Div(children="The Next Facebook v4"),
    # dcc.Graph(figure=fig)
    dcc.Graph(
        id="line-plot",
        figure=px.scatter(df,
                          x="Year",
                          y="Usage",
                          trendline_color_override="blue",
                          title="keyword usage vs year"
                          ).update_traces(line_shape="linear")
        # figure=px.histogram(df, x="Year", y="Usage")
    )
])

# running the app
if __name__ == "__main__":
    # info = [["Year", "Usage"], [2000, 40], [2001, 55], [2002, 30], [2003, 29], [2004, 80], [2005, 90]]
    # csv_file_path = "temp_data.csv"
    #
    # # Write data to CSV file
    # with open(csv_file_path, 'w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerows(info)

    app.run(debug=True)

