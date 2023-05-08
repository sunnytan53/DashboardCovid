import dash
from dash import html
from comps import get_home_layout

dash.register_page(__name__, path="/")

layout = html.Div()
