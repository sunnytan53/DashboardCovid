import dash
from init_data import get_df
from comps import get_page_layout

dash.register_page(__name__, name="Bar")

layout = get_page_layout("bar")
