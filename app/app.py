# Dash
from re import S
import dash
from dash import html
from dash import dcc, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import plotly.graph_objs as go
import numpy as np
import random

# Python scripts
import aux_ as aux
import tasks 
import profile
import datetime
import deadlines
from calendar_class import Calendar

#########################################################################################
# Calendar settings
#########################################################################################
calendar = Calendar("Simon")
calendar.auto_schedule = True

ASSIGNATURES = []
#########################################################################################

#########################################################################################
# Global vars
#########################################################################################
now = datetime.datetime.now()
str_date = datetime.datetime.strftime(now, '%Y/%m/%d')
now += datetime.timedelta(hours=2)
# a = [dash.dependencies.Output('TIME', 'figure')] + [dash.dependencies.Output(f"t{i+1}", 'style') for i in range(len(fruits))]
if str_date not in calendar.schedule.keys():
    day_tasks = {}
else:
    day_tasks = calendar.schedule[str_date]

DISPONIBILITAT = pd.DataFrame(aux.DISPONIBILITAT, index=['Diumenge',"Dissabte","Divendres","Dijous","Dimecres","Dimarts","Dilluns"])
#########################################################################################

#########################################################################################
# App settings
#########################################################################################
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.enable_dev_tools(debug=True, dev_tools_props_check=False)
app.title = aux.APP_TITLE

# Main front, set of initial tabs
app.layout = html.Div([
    html.Br(),
    html.Div([html.H1(aux.APP_TITLE)], style={"text-align": "center"}),
    html.Br(),
    dcc.Tabs(
        id="tabs-styled-with-inline",
        value="today",
        children=[
            dcc.Tab(
                label="Què he de fer avui?",
                value="avui",
                style=aux.tab_style,
                selected_style=aux.tab_selected_style,
            ),
            dcc.Tab(
                label="Afegeix tasca",
                value="add_task",
                style=aux.tab_style,
                selected_style=aux.tab_selected_style,
            ),
            dcc.Tab(
                label="Lliuraments i exàmens",
                value="deadlines",
                style=aux.tab_style,
                selected_style=aux.tab_selected_style,
            ),
            dcc.Tab(
                label="El meu perfil",
                value="profile",
                style=aux.tab_style,
                selected_style=aux.tab_selected_style,
            ),
        ],
        style=aux.tabs_styles,
    ),
    html.Div(id="tabs-content-inline"),
])
#########################################################################################

#########################################################################################
# App callbacks
#########################################################################################

# ---------------------------------------------------------------------------------------
# Add task tab
# ---------------------------------------------------------------------------------------
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
        calendar.add_deadline(
            select_subject,
            select_activity,
            enter_task,
            date,
            enter_time,
            dedication=enter_hours,
        )
        #print(calendar.get_schedule())
        print(calendar.weekly_schedule)
        return "today"
    raise dash.exceptions.PreventUpdate

# ---------------------------------------------------------------------------------------
# Today tab
# ---------------------------------------------------------------------------------------

@app.callback([dash.dependencies.Output('label1', 'children'),dash.dependencies.Output("TASQUES", "children"),],
    [dash.dependencies.Input('interval1', 'n_intervals')])
def update_interval(n):
    now = datetime.datetime.now()
    now += datetime.timedelta(hours=2)
    f_now = str(now.strftime("%H:%M:%S"))
    global day_tasks
    day_tasks = calendar.schedule[str_date]
    hours = sorted(day_tasks.keys())

    lst = []
    for hour in hours:
        check_task = hour[0:2]
        check_hour = f_now[0:2]
        if check_task == check_hour:
            style_B = aux.blue_button_style
        else:
            style_B = aux.normal_button_style 
        task = day_tasks[hour]
    # for hour, task in day_tasks.items():
        lst.append(
            html.Div([
                html.Button(hour + " | "+ task.name + " - "+ task.subject, id=str(task.date_time), style=style_B),
                html.Br(),
                html.Br()
            ])
        )

    return str(now.strftime("%H:%M:%S")), html.Div(lst)

@app.callback(
    [
        dash.dependencies.Output("TIME", "figure"),
        dash.dependencies.Output("ACTIVITY", "children"),
    ],
    [dash.dependencies.Input("label1", "children")],
)
def time_clock(time):
    min = int(time[-5:-3])
    hour = time[-8:-6]
    # There are things to do
    if hour+":00" in day_tasks.keys():
        fet = min / 60 * 100
        falta = 100 - fet
        data = [["% Completat", fet], ["% Pendent", falta]]
        df = pd.DataFrame(data, columns=["Etiqueta", "Percentatge"])
        fig = px.pie(
            df,
            hover_name="Etiqueta",
            hover_data={"Etiqueta": False, "Percentatge": False},
            values="Percentatge",
            names="Etiqueta",
            color_discrete_sequence=["#00CC96", "rgb(246,246,246)"],
        )
        fig.update(layout_showlegend=False)
        fig.update_traces(textinfo="none", sort=False)

        banner = [
            html.Div([
                html.Div([aux.ret_img(day_tasks[hour+":00"].activity_type)], style={'width':'40%'}),
                html.Div([
                    html.H2(day_tasks[hour+":00"].activity_type),
                    html.Div("De " + hour+":00" + " a " + str(int(hour)+1) +":00 cal fer:", style={'fontSize':20}), 
                    html.Br(),
                    html.Div("- Activitat: " + day_tasks[hour+":00"].name, style={'fontSize':20}), 
                    html.Div("- Assignatura: " + day_tasks[hour+":00"].subject, style={'fontSize':20}),
                    html.Br()
                ], style={'width':'60%','text-align':'center'})
            ], style={'display':'flex'})
        ]
        return fig, banner
    else:
        data = [["% Completat", 0], ["% Pendent", 100]]
        df = pd.DataFrame(data, columns=["Etiqueta", "Percentatge"])
        fig = px.pie(
            df,
            hover_data={"Etiqueta": False, "Percentatge": False},
            values="Percentatge",
            names="Etiqueta",
            color_discrete_sequence=["#00CC96", "rgb(256,256,256)"],
        )
        fig.update(layout_showlegend=False)
        fig.update_traces(textinfo="none", sort=False)
        banner = html.Div(
            "No tens cap activitat programada durant aquesta hora", style={"fontSize": 20}
        )
        return fig, banner

# ---------------------------------------------------------------------------------------
# Profile tab
# ---------------------------------------------------------------------------------------
def profile_tab():
    return html.Div([
       dcc.Tabs(id="tab-perfil", value='tab-perfil', children=[
           dcc.Tab(label='Afegeix esdeveniment', value='tab-esdeveniment'),
           dcc.Tab(label='Assignatures', value='tab-assignatures'),
           dcc.Tab(label='Disponibilitat Horària', value='tab-disponibilitat'),
        ]), 
        html.Div(id='tab-content-profile')
    ])

for hora in aux.HORES: 
    @app.callback(Output('%s' % hora, 'style'), [Input('%s' % hora, 'n_clicks')])
    def change_button_style(n_clicks):
        if n_clicks%2 != 0:
            print(n_clicks)
            return aux.green_button_style
        else:
            return aux.normal_button_style

        
@app.callback(
    Output('tab-perfil', "value"),
    [Input("save_disponibilitat", "n_clicks")],
    [
        State("dia_setmana", 'value'), 
        State('00:00-01:00', 'n_clicks'), State('01:00-02:00', 'n_clicks'), State('02:00-03:00', 'n_clicks'),
        State('03:00-04:00', 'n_clicks'), State('04:00-05:00', 'n_clicks'), State('05:00-06:00', 'n_clicks'),
        State('06:00-07:00', 'n_clicks'), State('07:00-08:00', 'n_clicks'), State('08:00-09:00', 'n_clicks'),
        State('09:00-10:00', 'n_clicks'), State('10:00-11:00', 'n_clicks'), State('11:00-12:00', 'n_clicks'),
        State('12:00-13:00', 'n_clicks'), State('13:00-14:00', 'n_clicks'), State('14:00-15:00', 'n_clicks'),
        State('15:00-16:00', 'n_clicks'), State('16:00-17:00', 'n_clicks'), State('17:00-18:00', 'n_clicks'),
        State('18:00-19:00', 'n_clicks'), State('19:00-20:00', 'n_clicks'), State('20:00-21:00', 'n_clicks'),
        State('21:00-22:00', 'n_clicks'), State('22:00-23:00', 'n_clicks'), State('23:00-00:00', 'n_clicks'),
    ],
)
def register(submit_entry, day, state0, state1, state2, state3, state4, state5, state6, state7, state8, state9,
            state10, state11, state12, state13, state14, state15, state16, state17, state18, state19, state20,
            state21, state22, state23):
    if submit_entry:
        DISPONIBILITAT.loc[day] = [state0%2, state1%2, state2%2, state3%2, state4%2, state5%2, state6%2, state7%2, state8%2, state9%2,
            state10%2, state11%2, state12%2, state13%2, state14%2, state15%2, state16%2, state17%2, state18%2, state19%2, state20%2,
            state21%2, state22%2, state23%2]

        disp = np.fliplr(np.transpose(DISPONIBILITAT))

        calendar.weekly_schedule = disp

        return 'tab-disponibilitat'
    else:
        return 'tab-disponibilitat'


@app.callback(Output('tab-content-profile', 'children'),
              Input('tab-perfil', 'value'))
def render_content(tab):
    if tab == 'tab-esdeveniment':
        return html.Div([
            html.H3('Tab content 1'),
        ])
    elif tab == 'tab-assignatures':

        return prova()

    elif tab == 'tab-disponibilitat':
        lst=[]
        i = 0
        lst.append(html.Div([html.H2("Disponibilitat horària")]))
        # for dia, hores in profile.horari.items():
        #     lst.append(html.H3(aux.DIES[i]))
        #     for hora in hores:   
        #         lst.append(html.Div([html.Button(hora, id=dia+hora,
        #             n_clicks=0,style=aux.normal_button_style)], style = {'display': 'inline-block'}))
        #     lst.append(html.Br())
        #     i+=1
        lst.append(html.Div([dcc.Graph(id='dispo_horaria', figure=holidays(), config={'displayModeBar': False}),html.Br(), html.Div(
                        [
                            html.Button(
                                "Actualitza la Disponibilitat",
                                id="save_disponibilitat",
                                n_clicks=0,
                                style=aux.normal_button_style,
                            )
                        ],
                        style={"width": "20%", "text-align": "rigth"},
                    ),html.Br(),dcc.Dropdown(
            options=[
                {'label': 'Dilluns', 'value': 'Dilluns'},
                {'label': 'Dimarts', 'value': 'Dimarts'},
                {'label': 'Dimecres', 'value': 'Dimecres'},
                {'label': 'Dijous', 'value': 'Dijous'},
                {'label': 'Divendres', 'value': 'Divendres'},
                {'label': 'Dissabte', 'value': 'Dissabte'},
                {'label': 'Diumenge', 'value': 'Diumenge'}
            ],clearable=False,id="dia_setmana",placeholder="Selecciona un dia"
        ),html.Br()], id="tab_com"))
        for hora in aux.HORES:   
            lst.append(html.Div([html.Button(hora, id=hora,
                n_clicks=0,style=aux.normal_button_style)], style = {'display': 'inline-block'}))
        lst.append(html.Br())
        i+=1
        return html.Div(lst,style={'marginLeft': "14%",'marginRight': "14%"})

def holidays():
    HORES = [str(i).rjust(2,"0")+":00-"+str((i+1)%24).rjust(2,"0")+":00" for i in range(24)]

    colorscale=[[False, "#eeeeee"], [True, "#76cf63"]]

    data = [
    go.Heatmap(
    z = DISPONIBILITAT,
    xgap=3, # this
    ygap=3, # and this is used to make the grid-like apperance
    showscale=False,
    colorscale=colorscale
    )
    ]
    layout = go.Layout(
    height=280,
    yaxis=dict(
    showline = False, showgrid = False, zeroline = False,
    tickmode='array',
    ticktext=['Diumenge',"Dissabte","Divendres","Dijous","Dimecres","Dimarts","Dilluns"],
    tickvals=[0,1,2,3,4,5,6],
    ),
    xaxis=dict(
    showline = False, showgrid = False, zeroline = False,
    tickmode='array',
    ticktext=HORES,
    tickvals=list(range(0, len(HORES)))
    ),
    font={'size':10, 'color':'#9e9e9e'},
    plot_bgcolor=('#fff'),
    margin = dict(t=40),
    )

    fig = go.Figure(data=data, layout=layout)
    return fig


@app.callback(
    Output('adding-rows-table', 'data'),
    Input('editing-rows-button', 'n_clicks'),Input('tab-perfil', 'value'),
    State('adding-rows-table', 'data'),State('assiggg', 'value'),)
def add_row(n_clicks, _, df, asig):
    if n_clicks > 0:
        print("CLICK")
        print(df)
        df.append({'tasques': asig})
        calendar.subject_list.append(asig)
        global ASSIGNATURES
        ASSIGNATURES = calendar.subject_list
        print(calendar.subject_list)
    return df

@app.callback(Output('tab-assignatures', "value"),
              [Input('adding-rows-table', 'data_previous')],
              [State('adding-rows-table', 'data')])
def show_removed_rows(previous, current):
    if previous is None:
        dash.exceptions.PreventUpdate()
    else:
        l = []
        for el in current:
            l.append(el['tasques'])
        
        calendar.subject_list = l
        global ASSIGNATURES
        ASSIGNATURES = calendar.subject_list

        dir_folder = os.path.dirname(__file__)
        df = pd.DataFrame({
            'tasques': calendar.subject_list,
        })
        return prova()

def prova():
    dir_folder = os.path.dirname(__file__)

    df = pd.DataFrame({
        'tasques': calendar.subject_list,
    })
    return html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.H2("Llista d'assignatures:"),
                            dash_table.DataTable(
                                id='adding-rows-table',
                                data=df.to_dict(orient='records'),
                                editable=True,
                                row_deletable=True,
                                style_as_list_view=True,
                                style_header = {'display': 'none'},
                                style_data= {'font-size': '13px', 'font-family':'Helvetica','padding': '10px'}
                                #fixed_rows={'headers': True},
                                #style_table={'height': 500}  # defaults to 500
                        ), html.Br(),html.Br(),html.Br(),
                            html.Div(id="TASQUES", children=''),dcc.Input(
            id="assiggg",
            type="text",
            placeholder="Escriu el nom de l'assignatura",
            style={'width':'82%','height': '20px','marginRight': 10, 'font-size': '13px','padding': '10px'}
        ),html.Button("Afegeix", id='editing-rows-button', n_clicks=0, style={'width':'12%','height': '40px','font-size': '13px','padding': '10px'}),
                        ], style={'marginLeft': "5%",'marginRight': "5%"})
                    ], style={'height': '500px','width':'40%','text-align':'left','backgroundColor': 'rgb(136,204,238)','marginTop': 22,'marginLeft': 10}),
                html.Div([html.Div([
 
                html.Img(src=aux.b64_image(f"{dir_folder}/img/assignatures.png"))
            ], style={'height':'70%','text-align':'center'})],style={'marginLeft': "5%",'marginRight': "5%"})], style={'display':'flex','text-align':'center','marginLeft': "5%",'marginRight': "5%"})
            ])



        
# ---------------------------------------------------------------------------------------
# Deadlines tab
# ---------------------------------------------------------------------------------------

#########################################################################################
# MAIN
#########################################################################################
@app.callback(Output('tabs-content-inline', 'children'),
              Input('tabs-styled-with-inline', 'value'))
def render_content(tab):
    if tab == 'avui':
        lst=[]

        if str_date not in calendar.schedule.keys():
            dir_folder = os.path.dirname(__file__)
            return html.Div([
                html.Div([html.H1("No tens res a fer avui!")], style={'text-align':'center'}), 
                html.Img(src=aux.b64_image(f"{dir_folder}/img/felicitats!.png"))
            ], style={'height':'70%','text-align':'center'})

        ACTIVITAT = []
        TASQUES = []

        time = str(now.strftime("%H:%M:%S"))[0:2]
        hour = time+":00"

        today_tasks = [
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.H2("Les tasques d'avui:"),
                            html.Div(id="TASQUES", children=''),
                        ], style={'marginLeft': "5%",'marginRight': "5%"})
                    ], style={'width':'40%','text-align':'left','backgroundColor': 'rgb(153,153,153)','marginTop': 22,'marginLeft': 10}),
                    html.Div([
                        html.Div([
                            dcc.Interval(id='interval1', interval=1000, n_intervals=0),
                            html.Br(),
                            html.H1(id='label1', children='', style={ 'textAlign': 'center', 'color': 'black'})
                        ]),
                        dcc.Graph(id='TIME'),
                        html.P(id='ACTIVITY', children='', style={ 'textAlign': 'center', 'color': 'black','background-color':'rgb(136,204,238)','marginLeft': "10%",'marginRight': "10%"})
                    ], style={'width':'60%','text-align':'center'})
                ], style={'display':'flex'})
            ])
        ] + ACTIVITAT
        return today_tasks
                
    elif tab == 'add_task':
        ASSIGNATURES = calendar.subject_list
        return tasks.tasks_tab(ASSIGNATURES)
    elif tab == 'profile':
        return profile_tab()
    elif tab == 'deadlines':
        return deadlines.deadlines_tab(calendar)

if __name__ == '__main__':
    app.run_server(debug=True)