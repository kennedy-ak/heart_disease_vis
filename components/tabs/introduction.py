import dash_bootstrap_components as dbc
from dash import Input, Output, callback, html
from dash.exceptions import PreventUpdate


def create_introduction_tab():

    return dbc.Container(
        [
            # Main Title
            dbc.Row(
                [
                    dbc.Col(
                        html.H1(
                            "Heart Disease Global Insights",
                            className="text-center text-primary fw-bold mb-4",
                        ),
                        width=12,
                    )
                ]
            ),
            # Tab Overview Cards
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        "🌐 World Map Visualization",
                                        className="bg-primary text-white",
                                    ),
                                    dbc.CardBody(
                                        [
                                            html.P(
                                                "Interactive choropleth map showing heart disease prevalence across countries.",
                                                className="card-text",
                                            ),
                                            html.Ul(
                                                [
                                                    html.Li("Country-level heart disease metrics"),
                                                    html.Li(
                                                        "Color-coded intensity representation"
                                                    ),
                                                    html.Li("Click to explore country details"),
                                                ],
                                                className="small",
                                            ),
                                        ]
                                    ),
                                ],
                                className="mb-3 shadow-sm",
                            )
                        ],
                        md=3,
                    ),
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        "💰 Geo-Economic Features",
                                        className="bg-success text-white",
                                    ),
                                    dbc.CardBody(
                                        [
                                            html.P(
                                                "Analyze heart disease through economic and geographical lenses.",
                                                className="card-text",
                                            ),
                                            html.Ul(
                                                [
                                                    html.Li("GDP correlation analysis"),
                                                    html.Li("Economic indicator comparisons"),
                                                    html.Li("Regional trend explorations"),
                                                ],
                                                className="small",
                                            ),
                                        ]
                                    ),
                                ],
                                className="mb-3 shadow-sm",
                            )
                        ],
                        md=3,
                    ),
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        "🏥 Healthcare Insights", className="bg-info text-white"
                                    ),
                                    dbc.CardBody(
                                        [
                                            html.P(
                                                "Deep dive into healthcare-related heart disease factors.",
                                                className="card-text",
                                            ),
                                            html.Ul(
                                                [
                                                    html.Li("Medical intervention effectiveness"),
                                                    html.Li("Healthcare spending analysis"),
                                                    html.Li("Treatment outcome comparisons"),
                                                ],
                                                className="small",
                                            ),
                                        ]
                                    ),
                                ],
                                className="mb-3 shadow-sm",
                            )
                        ],
                        md=3,
                    ),
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        "📈 Trends Analysis", className="bg-warning text-white"
                                    ),
                                    dbc.CardBody(
                                        [
                                            html.P(
                                                "Comprehensive temporal analysis of heart disease trends.",
                                                className="card-text",
                                            ),
                                            html.Ul(
                                                [
                                                    html.Li("Long-term trend visualization"),
                                                    html.Li("Year-over-year comparisons"),
                                                    html.Li("Predictive trend insights"),
                                                ],
                                                className="small",
                                            ),
                                        ]
                                    ),
                                ],
                                className="mb-3 shadow-sm",
                            )
                        ],
                        md=3,
                    ),
                ],
                className="mb-4",
            ),
            # Dataset Overview Cards
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader("📊 Dataset Metrics", className="bg-light"),
                                    dbc.CardBody(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            html.H5(
                                                                "Countries",
                                                                className="text-center",
                                                            ),
                                                            html.H3(
                                                                "194",
                                                                className="text-center text-primary",
                                                            ),
                                                        ],
                                                        width=4,
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            html.H5(
                                                                "Years", className="text-center"
                                                            ),
                                                            html.H3(
                                                                "1980-2021",
                                                                className="text-center text-primary",
                                                            ),
                                                        ],
                                                        width=4,
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            html.H5(
                                                                "Data Points",
                                                                className="text-center",
                                                            ),
                                                            html.H3(
                                                                "50K+",
                                                                className="text-center text-primary",
                                                            ),
                                                        ],
                                                        width=4,
                                                    ),
                                                ]
                                            )
                                        ]
                                    ),
                                ],
                                className="shadow-sm",
                            )
                        ],
                        width=12,
                    )
                ],
                className="mb-4",
            ),
            # Bottom Section
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            html.H3(
                                                                "Explore. Analyze. Understand.",
                                                                className="text-primary mb-3",
                                                            ),
                                                            html.P(
                                                                "Dive deep into the global landscape of heart disease with our comprehensive visualization dashboard.",
                                                                className="lead",
                                                            ),
                                                            dbc.Button(
                                                                "Start Exploring",
                                                                id="start-exploring-button",
                                                                color="primary",
                                                                className="mt-3",
                                                            ),
                                                        ],
                                                        md=8,
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            html.Div(
                                                                [
                                                                    html.I(
                                                                        className="fas fa-heartbeat fa-5x text-danger"
                                                                    ),
                                                                ],
                                                                className="text-center",
                                                            )
                                                        ],
                                                        md=4,
                                                    ),
                                                ]
                                            )
                                        ]
                                    )
                                ],
                                className="bg-light shadow-lg",
                            )
                        ]
                    )
                ]
            ),
        ],
        fluid=True,
    )


@callback(
    Output("tab-1-link", "n_clicks"),
    Input("start-exploring-button", "n_clicks"),
    prevent_initial_call=True,
)
def navigate_to_world_map(n_clicks):
    """
    Trigger the World Map nav link when Start Exploring is clicked
    """
    if n_clicks:
        return 1
    return 0
    return dbc.Container(
        [
            # Main Title
            dbc.Row(
                [
                    dbc.Col(
                        html.H1(
                            "Heart Disease Global Insights",
                            className="text-center text-primary fw-bold mb-4",
                        ),
                        width=12,
                    )
                ]
            ),
            # Tab Overview Cards
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        "🌐 World Map Visualization",
                                        className="bg-primary text-white",
                                    ),
                                    dbc.CardBody(
                                        [
                                            html.P(
                                                "Interactive choropleth map showing heart disease prevalence across countries.",
                                                className="card-text",
                                            ),
                                            html.Ul(
                                                [
                                                    html.Li("Country-level heart disease metrics"),
                                                    html.Li(
                                                        "Color-coded intensity representation"
                                                    ),
                                                    html.Li("Click to explore country details"),
                                                ],
                                                className="small",
                                            ),
                                        ]
                                    ),
                                ],
                                className="mb-3 shadow-sm",
                            )
                        ],
                        md=3,
                    ),
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        "💰 Geo-Economic Features",
                                        className="bg-success text-white",
                                    ),
                                    dbc.CardBody(
                                        [
                                            html.P(
                                                "Analyze heart disease through economic and geographical lenses.",
                                                className="card-text",
                                            ),
                                            html.Ul(
                                                [
                                                    html.Li("GDP correlation analysis"),
                                                    html.Li("Economic indicator comparisons"),
                                                    html.Li("Regional trend explorations"),
                                                ],
                                                className="small",
                                            ),
                                        ]
                                    ),
                                ],
                                className="mb-3 shadow-sm",
                            )
                        ],
                        md=3,
                    ),
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        "🏥 Healthcare Insights", className="bg-info text-white"
                                    ),
                                    dbc.CardBody(
                                        [
                                            html.P(
                                                "Deep dive into healthcare-related heart disease factors.",
                                                className="card-text",
                                            ),
                                            html.Ul(
                                                [
                                                    html.Li("Medical intervention effectiveness"),
                                                    html.Li("Healthcare spending analysis"),
                                                    html.Li("Treatment outcome comparisons"),
                                                ],
                                                className="small",
                                            ),
                                        ]
                                    ),
                                ],
                                className="mb-3 shadow-sm",
                            )
                        ],
                        md=3,
                    ),
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        "📈 Trends Analysis", className="bg-warning text-white"
                                    ),
                                    dbc.CardBody(
                                        [
                                            html.P(
                                                "Comprehensive temporal analysis of heart disease trends.",
                                                className="card-text",
                                            ),
                                            html.Ul(
                                                [
                                                    html.Li("Long-term trend visualization"),
                                                    html.Li("Year-over-year comparisons"),
                                                    html.Li("Predictive trend insights"),
                                                ],
                                                className="small",
                                            ),
                                        ]
                                    ),
                                ],
                                className="mb-3 shadow-sm",
                            )
                        ],
                        md=3,
                    ),
                ],
                className="mb-4",
            ),
            # Dataset Overview Cards
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader("📊 Dataset Metrics", className="bg-light"),
                                    dbc.CardBody(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            html.H5(
                                                                "Countries",
                                                                className="text-center",
                                                            ),
                                                            html.H3(
                                                                "194",
                                                                className="text-center text-primary",
                                                            ),
                                                        ],
                                                        width=4,
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            html.H5(
                                                                "Years", className="text-center"
                                                            ),
                                                            html.H3(
                                                                "1950-2022",
                                                                className="text-center text-primary",
                                                            ),
                                                        ],
                                                        width=4,
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            html.H5(
                                                                "Data Points",
                                                                className="text-center",
                                                            ),
                                                            html.H3(
                                                                "50K+",
                                                                className="text-center text-primary",
                                                            ),
                                                        ],
                                                        width=4,
                                                    ),
                                                ]
                                            )
                                        ]
                                    ),
                                ],
                                className="shadow-sm",
                            )
                        ],
                        width=12,
                    )
                ],
                className="mb-4",
            ),
            # Bottom Section
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            html.H3(
                                                                "Explore. Analyze. Understand.",
                                                                className="text-primary mb-3",
                                                            ),
                                                            html.P(
                                                                "Dive deep into the global landscape of heart disease with our comprehensive visualization dashboard.",
                                                                className="lead",
                                                            ),
                                                            dbc.Button(
                                                                "Start Exploring",
                                                                color="primary",
                                                                className="mt-3",
                                                            ),
                                                        ],
                                                        md=8,
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            html.Div(
                                                                [
                                                                    html.I(
                                                                        className="fas fa-heartbeat fa-5x text-danger"
                                                                    ),
                                                                ],
                                                                className="text-center",
                                                            )
                                                        ],
                                                        md=4,
                                                    ),
                                                ]
                                            )
                                        ]
                                    )
                                ],
                                className="bg-light shadow-lg",
                            )
                        ]
                    )
                ]
            ),
        ],
        fluid=True,
    )
