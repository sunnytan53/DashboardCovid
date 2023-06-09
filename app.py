from dash import html, dcc, Input, Output, callback
import dash
import dash_bootstrap_components as dbc
import calls  # import the callback to update graph

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

pages = ["line", "bar", "pie", "map"]
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        dbc.NavbarSimple(
            children=[
                dbc.NavLink(
                    children=name.capitalize(),
                    href=f"/{name}",
                    id=f"nav-{name}",
                )
                for name in pages
            ],
            brand="COVID19 Dashboard",
            brand_href="/",
            color="dark",
            dark=True,
            links_left=True,
        ),
        dash.page_container,
    ]
)


@callback(
    *(Output(f"nav-{name}", "className") for name in pages),
    Input("url", "pathname"),
)
def update_nav_url(url: str):
    ret = ["px-5"] * len(pages)
    try:
        ret[pages.index(url[1:])] += " bg-light text-dark fw-bold"
    except:
        pass
    return ret


if __name__ == "__main__":
    app.run_server(debug=True)
