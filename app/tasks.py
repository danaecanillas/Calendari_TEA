from dash import html
from dash import dcc
import aux_ as aux
import dash
from dash.dependencies import Input, Output

from datetime import date

def tasks_tab(ASSIGNATURES):
    return dcc.Tab(html.Div([
                html.Div([
                    html.P(
                        "Assignatura:",
                        className="input__heading",
                        style={'font-size': '18px'}
                    ),
                    dcc.Dropdown(
                        id="select-subject",
                        options=[
                            {"label": i, "value": i}
                            for i in ASSIGNATURES
                        ],
                        placeholder="Escull una assignatura",
                        className="subject__select",
                        style={'font-size': '18px'}
                    ),],
                        className="dropdown__container",
                    ),
                html.Div([
                    html.P(
                        "Tipus de tasca:",
                        className="input__heading",
                        style={'font-size': '18px'}
                    ),
                    dcc.Dropdown(
                        id="select-activity",
                        options=[
                            {"label": i, "value": i}
                            for i in [
                                "Examen",
                                "Projecte"
                            ]
                        ],
                        placeholder="Escull el tipus de tasca",
                        className="activity__select",
                        style={'font-size': '18px'}
                    ),],
                        className="dropdown__container",
                    ),
                html.Div([
                    html.P(
                        "Nom de la tasca:",
                        className="input__heading",
                        style={'font-size': '18px'}
                    ),
                    dcc.Input(
                        id="enter-task",
                        placeholder="Escriu el nom de la tasca",
                        className="oper__input",
                        style={'font-size': '18px','padding': '20px'}
                    ),],
                        className="dropdown__container",
                    ),
                html.Div([
                    html.P(
                        "Hores de dedicació:",
                        className="input__heading",
                        style={'font-size': '18px'}
                    ),
                    dcc.Input(
                        id="enter-hours",
                        type="text",
                        placeholder="2",
                        className="vol__input",
                        style={'font-size': '18px','padding': '10px'}
                    ),],
                        className="dropdown__container",
                    ),
                html.Div([
                    html.P(
                        "Dia:",
                        className="input__heading",
                        style={'font-size': '18px'}
                    ),
                    dcc.DatePickerSingle(
                        id='date-picker',
                        min_date_allowed=date(2015, 8, 5),
                        max_date_allowed=date(2050, 9, 19),
                        initial_visible_month=date(2021, 12, 10),
                        clearable=True,
                        with_portal=True,
                        placeholder="Data",
                        style={'font-size': '18px'}
                    ),],
                        className="input__container",
                ),
                html.Div([
                    html.P(
                        "Hora (HH:MM)",
                        className="input__heading",
                        style={'font-size': '18px'}
                    ),
                    dcc.Input(
                        id="enter-time",
                        placeholder="00:00",
                        className="dropdown__container",
                        style={'font-size': '18px','padding': '10px'}
                    ),
                ],
                        className="input__container",
                        ),
                html.Br(),html.Br(),
                html.Div([
                    html.Button(
                        "Afegeix",
                        id="submit-entry",
                        className="submit__button",
                        style={'font-size': '18px','padding': '10px'}
                    )
                ]
                )],style={'marginLeft': "15%",'marginRight': "15%",'marginTop': "5%"},
                        className="input__container",
                    ))

