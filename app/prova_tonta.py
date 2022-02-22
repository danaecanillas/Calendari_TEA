import datetime
import plotly.graph_objs as go
import numpy as np
from dash import dcc
from dash import html
import dash

def holidays():
    year = datetime.datetime.now().year

    d1 = datetime.date(year, 8, 1)
    d2 = datetime.date(year+1, 7, 15)

    delta = d2 - d1

    HORES = []
    for i in range(24):
        HORES.append(str(i).rjust(2,"0")+":00-"+str((i+1)%24).rjust(2,"0")+":00")

    HORES = [str(i).rjust(2,"0")+":00-"+str((i+1)%24).rjust(2,"0")+":00" for i in range(24)]
    dates_in_year = [d1 + datetime.timedelta(i) for i in range(delta.days+1)] #gives me a list with datetimes for each day a year
    z = np.random.randint(2, size=(len(dates_in_year)))
    text = [str(i) for i in dates_in_year] #gives something like list of strings like ‘2018-01-25’ for each date. Used in data trace to make good hovertext.
    #4cc417 green #347c17 dark green
    
    
    colorscale=[[False, '#eeeeee'], [True, '#76cf63']]

    data = [
    go.Heatmap(
    z = z,
    xgap=3, # this
    ygap=3, # and this is used to make the grid-like apperance
    showscale=False,
    colorscale=colorscale
    )
    ]
    layout = go.Layout(
    title='activity chart',
    height=280,
    yaxis=dict(
    showline = False, showgrid = False, zeroline = False,
    tickmode='array',
    ticktext=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    tickvals=[0,1,2,3,4,5,6],
    ),
    xaxis=dict(
    showline = False, showgrid = False, zeroline = False,
    ),
    font={'size':10, 'color':'#9e9e9e'},
    plot_bgcolor=('#fff'),
    margin = dict(t=40),
    )

    fig = go.Figure(data=data, layout=layout)
    return fig

app = dash.Dash()
app.layout = html.Div([
dcc.Graph(id='heatmap-test', figure=holidays(), config={'displayModeBar': False})
])