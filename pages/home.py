import dash
from dash import html
from comps import get_page_layout

dash.register_page(__name__, path="/")

layout = html.Div(get_page_layout("home", True))
