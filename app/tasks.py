import dash_html_components as html
import dash_core_components as dcc
import aux
import dash
from dash.dependencies import Input, Output

from datetime import date

def tasks_tab():
    return dcc.Tab(html.Div([
                html.Div([
                    html.P(
                        "Assignatura:",
                        className="input__heading",
                    ),
                    dcc.Dropdown(
                        id="select-subject",
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
                    ),
                html.Div([
                    html.P(
                        "Tipus de tasca:",
                        className="input__heading",
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
                    ),],
                        className="dropdown__container",
                    ),
                html.Div([
                    html.P(
                        "Nom de la tasca:",
                        className="input__heading",
                    ),
                    dcc.Input(
                        id="enter-task",
                        placeholder="Escriu el nom de la tasca",
                        className="oper__input",
                    ),],
                        className="input__container",
                    ),
                html.Div([
                    html.P(
                        "Hores de dedicació:",
                        className="input__heading",
                    ),
                    dcc.Input(
                        id="enter-hours",
                        type="number",
                        value="0",
                        placeholder="Introdueix el número d'hores de dedicació",
                        className="vol__input",
                    ),],
                        className="input__container",
                    ),
                html.Div([
                    html.P(
                        "Deadline:",
                        className="input__heading",
                    ),
                    dcc.DatePickerSingle(
                        id='date-picker',
                        min_date_allowed=date(2015, 8, 5),
                        max_date_allowed=date(2050, 9, 19),
                        initial_visible_month=date(2021, 12, 10),
                        clearable=True,
                        with_portal=True,
                        placeholder="Data"
                    ),],
                        className="input__container",
                ),
                html.Div([
                    html.P(
                        "Time (HH:MM)",
                        className="input__heading",
                    ),
                    dcc.Input(
                        id="enter-time",
                        value="00:00",
                        placeholder="Enter Time (HH:MM)",
                        className="time__input",
                    ),
                ],
                            className="input__container",
                        ),
                html.Div([
                    html.Button(
                        "Registre",
                        id="submit-entry",
                        className="submit__button",
                    )
                ]
                )],
                        className="input__container",
                    ))


def register(submit_entry, select_subject, select_activity, enter_task, enter_hours,date_picker, enter_time):
    if submit_entry:
        print(submit_entry, select_subject, select_activity, enter_task, enter_hours,date_picker, enter_time)
        return "today"
    raise dash.exceptions.PreventUpdate