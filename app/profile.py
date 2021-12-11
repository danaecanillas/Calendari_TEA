
import dash_html_components as html
import dash_core_components as dcc
import aux
from dash.dependencies import Input, Output

def profile_tab():
    return  html.Div([html.Div([
                    html.P(
                        "Nom de l'estudiant:",
                        className="input__heading",
                    ),
                    dcc.Input(
                        id="enter-nom",
                        placeholder="Escriu el teu nom",
                        className="oper__input",
                    ),],
                        className="input__container",
                    ),
            html.Div([
                    html.P(
                        "Assignatura:",
                        className="input__heading",
                    ),
                    dcc.Dropdown(
                                                    id="select-reagent",
                                                    options=[
                                                        {"label": i, "value": i}
                                                        for i in [
                                                            "POE",
                                                            "PIVA",
                                                            "TAED1",
                                                            "PE",
                                                            "TFG", 
                                                        ]
                                                    ],
                                                    placeholder="Escull una assignatura",
                                                    className="subject__select",
                                                ),],
                        className="dropdown__container",
                    )])