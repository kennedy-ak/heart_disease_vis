import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, dcc, html


def create_year_slider(min_year=1980, max_year=2021, default=2021):
    """Generate marks for the slider using a dictionary comprehension"""
    marks = {
        str(year): str(year) for year in range(min_year, max_year + 1, 10)  # Increased interval
    }

    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Button(
                                "▶️",
                                id="play-button",
                                n_clicks=0,
                                style={
                                    "border": "none",
                                    "background": "none",
                                    "font-size": "20px",
                                    "cursor": "pointer",
                                },
                            ),
                            dcc.Interval(
                                id="animation-interval",
                                interval=5000,  # 5 second between frames
                                disabled=True,
                            ),
                        ],
                        width=1,
                    ),
                    dbc.Col(
                        [
                            dbc.Label("Select Year"),
                            dcc.Slider(
                                id="year-slider",
                                min=min_year,
                                max=max_year,
                                value=default,
                                marks=marks,
                                step=1,
                                tooltip={"placement": "bottom", "always_visible": True},
                                included=False,
                            ),
                        ],
                        width=11,
                    ),
                ]
            )
        ]
    )


# callback functions
@callback(
    Output("animation-interval", "disabled"),
    Output("play-button", "children"),
    Input("play-button", "n_clicks"),
    State("animation-interval", "disabled"),
)
def toggle_animation(n_clicks, disabled):
    """Function to add a toggle animation the sidebar"""
    if n_clicks:
        return not disabled, "⏸️" if disabled else "▶️"
    return True, "▶️"


@callback(
    Output("year-slider", "value"),
    Input("animation-interval", "n_intervals"),
    State("year-slider", "value"),
    State("year-slider", "min"),
    State("year-slider", "max"),
)
def update_year_on_interval(n_intervals, current_year, min_year, max_year):
    """Function to update the year slider"""
    if current_year is None:
        return min_year
    next_year = current_year + 1 if current_year < max_year else min_year
    return next_year
