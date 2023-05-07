import dash
from comps import get_page_layout

dash.register_page(__name__, name="Map")

layout = get_page_layout("map")
