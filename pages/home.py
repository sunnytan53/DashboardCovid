import dash
from dash import html

dash.register_page(__name__, path="/")

layout = html.Div([html.Img(src=dash.get_asset_url(f"{x}.png")) for x in ["line", "bar", "pie"]])
