# Dash
import dash
from dash_core_components.Tabs import Tabs
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
import base64

# Python scripts
import aux

import tasks 
import datetime

import pandas as pd

fruits = {
            "t1":['10:00','potato','pending'],"t2":['18:00','potato','pending'],
            "t3":['19:00','potato','pending'],"t4":['20:00','potato','pending']
            }

def b64_image(image_filename):
    with open(image_filename, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')


# App settings
app = dash.Dash(__name__,suppress_callback_exceptions=True,meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])
app.title = aux.APP_TITLE
app.layout =  html.Div([html.Br(),html.Div([html.H1(aux.APP_TITLE)],style={'text-align':'center'}),html.Br(),
        dcc.Tabs(id="tabs-styled-with-inline", value='today', children=[
        dcc.Tab(label='Què he de fer avui?', value='avui', style=aux.tab_style, selected_style=aux.tab_selected_style),
        dcc.Tab(label='Afegeix tasca', value='add_task', style=aux.tab_style, selected_style=aux.tab_selected_style),
        dcc.Tab(label='El meu perfil', value='profile', style=aux.tab_style, selected_style=aux.tab_selected_style),
    ], style=aux.tabs_styles),
   html.Div(id='tabs-content-inline')
])

app.enable_dev_tools(debug=True, dev_tools_props_check=False)

@app.callback(
    Output("tabs-styled-with-inline", "value"),
    [Input("submit-entry", "n_clicks")],
    [
        State("select-subject", "value"),
        State("select-activity", "value"),
        State("enter-task", "value"),
        State("enter-hours", "value"),
        State("date-picker", "date"),
        State("enter-time", "value"),
    ],
)
def register(submit_entry, select_subject, select_activity, enter_task, enter_hours,date_picker, enter_time):
    print(submit_entry)
    return tasks.register(submit_entry,select_subject, select_activity, enter_task, enter_hours,date_picker, enter_time)


@app.callback(dash.dependencies.Output('label1', 'children'),
    [dash.dependencies.Input('interval1', 'n_intervals')])
def update_interval(n):
    return str(datetime.datetime.now().strftime("%H:%M:%S"))

red_button_style = {'background-color': 'red',
                    'padding': '10px',
                    "width": "100%"}

normal_button_style ={
    'padding': '10px',
    "width": "100%"
}

ended_button_style ={
    'background-color': 'rgb(153,153,153)',
    'padding': '10px',
    "width": "100%"
}
def get_first_task():
    return list(fruits.keys())[0]

def state(hour):
    res = []
    for task in fruits:
        time = int(fruits[task][0][0:2])
        if hour == time:
            res.append(red_button_style)
        elif hour < time:
            res.append(normal_button_style)
        elif hour > time:
            res.append(ended_button_style)
    return res


a = [dash.dependencies.Output('TIME', 'figure')] + [dash.dependencies.Output(f"t{i+1}", 'style') for i in range(len(fruits))]
@app.callback(a,
    [dash.dependencies.Input('label1', 'children')])
def time_clock(time):
    min = int(time[-5:-3])
    hour = int(time[-8:-6])
    fet = min/60*100
    falta = 100 - fet
    data = [['% Completat', fet],['% Pendent', falta]]
    df = pd.DataFrame(data,columns = ['Etiqueta', 'Percentatge'])
    fig = px.pie(df, hover_name="Etiqueta", hover_data={'Etiqueta':False,'Percentatge':False}, values='Percentatge', names='Etiqueta', color_discrete_sequence=["#00CC96","rgb(246,246,246)"])
    fig.update(layout_showlegend=False)
    fig.update_traces(textinfo='none',sort=False)


    #first_task = get_first_task()
    #hour_first_task = int(first_task[0:2])
    return [fig] + state(hour)
    #if hour == hour_first_task:
    #    return fig,red_button_style
    #elif hour < hour_first_task:
    #    return fig,normal_button_style
    #elif hour > hour_first_task:
    #    return fig,ended_button_style


# MAIN
@app.callback(Output('tabs-content-inline', 'children'),
              Input('tabs-styled-with-inline', 'value'))
def render_content(tab):
    if tab == 'avui':
        lst=[]
        for key, values in fruits.items():
            hour, name = values[0], values[1]
            lst.append( html.Div([html.Button(hour + " - "+ name, id=key,style=normal_button_style),html.Br(),html.Br()]))
        return  html.Div([html.Div([
                html.Div([html.Div([html.H2("Tasques:"),html.Div(lst)], style={'marginLeft': "5%",'marginRight': "5%"})], style={'width':'40%','text-align':'left','backgroundColor': 'rgb(153,153,153)','marginTop': 22,'marginLeft': 10}),html.Div([], style={'height':'1200px'}),
                html.Div([
                    html.Div([dcc.Interval(id='interval1', interval=1000, n_intervals=0),html.Br(),html.H1(id='label1', children='',style={ 'textAlign': 'center', 'color': 'black'})]),
                    dcc.Graph(id='TIME'),html.Img(src=b64_image("img/estudi.png"), style={'height':'30%'})], style={'width':'60%','text-align':'center'})],style={'display':'flex'}
                ),html.Div()])
                
    elif tab == 'add_task':
        return tasks.tasks_tab()
    elif tab == 'profile':
        return 

if __name__ == '__main__':
    app.run_server(debug=True)