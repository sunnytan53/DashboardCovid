from dash import Input, Output, callback, Input, Output
import plotly.express as px
from init_data import empty_figure, get_df, get_df_loc
from datetime import datetime
import pandas as pd
from init_data import (
    region_no_limit,
    region_has_states,
    region_has_cities,
    region_to_state_state,
    region_to_state_city,
    state_to_city,
)
import plotly.express as px
from datetime import datetime


@callback(
    Output("select-region", "options"),
    Input("level", "value"),
)
def _switch_select_region(level: str):
    if level == "State":
        return region_has_states
    elif level == "City":
        return region_has_cities
    return region_no_limit


@callback(
    Output("select-state", "placeholder"),
    Output("select-state", "options"),
    Output("select-state", "value"),
    Output("select-state", "disabled"),
    Input("level", "value"),
    Input("select-region", "value"),
    Input("select-region", "options"),
    Input("all-region", "value"),
    Input("all-state", "value"),
)
def _switch_select_state(
    level: str,
    values: list[str],
    region_options: list[str],
    all_region: bool,
    all_state: bool,
):
    ret = ["Select a region above, or check all", [], [], True]
    if level == "Region":
        ret[0] = "Not state or city level"
    else:
        if all_region:
            values = region_options
        if values:
            region_to_state = (
                region_to_state_city if level == "City" else region_to_state_state
            )
            for region in values:
                for state in region_to_state[region]:
                    state_str = f"{region} / {state}"
                    ret[1].append(state_str)
            # show states
            ret[1].sort()
            if all_state:
                ret[0] = "All states selected"
            else:
                ret[3] = False
                ret[0] = "Click to search/select states"
    # empty selection
    return ret


@callback(
    Output("select-city", "placeholder"),
    Output("select-city", "options"),
    Output("select-city", "value"),
    Output("select-city", "disabled"),
    Input("level", "value"),
    Input("select-state", "value"),
    Input("select-state", "options"),
    Input("all-state", "value"),
    Input("all-city", "value"),
)
def _switch_select_city(
    level: str,
    values: str,
    state_options: list[str],
    all_state: bool,
    all_city: bool,
):
    ret = ["Select a state above, or check all", [], [], True]
    if level != "City":
        ret[0] = "Not city level"
    else:
        if all_state:
            values = state_options
        if values:
            for x in values:
                region, state = x.split(" / ")
                for city in state_to_city[state]:
                    ret[1].append(f"{x} / {city}")
            # show cities
            ret[1].sort()
            if all_city:
                ret[3] = True
                ret[0] = "All cities selected"
            else:
                ret[3] = False
                ret[0] = "Click to search/select cities"
    # empty selection
    return ret


@callback(
    Output("all-region", "disabled"),
    Output("all-state", "disabled"),
    Output("all-city", "disabled"),
    Output("all-region", "value"),
    Output("all-state", "value"),
    Output("all-city", "value"),
    Input("level", "value"),
)
def _swtich_all(level: str):
    arr = [False] * 3 + [False] * 3
    if level == "Region":
        arr[1] = True
        arr[2] = True
    elif level == "State":
        arr[2] = True
    return arr


@callback(
    Output("select-region", "placeholder"),
    Output("select-region", "value"),
    Output("select-region", "disabled"),
    Input("all-region", "value"),
)
def _select_all_region(all_region: bool):
    if all_region:
        return "All regions selected", [], True
    return "Click to search/select regions", [], False


@callback(
    Output("date", "min_date_allowed"),
    Output("date", "max_date_allowed"),
    Input("level", "value"),
    Input("period", "value"),
)
def _switch_date_by_level(level: str, period: str):
    df = get_df(level, period[0])
    return df["Date"].min(), df["Date"].max()


@callback(
    Output("graph", "figure"),
    Output("full-graph", "figure"),
    Input("level", "value"),
    Input("select-region", "value"),
    Input("select-state", "value"),
    Input("select-city", "value"),
    Input("select-region", "options"),
    Input("select-state", "options"),
    Input("select-city", "options"),
    Input("all-region", "value"),
    Input("all-state", "value"),
    Input("all-city", "value"),
    Input("date", "start_date"),
    Input("date", "end_date"),
    Input("case", "value"),
    Input("cumu", "value"),
    Input("period", "value"),
    Input("active-page", "pathname"),
    ### sepcific chart options
    Input("line-marker", "value"),
    Input("bar-column", "value"),
    Input("bar-orient", "value"),
    Input("pie-hole", "value"),
)
def update_graph(  # can't use _name here sine import will ignore this function
    level: str,
    region_values: list[str],
    state_values: list[str],
    city_values: list[str],
    region_options: list[str],
    state_options: list[str],
    city_options: list[str],
    all_region: bool,
    all_state: bool,
    all_city: bool,
    start: str,
    end: str,
    case_cat: str,
    to_cumu: str,
    period: str,
    active_page: str,
    ### sepcific chart options
    line_marker: str,
    bar_column: str,
    bar_orient: str,
    pie_hole: str,
):

    valid_region = bool(region_values) or all_region
    valid_state = bool(state_values) or all_state
    valid_city = bool(city_values) or all_city

    df = get_df(level, period[0])
    mask = None
    if level == "City":
        if valid_region and valid_state and valid_city:
            mask = df[level].isin(city_options if all_city else city_values)

    elif level == "State":
        if valid_region and valid_state:
            mask = df[level].isin(state_options if all_state else state_values)

    elif level == "Region":
        if valid_region:
            mask = df[level].isin(region_options if all_region else region_values)

    if mask is None:
        return empty_figure, empty_figure

    if start:
        mask &= df["Date"] >= datetime.strptime(start[:10], "%Y-%m-%d")
    if end:
        mask &= df["Date"] <= datetime.strptime(end[:10], "%Y-%m-%d")
    df = df[mask]

    case_cat += " Cases"
    if to_cumu == "Cumulative":
        df_list = []
        for _, x in df.groupby(level):
            x[case_cat] = x[case_cat].cumsum()
            df_list.append(x)
        df = pd.concat(df_list)

    active_page = active_page[1:]
    if active_page == "bar":
        if bar_orient == "Horizontal":
            fig = px.bar(df, x=case_cat, y="Date", color=level, orientation="h")
        else:
            fig = px.bar(df, x="Date", y=case_cat, color=level)
        if bar_column == "Group":
            fig.update_layout(barmode="group")

    elif active_page == "pie":
        fig = px.pie(df, names=level, values=case_cat, hole=float(pie_hole) if pie_hole else 0)
        fig.update_traces(textposition="inside", textinfo="percent+label")

    elif active_page == "map":
        df_list2 = []
        for l, x in df.groupby(level):
            df_list2.append([l, x[case_cat].sum()])
        df = pd.DataFrame(df_list2, columns=[level, case_cat])
        fig = px.scatter_geo(
            df.merge(get_df_loc(level), on=level),
            lat="Latitude",
            lon="Longitude",
            size=case_cat,
            color=level,
        )

    else:
        if line_marker == "Simple":
            fig = px.line(df, x="Date", y=case_cat, color=level, markers=True)
        elif line_marker == "Complex":
            fig = px.line(df, x="Date", y=case_cat, color=level, symbol=level)
        else:
            fig = px.line(df, x="Date", y=case_cat, color=level)

    fig.update_layout(height=600)
    return fig, fig
