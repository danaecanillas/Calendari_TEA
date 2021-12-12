import dash_html_components as html
import dash_core_components as dcc
import aux_ as aux
import dash
from dash.dependencies import Input, Output

from datetime import date

def deadlines_tab(calendar):
    res = []
    deadlines = calendar.get_next_deadlines()
    for lliurament in deadlines:
        res.append(html.P("-" + lliurament, style={'marginLeft': "2%"}))

    print(res)

    return dcc.Tab(html.Div([html.Br(),
                    html.H2(
                        "Propers lliuraments i examens:",style={'marginLeft': "2%"}
                    )] + res + [html.Br()],style={'marginLeft': "15%",'marginRight': "15%",'marginTop': "5%",'background-color':'rgb(240,240,240)'},
                        className="input__container",
                    ))

