from flask import Flask
from flask import render_template

import plotly.offline
import plotly.graph_objs as go
import pandas as pd

app = Flask(__name__)

# Data Path
data = "data.json"
df = pd.read_json(data)
df.index += 1


# Function Declarations
def AccountHistogram():
    ipSeries = df["IP Address"].value_counts()
    ipFrame = pd.DataFrame({'ipAddress':ipSeries.index, 'login count':ipSeries.values})
    trace = [
        go.Bar(
            x=ipFrame["ipAddress"],
            y=ipFrame["login count"],
            width = 1,
            marker = dict(
                color='rgb(158,202,225)',
                line=dict(
                    color='rgb(8,48,107)',
                    width=1.5,
                ),
                #colorbar = dict(
                #    thickness = 1,
                #),
            ),
            opacity=0.6,
        ),
    ]
    layout = go.Layout(
        margin = dict(
            l=10,
            r=0,
            t=0,
            #b=100,
        ),
    )

    accounts = go.Figure(data=trace, layout=layout)

    return plotly.offline.plot(
        accounts,
        output_type='div',
        include_plotlyjs=False,
        show_link=False,
        )

def LocationHistogram():
    #df = pd.read_json(data_filename)
    trace = [
        go.Histogram(x=df["City"])
    ]
    layout = go.Layout(
        margin = dict(
            l=10,
            r=0,
            t=0,
        ),
    )
    locations = go.Figure(data=trace, layout=layout)

    return plotly.offline.plot(
        locations,
        output_type='div',
        include_plotlyjs=False,
        show_link=False,
        )

## URL Routing
@app.route("/")
def index():
    return render_template(
        "index.html",
        account_histogram=AccountHistogram(),
        location_histogram=LocationHistogram(),
        data_table=df.to_html(),
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
