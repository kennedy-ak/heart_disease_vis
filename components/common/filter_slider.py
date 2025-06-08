from dash import dcc, html


def create_filter_slider():
    """Function to create a year slider on the pages"""
    marks = {i: str(i) for i in range(5, 26, 1)}  # Generate marks for the slider
    return html.Div(
        [
            html.Label("Filter by top:"),
            dcc.Slider(
                id="top-filter-slider",
                min=5,
                max=25,
                step=1,
                value=10,  # Adjusted initial value to be within bounds
                marks=marks,
            ),
        ]
    )
