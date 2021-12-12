import dash_html_components as html
import dash_core_components as dcc
import aux_ as aux
import dash
from dash.dependencies import Input, Output

import datetime 

def deadlines_tab(calendar):
    res = []
    deadlines = calendar.get_next_deadlines()
    for lliurament in deadlines:
        str_clock = datetime.datetime.strftime(lliurament.date_time, '%H:%M')
        res.append(html.P("- " + lliurament.name + " ("+ str(lliurament.date_time.date()) + " " + str_clock +")", style={'marginLeft': "2%"}))

    print(res)

    return dcc.Tab(html.Div([html.Br(),
                    html.H2(
                        "Propers lliuraments i examens:",style={'marginLeft': "2%"}
                    )] + res + [html.Br()],style={'marginLeft': "15%",'marginRight': "15%",'marginTop': "5%",'background-color':'rgb(240,240,240)'},
                        className="input__container",
                    ))

