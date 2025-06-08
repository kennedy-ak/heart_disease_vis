import logging

import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, State, callback, dcc, html, no_update

logger = logging.getLogger(__name__)


from components.common.year_slider import create_year_slider
from components.visualisations import create_chloropleth_map, create_tooltip


def create_world_map_tab():
    """Create the world map tab with choropleth map and year slider."""
    return html.Div(
        [
            dcc.Store(id="general-data"),
            dcc.Store(id="world-map-data"),
            html.Div(
                [
                    html.H2(
                        id="map-title",
                        style={"textAlign": "center", "marginBottom": "5px", "height": "30px"},
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                dcc.Loading(
                                    dcc.Graph(
                                        id="chloropleth-map",
                                        style={"height": "calc(95vh - 160px)"},
                                        config={"displayModeBar": False},
                                    ),
                                    type="default",
                                    color="#00AEF0",
                                ),
                                dcc.Tooltip(
                                    id="graph-tooltip",
                                    style={"position": "absolute", "zIndex": 1000}
                                ),
                            ],
                            style={"position": "relative", "width": "100%", "height": "100%"},
                        ),
                        style={"position": "relative", "width": "100%", "height": "100%"},
                    ),
                    html.Div(
                        create_year_slider(),
                        style={"height": "50px", "marginTop": "2px"},
                    ),
                ],
                id="world-map-container",
                style={
                    "height": "100%",
                    "display": "flex",
                    "flexDirection": "column",
                    "padding": "5px",
                },
            ),
        ]
    )


@callback(
    Output("map-title", "children"),
    Input("year-slider", "value"),
    Input("metric-dropdown", "value"),
    Input("gender-dropdown", "value"),
)
def update_map_title(year, metric, gender):
    """Update the map title based on selected year and metric."""
    gender = ": " + gender if gender != "Both" else ""
    if not year or not metric:
        return ""
    return f"{metric} for {year} {gender}"


@callback(
    Output("chloropleth-map", "figure"),
    Input("world-map-data", "data"),
    Input("metric-dropdown", "value"),
    Input("gender-dropdown", "value"),
)
def update_map(filtered_data, metric, gender):
    """Update the choropleth map based on filtered data."""
    if not filtered_data or not metric or not gender:
        return create_empty_message("Please select metric and gender")

    df = pd.DataFrame(filtered_data)
    if df.empty:
        return create_empty_message("No data available for the selected filters")

    return create_chloropleth_map(filtered_data, metric, gender)


def create_empty_message(message):
    """Create an empty figure with a centered message."""
    return {
        "data": [],
        "layout": {
            "xaxis": {"visible": False},
            "yaxis": {"visible": False},
            "annotations": [
                {
                    "text": message,
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {"size": 28},
                }
            ],
            "height": 600,
        },
    }


@callback(
    Output("graph-tooltip", "show"),
    Output("graph-tooltip", "bbox"),
    Output("graph-tooltip", "children"),
    Input("chloropleth-map", "hoverData"),
    Input("metric-dropdown", "value"),
    Input("gender-dropdown", "value"),
    Input("year-slider", "value"),
    Input("age-dropdown", "value"),
)
def display_hover(hover_data, metric, gender, year, age):
    """Display time series plot in tooltip when hovering over a country."""
    if not hover_data or not metric or not gender:
        return False, no_update, no_update

    pt = hover_data["points"][0]
    country_name = pt["location"]

    fig, risk_factors = create_tooltip(country_name, metric, gender, age, year)

    if fig is None:
        children = html.Div(
            risk_factors["message"],
            style={
                "backgroundColor": "white",
                "padding": "10px",
                "borderRadius": "5px",
                "border": "1px solid #ddd",
            },
        )
    else:
        children = [
            dcc.Graph(
                figure=fig,
                config={"displayModeBar": False},
                style={"width": "300px", "height": "200px"},
            ),
            html.Div(
                [
                    html.H6(
                        f"Risk Factors ({risk_factors.get('Year', 'Latest Year')})",
                        style={"marginTop": "10px", "marginBottom": "5px", "fontSize": "12px"},
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Strong(f"{k}: ", style={"fontSize": "11px"}),
                                    html.Span(v, style={"fontSize": "11px"}),
                                ],
                                style={"marginBottom": "3px"},
                            )
                            for k, v in risk_factors.items()
                            if k != "Year"
                        ],
                        style={"paddingLeft": "5px"},
                    ),
                ],
                style={"backgroundColor": "white", "padding": "5px"},
            ),
        ]

    bbox = pt["bbox"]
    return True, bbox, children
