import dash
from dash_core_components.Tabs import Tabs
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
import datetime
import pandas as pd
import base64

# Python scripts
import aux_ as aux
import tasks 
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import ../db.py
from calendar_class import Calendar

calendar = Calendar()
calendar.auto_schedule = True

now = datetime.datetime.now()
str_date = datetime.datetime.strftime(now, '%Y/%m/%d')


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

###############################################
# TASKS
###############################################
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
    if submit_entry:
        date = date_picker.replace("-", "/")
        calendar.add_deadline(select_subject, select_activity, enter_task, date, enter_time, dedication=enter_hours)
        #print(submit_entry, select_subject, select_activity, enter_task, enter_hours, date_picker, enter_time)
        print(calendar.get_schedule())
        return "today"
    raise dash.exceptions.PreventUpdate
    

###############################################
# TODAY 
###############################################
@app.callback(dash.dependencies.Output('label1', 'children'),
    [dash.dependencies.Input('interval1', 'n_intervals')])
def update_interval(n):
    now = datetime.datetime.now()
    now += datetime.timedelta(hours= 12)
    return now

def state(str_date, hour):
    res = []
    for time,task in calendar.schedule[str_date].items():
        time = int(time[0:2])
        if hour == time:
            res.append(aux.red_button_style)
        elif hour < time:
            res.append(aux.normal_button_style)
        elif hour > time:
            res.append(aux.ended_button_style)
    return res


LLISTA = []

a = [dash.dependencies.Output('TIME', 'figure')] + LLISTA
@app.callback(a,
    [dash.dependencies.Input('label1', 'children')])
def time_clock(now):
    time = now[11:19]
    global str_date
    str_date = now[0:10].replace("-", "/")
    min = int(time[-5:-3])
    hour = int(time[-8:-6])
    fet = min/60*100
    falta = 100 - fet
    data = [['% Completat', fet],['% Pendent', falta]]
    df = pd.DataFrame(data,columns = ['Etiqueta', 'Percentatge'])
    fig = px.pie(df, hover_name="Etiqueta", hover_data={'Etiqueta':False,'Percentatge':False}, values='Percentatge', names='Etiqueta', color_discrete_sequence=["#00CC96","rgb(246,246,246)"])
    fig.update(layout_showlegend=False)
    fig.update_traces(textinfo='none',sort=False)

    global a
    if str_date in calendar.schedule.keys():
        
        LLISTA = [dash.dependencies.Output(f"t{task.date_time}", 'style') for _, task in calendar.schedule[str_date].items()]
        a = [dash.dependencies.Output('TIME', 'figure')] + LLISTA
        print(len(a))
        print(len(LLISTA))
        print(type(LLISTA))
        print(len([fig] + state(str_date, hour)))
    else:
        a = [dash.dependencies.Output('TIME', 'figure')] + []

    return [fig] + state(str_date, hour)


# MAIN
@app.callback(Output('tabs-content-inline', 'children'),
              Input('tabs-styled-with-inline', 'value'))
def render_content(tab):
    if tab == 'avui':
        now = datetime.datetime.now()
        now += datetime.timedelta(hours= 12) #BORRAR
        str_date = datetime.datetime.strftime(now, '%Y/%m/%d')
        lst=[]
        
        if str_date not in calendar.schedule.keys():
            return html.Div([html.Div([html.H1("No tens res a fer avui!")],style={'text-align':'center'}), html.Img(src=aux.b64_image("img/felicitats!.png"))], style={'height':'70%','text-align':'center'})

        for hour, task in calendar.schedule[str_date].items():
            lst.append( html.Div([html.Button(hour + " - "+ task.name, id=str(task.date_time),style=aux.normal_button_style),html.Br(),html.Br()]))
        return  html.Div([html.Div([
                html.Div([html.Div([html.H2("Tasques:"),html.Div(lst)], style={'marginLeft': "5%",'marginRight': "5%"})], style={'width':'40%','text-align':'left','backgroundColor': 'rgb(153,153,153)','marginTop': 22,'marginBottom': 60,'marginLeft': 10}),
                html.Div([
                    html.Div([dcc.Interval(id='interval1', interval=1000, n_intervals=0),html.Br(),html.H1(id='label1', children='',style={ 'textAlign': 'center', 'color': 'black'})]),
                    dcc.Graph(id='TIME')], style={'width':'60%','text-align':'center'})],style={'display':'flex'}
                ),html.Div([html.Div("hl")], style={'width':'50%','text-align':'right'})])
                
    elif tab == 'add_task':
        return tasks.tasks_tab()
    elif tab == 'profile':
        return 

if __name__ == '__main__':
    app.run_server(debug=True)