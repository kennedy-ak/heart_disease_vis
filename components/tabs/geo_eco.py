import logging

import dash_bootstrap_components as dbc
import pandas as pd
import polars as pl
from dash import Input, Output, callback, dcc, html

logger = logging.getLogger(__name__)

from components.common.filter_slider import create_filter_slider
from components.common.gender_metric_selector import get_metric_column
from components.common.year_slider import create_year_slider
from components.visualisations import (
    create_bar_plot,
    create_histogram_plot,
    create_line_plot,
    create_sankey_diagram,
    create_scatter_plot,
)


def create_geo_eco_tab():
    """Function to create layout and visualations in the geo eco tab"""
    return dcc.Loading(
        dbc.Container(
            [
                # Add Store component for data
                dcc.Store(id="geo-eco-data"),
                dcc.Store(id="sankey-data"),
                dbc.Row(
                    [
                        dbc.Col(
                            create_filter_slider(),
                            width=12,
                        ),
                    ],
                    className="mb-3",
                ),
                html.Div(id="geo-eco-plots"),
                create_year_slider(min_year=1990, max_year=2021, default=2021),
            ],
            fluid=True,
        )
    )


@callback(
    Output("geo-eco-plots", "children"),
    Input("geo-eco-data", "data"),
    Input("sankey-data", "data"),
    Input("metric-dropdown", "value"),
    Input("gender-dropdown", "value"),
    Input("top-filter-slider", "value"),
    Input("year-slider", "value"),
)
def create_geo_eco_plots(data, sankey_data, metric, gender, top_n, year):
    """Create a grid of plots using visualizations from visualisations.py."""
    if not data or not metric or not gender:
        print(
            "Missing data:", not data, "Missing metric:", not metric, "Missing gender:", not gender
        )
        return html.Div("Please select metric and gender", style={"margin": "20px"})

    df = pl.DataFrame(data)

    col = get_metric_column(gender, metric)

    print("Metric column:", col)
    if not col or col not in df.columns:
        return html.Div("Selected metric data not available", style={"margin": "20px"})

    # Create plots

    return dcc.Loading(
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        html.H4("GDP vs Death Rate", className="text-center")
                                    ),
                                    dbc.CardBody(
                                        create_scatter_plot(
                                            data=df.filter(pl.col("Year").eq(year)).drop_nulls(
                                                subset=["gdp_pc", col]
                                            ),
                                            x_metric="gdp_pc",
                                            y_metric=col,
                                            # gender="Both",
                                            hue="WB_Income",
                                            top_n=top_n,
                                        ),
                                        style={"height": "350px", "overflow": "auto"},
                                    ),
                                ],
                                className="mb-3 shadow-sm",
                            ),
                            xs=12,
                            sm=12,
                            md=6,
                            lg=6,
                            xl=6,
                        ),
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        html.H4(f"{metric} Distribution", className="text-center")
                                    ),
                                    dbc.CardBody(
                                        create_histogram_plot(
                                            col,
                                            df.filter(pl.col("Year").eq(year)).drop_nulls(
                                                subset=[col]
                                            ),
                                        ),
                                        style={"height": "350px", "overflow": "auto"},
                                    ),
                                ],
                                className="mb-3 shadow-sm",
                            ),
                            xs=12,
                            sm=12,
                            md=6,
                            lg=6,
                            xl=6,
                        ),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        html.H4(f"{metric} Top {top_n} Countries", className="text-center")
                                    ),
                                    dbc.CardBody(
                                        create_bar_plot(
                                            col,
                                            df.filter(pl.col("Year").eq(year)).drop_nulls(
                                                subset=[col]
                                            ),
                                            top_n=top_n,
                                        ),
                                        style={"height": "350px", "overflow": "auto"},
                                    ),
                                ],
                                className="mb-3 shadow-sm",
                            ),
                            xs=12,
                            sm=12,
                            md=6,
                            lg=6,
                            xl=6,
                        ),
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        html.H4("Sankey Diagram", className="text-center")
                                    ),
                                    dbc.CardBody(
                                        create_sankey_diagram(sankey_data, metric, gender),
                                        style={"height": "350px", "overflow": "auto"},
                                    ),
                                ],
                                className="mb-3 shadow-sm",
                            ),
                            xs=12,
                            sm=12,
                            md=6,
                            lg=6,
                            xl=6,
                        ),
                    ]
                ),
            ],
            fluid=True,
            style={
                "backgroundColor": "#f8f9fa",
                "padding": "15px",
                "borderRadius": "8px",
            },
        ),
        type="default",
        color="#00AEF0",
    )
