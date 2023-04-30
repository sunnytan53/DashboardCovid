import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


pages = {"line": ["Normal"], "bar": ["Normal"], "pie": ["Normal"]}
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        dbc.NavbarSimple(
            children=[
                *(
                    dbc.DropdownMenu(
                        children=[
                            dbc.DropdownMenuItem(items[i], href=f"/{name}{i}")
                            for i in range(len(items))
                        ],
                        class_name="ps-5",
                        label=name.capitalize(),
                    )
                    for name, items in pages.items()
                ),
                html.Div("Current Chart:", className="ps-5 fs-4 text-white"),
                html.Div("", id="current-page", className="ps-3 fs-4 text-danger")
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


@app.callback(
    Output("current-page", "children"),
    Input("url", "pathname"),
)
def update_nav_url(url: str):
    if url == "/":
        return "Select a chart to start!"
    name = url[1:-1]
    return f"{name.capitalize()} - {pages[name][int(url[-1])]}"


if __name__ == "__main__":
    app.run_server(debug=True)
