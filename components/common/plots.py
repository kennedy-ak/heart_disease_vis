"""Utility module for creating common plot layouts."""

import dash_bootstrap_components as dbc
from dash import html

from components.data.data import data
from components.visualisations import create_bar_plot, create_line_plot, create_scatter_plot


def create_plot_grid(df, col, selected_countries, top_n):
    """Create a grid of plots for visualization.

    Args:
        df (pd.DataFrame): Filtered dataframe to use for plots
        col (str): Column name for metrics
        selected_countries (list): List of selected countries
        top_n (int): Number of top entries to show

    Returns:
        html.Div: A div containing a grid of plots
    """
    plots = {
        "gdp_scatter": dbc.Col(
            create_scatter_plot("gdp_pc", "death_std", df, top_n=top_n),
            width=6,
            className="px-2 py-2",
        ),
        "metric_bar": dbc.Col(
            create_bar_plot(col, df, top_n=top_n), width=6, className="px-2 py-2"
        ),
        "pop_line": dbc.Col(
            create_line_plot("Population", data, countries=selected_countries, top_n=top_n),
            width=6,
            className="px-2 py-2",
        ),
        "gender_scatter": dbc.Col(
            create_scatter_plot("f_deaths", "m_deaths", df), width=6, className="px-2 py-2"
        ),
    }

    row1 = dbc.Row([plots["gdp_scatter"], plots["metric_bar"]], className="g-0 mb-2")
    row2 = dbc.Row([plots["pop_line"], plots["gender_scatter"]], className="g-0")

    return html.Div(
        [row1, row2],
        style={
            "margin": "10px",
            "height": "calc(90vh - 15vh)",
            "backgroundColor": "white",
            "borderRadius": "8px",
            "padding": "15px",
            "boxShadow": "0 2px 4px rgba(0,0,0,0.05)",
        },
    )
