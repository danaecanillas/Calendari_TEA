import base64

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
# Data
fruits = {
            "t1":['10:00','potato','pending'],"t2":['18:00','potato','pending'],
            "t3":['19:00','potato','pending'],"t4":['20:00','potato','pending']
            }

# Aux functions

def b64_image(image_filename):
    with open(image_filename, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')
