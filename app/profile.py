import dash_html_components as html
import dash_core_components as dcc
import aux_ as aux
from dash.dependencies import Input, Output
import base64

horari = {}
for dia in aux.DIES:
    horari[dia] = aux.HORES

def profile_tab():
    return html.Div([
       dcc.Tabs(id="tab-perfil", value='tab-perfil', children=[
           dcc.Tab(label='Afegeix esdeveniment', value='tab-esdeveniment'),
           dcc.Tab(label='Assignatures', value='tab-assignatures'),
           dcc.Tab(label='Disponibilitat Horària', value='tab-disponibilitat'),
        ]), 
        html.Div(id='tab-content-profile')
    ])
    
