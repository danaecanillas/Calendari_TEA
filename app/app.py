# Dash
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
#########################################################################################

#########################################################################################
# Global vars
#########################################################################################
now = datetime.datetime.now()
str_date = datetime.datetime.strftime(now, '%Y/%m/%d')

# a = [dash.dependencies.Output('TIME', 'figure')] + [dash.dependencies.Output(f"t{i+1}", 'style') for i in range(len(fruits))]
if str_date not in calendar.schedule.keys():
    day_tasks = {}
else:
    day_tasks = calendar.schedule[str_date]
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
        print(calendar.get_schedule())
        return "today"
    raise dash.exceptions.PreventUpdate

# ---------------------------------------------------------------------------------------
# Today tab
# ---------------------------------------------------------------------------------------
@app.callback(dash.dependencies.Output('label1', 'children'),
    [dash.dependencies.Input('interval1', 'n_intervals')])
def update_interval(n):
    now = datetime.datetime.now()
    return str(now.strftime("%H:%M:%S"))

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
for dia, hores in profile.horari.items():
    for hora in hores: 
        @app.callback(Output('%s' % dia+hora, 'style'), [Input('%s' % dia+hora, 'n_clicks')])
        def change_button_style(n_clicks):
            if n_clicks%2 != 0:
                return aux.red_button_style
            else:
                return aux.normal_button_style

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
        
        global day_tasks
        day_tasks = calendar.schedule[str_date]
        hours = sorted(day_tasks.keys())

        for hour in hours:
            task = day_tasks[hour]
        # for hour, task in day_tasks.items():
            lst.append(
                html.Div([
                    html.Button(hour + " | "+ task.name + " - "+ task.subject, id=str(task.date_time), style=aux.normal_button_style),
                    html.Br(),
                    html.Br()
                ])
            )

        ACTIVITAT = []

        time = str(now.strftime("%H:%M:%S"))[0:2]
        hour = time+":00"

        today_tasks = [
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.H2("Les tasques d'avui:"),
                            html.Div(lst)
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
        return tasks.tasks_tab()
    elif tab == 'profile':
        return profile.profile_tab()
    elif tab == 'deadlines':
        return deadlines.deadlines_tab(calendar)

if __name__ == '__main__':
    app.run_server(debug=True)