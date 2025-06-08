import logging

import dash_bootstrap_components as dbc
import polars as pl
from dash import Input, Output, callback, dcc, html

from components.common.gender_metric_selector import get_metric_column
from components.visualisations import create_trend_plot

logger = logging.getLogger(__name__)


def create_trends_tab():
    """Function to create layout and visualations in the trends tab"""
    return dcc.Loading(
        html.Div(
            [
                dcc.Store(id="trends-data"),
                html.Br(),
                html.Div(id="trend-plots", style={"height": "100%"}),
                html.Br(),
            ]
        ),
        type="default",
        color="#00AEF0",
    )


@callback(
    Output("trend-plots", "children"),
    Input("trends-data", "data"),
    Input("metric-dropdown", "value"),
    Input("gender-dropdown", "value"),
)
def update_trend_plots(trends_data, metric, gender):
    """Update trend plots with projection styling

    Args:
        trends_data (dict): Dictionary containing the trends data
        metric (str): Selected metric
        gender (str): Selected gender

    Returns:
        dcc.Graph: Graph component with all causes plotted
    """
    if not trends_data or not metric or not gender:
        return html.Div("No Data")

    df = pl.DataFrame(trends_data)

    return dcc.Loading(
        create_trend_plot(df, metric, gender),
        type="default",
        color="#00AEF0",
    )
