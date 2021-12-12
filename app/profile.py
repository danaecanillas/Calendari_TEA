
import dash_html_components as html
import dash_core_components as dcc
import aux_ as aux
from dash.dependencies import Input, Output
import base64

dies = ["dl","dm","dx","dj","dv","ds","dg"]
DIES = ["Dilluns","Dimarts","Dimecres","Dijous","Divendres","Dissabte","Diumenge"]
hores = ["09:00-10:00","10:00-11:00","11:00-12:00",
        "12:00-13:00","13:00-14:00","14:00-15:00","15:00-16:00","16:00-17:00",
         "17:00-18:00","18:00-19:00","19:00-20:00","20:00-21:00"]

normal_button_style ={
    'padding': '10px',
    "width": "100%"
}
horari = {}
for dia in dies:
    horari[dia] = hores

def b64_image(image_filename):
    with open(image_filename, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')

def profile_tab():
    lst=[]
    i = 0
    lst.append(html.Div([html.Div([html.H2("Disponibilitat horària")], style = {'display': 'inline-block','padding':"70px"}),html.Div([html.Img(src=b64_image("img/horari.png"),style = {'height':'150px'})], style = {'display': 'inline-block'})], style = {'display': 'inline-block','text-align':'right'}))
    for dia, hores in horari.items():
        lst.append(html.H3(DIES[i]))
        for hora in hores:   
            lst.append(html.Div([html.Button(hora, id=dia+hora,
                n_clicks=0,style=normal_button_style)], style = {'display': 'inline-block'}))
        lst.append(html.Br())
        i+=1
    return html.Div(lst,style={'marginLeft': "20%",'marginRight': "20%"})
