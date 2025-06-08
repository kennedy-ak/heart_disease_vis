import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, State, callback, dcc, html

from components.data.data import REGION_COUNTRIES, UNIQUE_REGIONS


def create_sidebar():
    """Function to create a side bar for the page"""
    dropdowns = [
        ("REGION", "region-dropdown", []),
        ("COUNTRY", "country-dropdown", []),
        (
            "GENDER",
            "gender-dropdown",
            [
                {"label": "Both", "value": "Both"},
                {"label": "Male", "value": "Male"},
                {"label": "Female", "value": "Female"},
            ],
        ),
        (
            "WORLD INCOME",
            "income-dropdown",
            [
                {"label": "High income", "value": "High income"},
                {"label": "Lower middle income", "value": "Lower middle income"},
                {"label": "Low income", "value": "Low income"},
                {"label": "Upper middle income", "value": "Upper middle income"},
            ],
        ),
        (
            "METRIC",
            "metric-dropdown",
            [
                {"label": "Prevalence Percent", "value": "Prevalence Percent"},
                {"label": "Prevalence Rate", "value": "Prevalence Rate"},
                {"label": "Prevalence", "value": "Prevalence"},
                {"label": "Death Percent", "value": "Death Percent"},
                {"label": "Death Rate", "value": "Death Rate"},
                {"label": "Death", "value": "Death"},
            ],
        ),
        (
            "AGE",
            "age-dropdown",
            [
                {"label": "Age-standardized", "value": "Age-standardized"},
                {"label": "15-49 years", "value": "15-49 years"},
                {"label": "50-74 years", "value": "50-74 years"},
                {"label": "75+ years", "value": "75+ years"},
            ],
        ),
    ]

    dropdown_elements = [
        html.Div(
            [
                html.H6(label),
                dcc.Dropdown(
                    id=id,
                    options=options,
                    value=(
                        "Death Rate"
                        if id == "metric-dropdown"
                        else (
                            "Both"
                            if id == "gender-dropdown"
                            else "Age-standardized" if id == "age-dropdown" else None
                        )
                    ),
                    placeholder=f"Select {label}",
                    multi=True if id in ["country-dropdown", "region-dropdown"] else False,
                ),
                html.Br(),
            ]
        )
        for label, id, options in dropdowns
    ]

    sidebar_style = {
        "padding": "1rem",
        "background-color": "#f8f9fa",
        "height": "100vh",
        "width": "250px",
        "position": "fixed",
        "z-index": "1",
        "transition": "all 0.3s",
        "box-shadow": "3px 0 10px rgba(0,0,0,0.1)",
        "top": "90px",  # Add top offset equal to navbar height
    }

    return html.Div(
        [
            dbc.Button(
                "☰",
                id="sidebar-toggle",
                color="info",
                className="mb-3",
                style={"position": "absolute", "top": "10px", "right": "-20px", "zIndex": "100"},
            ),
            dbc.Collapse(
                html.Div(
                    [
                        html.H5("Selectors", className="text-center fw-bold"),
                        html.Br(),
                    ]
                    + dropdown_elements,
                    style={"padding": "1rem"},
                ),
                id="sidebar",
                is_open=True,
            ),
        ],
        id="sidebar-container",
        style=sidebar_style,
    )


@callback(
    Output("sidebar", "is_open"),
    Output("sidebar-container", "style"),
    Input("sidebar-toggle", "n_clicks"),
    State("sidebar", "is_open"),
    prevent_initial_call=True,
)
def toggle_sidebar(n_clicks, is_open):
    sidebar_style = {
        "padding": "1rem",
        "background-color": "#f8f9fa",
        "height": "100vh",
        "width": "250px",
        "position": "fixed",
        "z-index": "1",  # Ensure sidebar stays behind the button
        "transition": "all 0.3s",
        "box-shadow": "3px 0 10px rgba(0,0,0,0.1)",
        "top": "90px",  # Add top offset equal to navbar height
    }

    width = "60px" if is_open else "250px"
    return not is_open, {**sidebar_style, "width": width}


@callback(
    Output("country-dropdown", "options"),
    Input("region-dropdown", "value"),
)
def update_country_options(selected_region):
    """Update country dropdown options based on selected region."""
    if not selected_region:
        return []

    # Handle multiple regions
    all_countries = []
    for region in selected_region:
        all_countries.extend(REGION_COUNTRIES.get(region, []))
    return [{"label": country, "value": country} for country in sorted(set(all_countries))]


@callback(
    Output("region-dropdown", "options"),
    Input("url", "pathname"),  # Use URL as trigger to populate on page load
)
def update_region_options(_):
    """Update region dropdown options."""
    regions = UNIQUE_REGIONS
    return [{"label": region, "value": region} for region in regions]
