import base64
import dash_html_components as html

# App
APP_TITLE = "Eina de Suport per la Planificació de les Tasques Acadèmiques"


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

normal_button_style ={
    'padding': '10px',
    "width": "100%"
}

ended_button_style ={
    'background-color': 'rgb(153,153,153)',
    'padding': '10px',
    "width": "100%"
}

# Aux functions
def b64_image(image_filename):
    with open(image_filename, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')

def state(hour,day_tasks):
    res = []
    for time in day_tasks.keys():
        time = time[0:2]
        if hour == time:
            res.append(red_button_style)
        elif hour < time:
            res.append(normal_button_style)
        elif hour > time:
            res.append(ended_button_style)
    return res

def get_first_task(now,day_tasks):
    time = str(now.strftime("%H:%M:%S"))[0:2]
    hour = time+":00"
    if len(day_tasks.keys()) == 0:
        print(day_tasks)
        return "blu"
    else:
        if hour in day_tasks.keys():
            return str(day_tasks[hour].date_time)


def ret_img(activity_type):
    "Examen", "Projecte", "Estudi", "Fer treball"
    if activity_type == "Examen":
        return html.Img(
            src=b64_image("img/examen.png"),
            style={"width": "60%", "text-align": "center"},
        )
    elif activity_type == "Projecte":
        return html.Img(
            src= b64_image("img/treball.png"),
            style={"width": "60%", "text-align": "center"},
        )
    elif activity_type == "Estudi":
        return html.Img(
            src=b64_image("img/estudi.png"),
            style={"width": "60%", "text-align": "center"},
        )
    else:
        return html.Img(
            src=b64_image("img/feina.png"),
            style={"width": "60%", "text-align": "center"},
        )

