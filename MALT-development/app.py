'''
MALT - Flask Web Application
-----------------------------------------------
Andrew Pyle, Zhenlin Jin, Hanzhao Chen
UA LITTLE ROCK DEPARTMENT OF COMPUTER SCIENCE
-----------------------------------------------
This python applicaiton routes HTTP requests, manipulates data (Pandas Library), creates charts
(Plotly Python API). The static CSS and JS files are under static/assets. This is requrired for
Flask to serve them in production. The web server should serve these files in production.

The data manipulation and charting functions are defined below. They expect a Pandas DataFrame with
The data to be visualized.

DataFrame columns expected (as of 23 Mar 2017):
 - df['Account Name']
 - df['City']
 - df['Hour']
 - df[['Country']
 - df['State']
 - df['City']
 - df['Date']
 - df['Time']
 - df['IP Address']

TODO:
 - Create python function to query a database for the data and feed it to the functions (save it in
 memory or query in each function?)
  - Create markers for the leaflet map. (Database query)
  - AJAX query for leafletMapCustom.js to fetch markers (lat/long)
'''

from flask import Flask
from flask import render_template
from flask import request
import plotly.offline
import plotly.graph_objs as go
# import plotly.figure_factory as FF  ## Switched to a HTML table generated by Pandas
import pandas as pd
import MySQLdb
# from db_connector import db_connection

app = Flask(__name__)
# mysql = MySQLdb(app) #flask_mysqldb initialization

## Import flat JSON file with data sample for development
data = "data.json"
df = pd.read_json(data)
df.index += 1

db = MySQLdb.connect(host='localhost', user='root', passwd='a1boxxit', db='malttest')
cur = db.cursor()

## Plotly Chart generation functions
def AccountDistribution():
#   Change IP Address column to account column - sample data had assounts redacted
    ipSeries = df["IP Address"].value_counts()
    ipFrame = pd.DataFrame({'ipAddress' : ipSeries.index, 'login count' : ipSeries.values})
    trace = [
        go.Bar(
            x = ipFrame["ipAddress"],
            y = ipFrame["login count"],
            #width = 0.9,
            marker = dict(
                color='#fe9aa2',
                line=dict(
                    color='#fe3445',
                    width=1.5,
                    ),
                #colorbar = dict(
                #    thickness = 1,
                #   ),
                ),
            opacity=0.8,
            ),
        ]
    layout = go.Layout(
        margin = dict(
            l=50,
            r=50,
            t=10,
            b=50,
            ),
        xaxis = dict(
            #title = "Account Name",
            showticklabels = True,
            tickmode = 'auto',
            nticks = 10,
            tickfont = dict(
                size=10,
                ),
            ),
        yaxis = dict(
            #title = "Frequency"
            ),
    )
    accounts = go.Figure(data=trace, layout=layout)
    return plotly.offline.plot(
        accounts,
        output_type='div',
        include_plotlyjs=False,
        show_link=False,
        )

def LocationDistribution():
    citySeries = df['City'].value_counts()
    cityFrame = pd.DataFrame({'city' : citySeries.index, 'count' : citySeries.values})
    trace = [
        go.Bar(
            x = cityFrame['city'],
            y = cityFrame['count'],
            marker = dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
                ),
            ),
        opacity=0.6,
        ),
    ]
    layout = go.Layout(
        margin = dict(
            l=50,
            r=50,
            t=10,
            b=50,
            ),
        xaxis = dict(
            showticklabels = True,
            tickmode = 'auto',
            tickfont = dict(
                size=10,
                ),
            ),
        )
    locations = go.Figure(data=trace, layout=layout)
    return plotly.offline.plot(
        locations,
        output_type='div',
        include_plotlyjs=False,
        show_link=False,
        )

def TimeOfDayDistribution():
    # Declare variables for layout below. I couldn't figure out how to create them inline.
    hours_list = list(range(0,25))
    hours_format_list = []
    for x in range(0,25):
        hours_format_list.append('{}:00'.format(x))


    timeSeries = df["Hour"].value_counts()
    timeFrame = pd.DataFrame({'Time':timeSeries.index, 'Count':timeSeries.values})
    trace = [
        go.Bar(
            x = timeFrame["Time"],
            y = timeFrame["Count"],
            #width = 0.9,
            marker = dict(
                color='	#f6d3a2',
                line=dict(
                    color='#eeb058',
                    width=1.5,
                ),
                #colorbar = dict(
                #    thickness = 1,
                #),
            ),
            opacity=1.0,
        ),
    ]
    layout = go.Layout(
        margin = dict(
            l=50,
            r=50,
            t=10,
            b=50,
            ),
        xaxis = dict(
            autotick = False,
            showticklabels = True,
            tickmode = 'array',
            tickvals = list(range(0,25)), ## Should be: [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24],
            ticktext = hours_format_list, ## Should be: ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '24:00'],
            tickfont = dict(
                size=10,
                ),
            ),
        yaxis = dict(
            #title = "Frequency"
            ),
    )
    times = go.Figure(data=trace, layout=layout)
    return plotly.offline.plot(
        times,
        output_type='div',
        include_plotlyjs=False,
        show_link=False,
        )

def IPAddressDistributionToday():
    ipSeries = df.loc[df.Date >= pd.to_datetime('today')]['IP Address'].value_counts()
    ipFrame = pd.DataFrame({'ipAddress' : ipSeries.index, 'login count' : ipSeries.values})
    trace = [
        go.Bar(
            x = ipFrame["ipAddress"],
            y = ipFrame["login count"],
            #width = 0.9,
            marker = dict(
                color='#8dd775',
                line=dict(
                    color='#418a28',
                    width=1.5,
                    ),
                #colorbar = dict(
                #    thickness = 1,
                #   ),
                ),
            opacity=0.6,
            ),
        ]
    layout = go.Layout(
        margin = dict(
            l=50,
            r=50,
            t=10,
            b=50,
            ),
        xaxis = dict(
            #title = "Account Name",
            # showticklabels = True,
            # tickmode = 'auto',
            # nticks = 10,
            tickfont = dict(
                size=10,
                ),
            ),
        yaxis = dict(
            #title = "Frequency"
            ),
    )
    accounts = go.Figure(data=trace, layout=layout)
    return plotly.offline.plot(
        accounts,
        output_type='div',
        include_plotlyjs=False,
        show_link=False,
        )

def DataTable():
    df = pd.DataFrame(db_connection()).to_html()
    return df
    ##return df[['Account Name','Country','State','City','Date','Time','IP Address',]].to_html()
    # dfTable = df[['Account Name','Country','State','City','Date','Time','IP Address',]]
    # table = FF.create_table(
    #     dfTable,
    #     colorscale = [[0, '#3D4A57'],
    #                   [.5, '#d9d9d9'],
    #                   [1, '#ffffff']],
    #     )
    # #table.layout.width = 1000 #width in px
    # return plotly.offline.plot(
    #     table,
    #     #filename='file.html',
    #     output_type='div',
    #     include_plotlyjs=False,
    #     show_link=False,
    #     )

## URL Routing
@app.route("/")
def index():
    return render_template(
        "index.html",
        account_distribution = AccountDistribution(),
        location_distribution = LocationDistribution(),
        time_of_day_distribtion = TimeOfDayDistribution(),
        ip_address_distribution_today = IPAddressDistributionToday(),
        # data_table = DataTable(),
        )


@app.route("/login", methods=["GET","POST"])
def login():
    if (request.method == 'GET'):
        return render_template('login.html')
    elif (request.method == 'POST'):
        username_submit = request.form['username']
        password_submit = request.form['password']
        return str(cur.execute("SELECT * FROM MaltUsers WHERE UserName='{}';".format(username_submit)))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
