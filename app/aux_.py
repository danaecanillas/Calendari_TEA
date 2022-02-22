import base64
import os.path
from dash import html
from dash import dcc
import numpy as np

# App
APP_TITLE = "Eina de Suport per la Planificació de les Tasques Acadèmiques"

DIES = ["Dilluns","Dimarts","Dimecres","Dijous","Divendres","Dissabte","Diumenge"]

HORES = []
for i in range(24):
    HORES.append(str(i).rjust(2,"0")+":00-"+str((i+1)%24).rjust(2,"0")+":00")

DISPONIBILITAT = np.zeros((7, len(HORES)))

# Page style
tabs_styles = {
    'height': '44px',
    'align-items': 'center'
}

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'border-radius': '15px',
    'background-color': '#F2F2F2',
    'box-shadow': '4px 4px 4px 4px lightgrey',
}
 
tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px',
    'border-radius': '15px',
}

# Buttons style 
red_button_style = {'background-color': 'red',
                    'padding': '10px',
                    "width": "100%"}

blue_button_style = {'background-color': 'rgb(136,204,238)',
                    'padding': '10px',
                    "width": "100%"}

normal_button_style ={
    'padding': '10px',
    "width": "100%"
}

green_button_style = {'background-color': '#76cf63',
                    'padding': '9px',
                    "width": "100%"}

ended_button_style ={
    'background-color': 'rgb(153,153,153)',
    'padding': '10px',
    "width": "100%"
}

# Aux functions
def b64_image(image_filename):
    '''
    This functions codes the image so it can be read by dash
    - image_filename: path of the image (string)
    '''
    with open(image_filename, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')

# def state(hour,day_tasks):
#     res = []
#     for time in day_tasks.keys():
#         time = time[0:2]
#         if hour == time:
#             res.append(red_button_style)
#         elif hour < time:
#             res.append(normal_button_style)
#         elif hour > time:
#             res.append(ended_button_style)
#     return res

# def get_first_task(now,day_tasks):
#     time = str(now.strftime("%H:%M:%S"))[0:2]
#     hour = time+":00"
#     if len(day_tasks.keys()) == 0:
#         print(day_tasks)
#         return "blu"
#     else:
#         if hour in day_tasks.keys():
#             return str(day_tasks[hour].date_time)


def ret_img(activity_type):
    '''
    This function returns the image related to the inputted activity type
    - activity_type: string
    '''
    "Examen", "Projecte", "Estudi", "Fer treball"
    dir_folder = os.path.dirname(__file__)
    if activity_type == "Examen":
        return html.Img(
            src=b64_image(f"{dir_folder}/img/examen.png"),
            style={"width": "60%", "text-align": "center"},
        )
    elif activity_type == "Projecte":
        return html.Img(
            src= b64_image(f"{dir_folder}/img/treball.png"),
            style={"width": "60%", "text-align": "center"},
        )
    elif activity_type == "Estudi":
        return html.Img(
            src=b64_image(f"{dir_folder}/img/estudi.png"),
            style={"width": "60%", "text-align": "center"},
        )
    else:
        return html.Img(
            src=b64_image(f"{dir_folder}/img/feina.png"),
            style={"width": "60%", "text-align": "center"},
        )

