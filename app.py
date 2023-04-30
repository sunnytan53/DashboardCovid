import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
pageNames = ["line", "bar", "pie"]

def navbar():
    # return html.Div(
    #     dbc.Nav(
    #         [
    #             dbc.NavLink(
    #                 [
    #                     html.Div(page["name"]),
    #                 ],
    #                 href=page["path"],
    #                 active="exact",
    #             )
    #             for page in dash.page_registry.values()
    #         ]
    #     )
    # )
    return dbc.NavbarSimple(
        children=[
            *(dbc.NavLink(p.capitalize(), href=p) for p in pageNames),
        ],
        brand="COVID Dashboard",
        brand_href="/",
        color="dark",
        dark=True,
        links_left=True
    )


app.layout = html.Div(
    [
        navbar(),
        dash.page_container,
        *(html.Img(src=dash.get_asset_url(f"{x}.png")) for x in pageNames),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
