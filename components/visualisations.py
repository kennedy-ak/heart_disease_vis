import logging
from collections import OrderedDict
from functools import lru_cache

import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import polars as pl
from dash import dcc, html
from scipy import stats
from scipy.stats import t
from statsmodels.nonparametric.smoothers_lowess import lowess

from components.common import gender_metric_selector
from components.common.gender_metric_selector import get_metric_column
from components.data.data import UNIQUE_INCOMES, UNIQUE_REGIONS, data

logger = logging.getLogger(__name__)

# Common layout settings
BASE_LAYOUT = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {"size": 12},
}

COMMON_LAYOUT = {
    "showlegend": False,
}


GRID_SETTINGS = {"gridwidth": 1, "gridcolor": "rgba(128,128,128,0.1)", "zeroline": False}


@lru_cache(maxsize=32)
def get_title_text(metric):
    """Cache title text generation."""
    mapping = {
        "valdeathsnumberfemale": "Female Deaths",
        "valdeathsnumbermale": "Male Deaths",
        "valdeathsnumberboth": "Deaths",
        "valdeathsratefemale": "Female Death Rate",
        "valdeathsratemale": "Male Death Rate",
        "valdeathsrateboth": "Death Rate",
        "valdeathspercentfemale": "Female Death %",
        "valdeathspercentmale": "Male Death %",
        "valdeathspercentboth": "Death %",
        "valprevnumberfemale": "Female Prevalence",
        "valprevnumbermale": "Male Prevalence",
        "valprevnumberboth": "Prevalence",
        "valprevratefemale": "Female Prevalence Rate",
        "valprevratemale": "Male Prevalence Rate",
        "valprevrateboth": "Prevalence Rate",
        "valprevpercentfemale": "Female Prevalence %",
        "valprevpercentmale": "Male Prevalence %",
        "valprevpercentboth": "Prevalence %",
    }
    return mapping.get(metric, metric).replace("_", " ").title()


def create_scatter_plot(
    x_metric, y_metric, data, size=None, hue=None, top_n=5, add_diagonal=False
):
    """Create a scatter plot comparing two metrics with optional size and color encoding."""
    # print(f"Creating scatter plot: x={x_metric}, y={y_metric}, data shape={data.shape}")
    # print(f"Data columns: {data.columns.tolist()}")
    # print(f"Data values:\n{data[[x_metric, y_metric]].head()}")

    if data.is_empty() or x_metric not in data.columns or y_metric not in data.columns:
        return create_no_data_figure("No data available for selected metrics")

    plot_data = data

    # Convert numeric columns
    plot_data = plot_data.with_columns(
        [pl.col(x_metric).cast(pl.Float64), pl.col(y_metric).cast(pl.Float64)]
    )
    plot_data = plot_data.drop_nulls(subset=[x_metric, y_metric])

    print(f"After numeric conversion: shape={plot_data.shape}")
    print(f"Numeric values:\n{plot_data[[x_metric, y_metric]].head()}")

    # Take top N if specified
    if top_n:
        plot_data = plot_data.sort(y_metric, descending=True).limit(int(top_n))
        print(f"After top_n filter: shape={plot_data.shape}")

    fig = px.scatter(
        data_frame=plot_data,
        x=x_metric,
        y=y_metric,
        color=hue if hue in plot_data.columns else None,
        hover_name="Entity",
        labels={x_metric: get_title_text(x_metric), y_metric: get_title_text(y_metric)},
        size=size,
    )

    # Add diagonal line if requested
    if add_diagonal:
        min_val = min(plot_data[x_metric].min(), plot_data[y_metric].min())
        max_val = max(plot_data[x_metric].max(), plot_data[y_metric].max())
        fig.add_trace(
            go.Scatter(
                x=[min_val, max_val],
                y=[min_val, max_val],
                mode="lines",
                name="45° line",
                line=dict(color="gray", dash="dash"),
                opacity=0.5,
            )
        )

    layout = {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"size": 12},
        "showlegend": True if hue or add_diagonal else False,
        "margin": {"l": 60, "r": 30, "t": 50, "b": 50},
        "height": 300,
        "title": {
            "text": f"{get_title_text(x_metric)} vs {get_title_text(y_metric)}",
            "y": 1,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 14},
        },
    }

    fig.update_layout(**layout)
    for axis in [fig.update_xaxes, fig.update_yaxes]:
        axis(**GRID_SETTINGS)

    return dcc.Graph(figure=fig, style={"height": "100%"}, config={"displayModeBar": False})


def create_tooltip(country_name, metric, gender, age, selected_year=None):
    """Create a tooltip with time series plot and risk factors for a country."""
    # Get data for the country
    df = data
    df = df.filter(pl.col("Entity").eq(country_name))

    if df.height == 0:
        return create_no_data_figure("No data available for this country"), {}

    # Get appropriate column based on metric and gender
    col = get_metric_column(gender, metric)
    df = df.with_columns(pl.col(col).cast(pl.Float64, strict=False))
    is_percent = "percent" in metric.lower()

    # Create time series plot for cardiovascular diseases
    cv_df = df.filter(
        (pl.col("cause").str.to_lowercase().eq("cardiovascular diseases"))
        & (pl.col("age").eq(age))
    )
    cv_df = cv_df.drop_nulls(subset=[col])

    if cv_df.height == 0:
        return None, {"message": f"No data available for {metric} with age group: {age}"}

    fig = go.Figure()

    # Add main time series
    cv_df_pd = cv_df.sort("Year").to_pandas()
    fig.add_trace(
        go.Scatter(
            x=cv_df_pd["Year"],
            y=cv_df_pd[col],
            mode="lines+markers",
            name="Actual",
        )
    )

    # Add marker for selected year if provided
    if selected_year:
        year_data = cv_df.filter(pl.col("Year").eq(selected_year))
        if year_data.height > 0:
            year_value = year_data.select(pl.col(col)).row(0)[0]
            fig.add_trace(
                go.Scatter(
                    x=[selected_year],
                    y=[year_value],
                    mode="markers",
                    marker=dict(size=10, color="red"),
                    name=f"{selected_year}",
                )
            )

    fig.update_layout(
        title=f"{country_name} {metric} Over Time",
        xaxis_title="Year",
        yaxis_title=metric,
        height=300,
        showlegend=False,
        margin={"l": 60, "r": 30, "t": 50, "b": 50},
    )

    risk_factors = OrderedDict()

    if selected_year:
        # Add other causes
        other_causes = df.filter(
            (pl.col("Year").eq(selected_year))
            & ~(pl.col("cause").str.to_lowercase().str.contains("cardiovascular diseases"))
            & (pl.col("age").eq(age))
        )
        other_causes = other_causes.drop_nulls(subset=[col])

        # Sort causes by value and add to risk factors
        other_causes = other_causes.sort(col, descending=True)
        for row in other_causes.iter_rows(named=True):
            risk_factors[row["cause"]] = format_value(row[col], is_percent=is_percent)

    return fig, risk_factors


def create_trend_plot(data, metric, gender):
    """Create a trend plot showing the metric over time for each cause."""
    df = data

    # Get appropriate column based on metric and gender
    col = get_metric_column(gender, metric)
    if not col or df.height == 0:
        return create_no_data_figure("No data available for selected filters")

    # Create figure
    fig = go.Figure()

    # Color mapping for causes
    colors = {
        "Cardiovascular diseases": "#1f77b4",
        "Ischemic heart disease": "#ff7f0e",
        "Lower extremity peripheral arterial disease": "#2ca02c",
        "Other": "#d62728",
        "Pulmonary Arterial Hypertension": "#9467bd",
    }

    # Add traces for each cause
    for cause in df["cause"].unique():
        cause_data = df.filter(pl.col("cause").eq(cause))
        yearly_data = cause_data.group_by("Year").agg(pl.col(col).mean()).sort("Year")

        # Split data at 2021.5
        actual = yearly_data.filter(pl.col("Year") <= 2021.5)
        projected = yearly_data.filter(pl.col("Year") > 2021.5)

        color = colors.get(cause, "#17becf")

        # Add actual data (solid line)
        fig.add_trace(
            go.Scatter(
                x=actual["Year"],
                y=actual[col],
                name=cause,
                mode="lines",
                line=dict(color=color),
            )
        )

        # Add projected data (dotted line)
        if not projected.is_empty():
            fig.add_trace(
                go.Scatter(
                    x=projected["Year"],
                    y=projected[col],
                    name=f"{cause} (Projected)",
                    mode="lines",
                    line=dict(
                        color=color,
                        dash="dot",
                    ),
                    showlegend=False,
                )
            )

    fig.update_layout(
        title=f"{metric} Trends Over Time",
        xaxis_title="Year",
        yaxis_title=metric,
        height=600,
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255, 255, 255, 0.8)",
        ),
        hovermode="x unified",
    )

    return dcc.Graph(figure=fig, config={"displayModeBar": False})


def format_value(value, is_percent=True, is_estimate=True, is_obesity=False):
    """Format a value for display.

    Args:
        value: The value to format
        is_percent (bool): Whether the value is a percentage
        is_estimate (bool): Whether to show decimal places
        is_obesity (bool): Whether this is an obesity rate (already in percentage)

    Returns:
        str: Formatted value
    """
    if pd.isna(value):
        return "N/A"

    try:
        if is_percent:
            if is_obesity:
                return f"{float(value):.1f}%"
            return f"{float(value) * 100:.1f}%"
        elif isinstance(value, (int, float)):
            if value >= 1000000:
                return f"{value/1000000:.1f}M"
            elif value >= 1000:
                return f"{value/1000:.1f}K"
            else:
                return f"{value:.1f}" if is_estimate else f"{int(value):,}"
        return str(value)
    except:
        return "N/A"


def create_no_data_figure(message="No data available"):
    """Create an empty figure with a message when no data is available."""
    fig = go.Figure()
    fig.add_annotation(
        text=message, xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(size=14)
    )
    fig.update_xaxes(showgrid=False, showticklabels=False)
    fig.update_yaxes(showgrid=False, showticklabels=False)
    fig.update_layout(height=200, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return dcc.Graph(figure=fig, config={"displayModeBar": False})


def create_line_plot(metric, data, top_n=5, n_metric=None):
    """Create a line plot for a given metric over time."""
    filtered_data = data.filter(pl.col("Year").gt(2000))

    latest_year = filtered_data["Year"].max()

    # Determine which metric to use for sorting
    sort_metric = n_metric if n_metric else metric

    # Get top entities based on latest year values
    top_entities = (
        filtered_data.filter(pl.col("Year").eq(latest_year))
        .sort(pl.col(sort_metric), descending=True)
        .limit(top_n)
        .get_column("Entity")
        .to_list()
    )

    filtered_data = filtered_data.filter(pl.col("Entity").is_in(top_entities))

    fig = px.line(
        filtered_data.to_pandas(),
        x="Year",
        y=metric,
        color="Entity",
        title=f"Top {top_n} Countries by {metric}",
    )

    layout = {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"size": 12},
        "showlegend": True,
        "margin": {"l": 60, "r": 30, "t": 50, "b": 50},
        "height": None,
        "title": {
            "text": f"{get_title_text(metric)} Over Time",
            "y": 1,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 14},
        },
    }

    fig.update_layout(**layout)
    for axis in [fig.update_xaxes, fig.update_yaxes]:
        axis(**GRID_SETTINGS)

    return dcc.Graph(figure=fig, style={"height": "100%"}, config={"displayModeBar": False})


def create_bar_plot(metric, data, top_n=5, color=None):
    """Create a bar plot for a given metric.

    Args:
        metric (str): Column to plot
        data (pd.DataFrame): Data to plot
        top_n (int, optional): Number of top entries to show. Defaults to 5.
        color (str, optional): Column to use for color coding. Defaults to None.
    """
    if isinstance(data, pd.DataFrame):
        df = pl.from_pandas(data)
    elif isinstance(data, (list, dict)):
        df = pl.DataFrame(data)
    else:
        df = data
    # df =data
    if df.height == 0:
        return create_no_data_figure("No data available")

    # Get top N entries by metric value
    df = df.sort(metric, descending=True).limit(top_n)

    fig = px.bar(
        data_frame=df.to_pandas(),
        x="Entity",
        y=metric,
        color=color,
        labels={metric: get_title_text(metric)},
        title=f"Top {top_n} Countries by {get_title_text(metric)}",
    )

    layout = {
        **BASE_LAYOUT,
        "margin": {"l": 60, "r": 30, "t": 50, "b": 70},
        "height": None,
        "coloraxis_showscale": False,
        "title": {
            "text": f"Top {top_n} Countries by {get_title_text(metric)}",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 14},
        },
    }

    fig.update_layout(**layout)
    for axis in [fig.update_xaxes, fig.update_yaxes]:
        axis(**GRID_SETTINGS)

    return dcc.Graph(figure=fig, style={"height": "100%"}, config={"displayModeBar": False})


def create_chloropleth_map(filtered_data, metric, gender="Both"):
    """Create a choropleth map visualization from filtered data.

    Args:
        filtered_data (list): List of dictionaries containing filtered data
        metric (str): Selected metric name
        gender (str, optional): Selected gender. Defaults to "Both".

    Returns:
        plotly.graph_objects.Figure: The choropleth map figure
    """

    # Convert list of dicts to DataFrame
    df = pd.DataFrame(filtered_data)
    if df.empty:
        return create_no_data_figure("No data available for selected filters")

    # Get the appropriate column based on metric and gender
    metric_col = get_metric_column(gender, metric)
    if not metric_col:
        return create_no_data_figure("No data available for selected filters")

    df[metric_col] = pd.to_numeric(df[metric_col], errors="coerce")

    # Create figure
    # Calculate rounded max value for better scale
    data_max = df[metric_col].max()
    scale_max = round(data_max / 100) * 100  # Round to nearest hundred

    fig = go.Figure(
        data=go.Choropleth(
            locations=df["Entity"],
            locationmode="country names",
            z=df[metric_col],
            text=None,
            colorscale="RdYlBu_r",  # Changed to a more intuitive red-yellow-blue scale
            autocolorscale=False,
            zmin=0,  # Start from 0 for better context
            zmax=scale_max,  # Use rounded max
            marker_line_color="darkgray",
            marker_line_width=0.5,
            colorbar=dict(
                title=dict(text=get_title_text(metric), side="right", font=dict(size=12)),
                thickness=15,
                len=0.9,
                tickformat=".0f",
                outlinewidth=0,
            ),
        )
    )

    fig.update_layout(
        **COMMON_LAYOUT,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=None,
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type="equirectangular",
            showocean=True,
            oceancolor="rgba(0,0,0,0)",
            showland=True,
            landcolor="rgba(0,0,0,0)",
            showlakes=True,
            lakecolor="rgba(0,0,0,0)",
            showrivers=True,
            rivercolor="rgba(0,0,0,0)",
            showcountries=True,
            countrycolor="gray",
            countrywidth=0.5,
            showsubunits=True,
            subunitcolor="gray",
            subunitwidth=0.5,
        ),
    )

    return fig


def create_sankey_diagram(data, metric, gender):
    """Create a Sankey diagram showing flow between Region -> Income -> Metric Ranges."""
    df = pd.DataFrame(data)
    # df = data
    if df.empty:
        return create_no_data_figure("No data available")

    metric = get_metric_column(gender, metric)

    # df = data
    logger.debug(msg=df.columns.tolist())
    df[metric] = df[metric].astype(float)
    print(df.dtypes)

    if df.empty:
        return create_no_data_figure("No data available")

    try:
        labels = [f"{get_title_text(metric)} ({i}%)" for i in ["0-25", "25-50", "50-75", "75-100"]]
        df["metric_range"] = pd.qcut(df[metric], q=4, labels=labels, duplicates="drop")
    except ValueError:
        bins = [
            df[metric].min(),
            df[metric].mean() / 2,
            df[metric].mean(),
            df[metric].mean() * 1.5,
            df[metric].max(),
        ]
        labels = [
            f"{get_title_text(metric)} (Low)",
            f"{get_title_text(metric)} (Medium-Low)",
            f"{get_title_text(metric)} (Medium-High)",
            f"{get_title_text(metric)} (High)",
        ]
        df["metric_range"] = pd.cut(df[metric], bins=bins, labels=labels, duplicates="drop")

    regions = df["region"].unique().tolist()
    incomes = df["WB_Income"].unique().tolist()
    ranges = df["metric_range"].unique().tolist()
    nodes = regions + incomes + ranges
    sources, targets, values = [], [], []
    link_colors = []

    for region in regions:
        region_idx = nodes.index(region)
        region_data = df[df["region"] == region]
        for income in incomes:
            income_idx = nodes.index(income)
            income_data = region_data[region_data["WB_Income"] == income]
            if not income_data.empty:
                sources.append(region_idx)
                targets.append(income_idx)
                values.append(len(income_data))
                link_colors.append("rgba(31, 119, 180, 0.4)")  # Light blue

    for income in incomes:
        income_idx = nodes.index(income)
        income_data = df[df["WB_Income"] == income]
        for range_val in ranges:
            range_idx = nodes.index(range_val)
            range_data = income_data[income_data["metric_range"] == range_val]
            if not range_data.empty:
                sources.append(income_idx)
                targets.append(range_idx)
                values.append(len(range_data))
                link_colors.append("rgba(44, 160, 44, 0.4)")  # Light green

    node_colors = (
        ["#1f77b4"] * len(regions) + ["#2ca02c"] * len(incomes) + ["#ff7f0e"] * len(ranges)
    )

    fig = go.Figure(
        data=[
            go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=nodes,
                    color=node_colors,
                ),
                link=dict(source=sources, target=targets, value=values, color=link_colors),
            )
        ]
    )

    fig.update_layout(
        **COMMON_LAYOUT,
        height=400,
        title=dict(
            text=f"Distribution of {get_title_text(metric)} across Regions and Income Groups",
            y=0.95,
            x=0.5,
            xanchor="center",
            yanchor="top",
            font=dict(size=14),
        ),
    )

    return dcc.Graph(figure=fig, style={"height": "100%"}, config={"displayModeBar": False})


def create_histogram_plot(metric: str, data: pl.DataFrame, bins: int = 30) -> go.Figure:
    """Create a histogram plot showing the distribution of a metric.

    Args:
        metric (str): Column name to plot
        data (pl.DataFrame): Data to plot
        bins (int, optional): Number of bins for histogram. Defaults to 30.

    Returns:
        go.Figure: Plotly figure object
    """
    if len(data) == 0:
        return create_no_data_figure()

    title = get_title_text(metric)

    # Convert to pandas for plotly compatibility
    df = data.select([metric]).to_pandas()

    # Create histogram
    fig = px.histogram(df, x=metric, nbins=bins, title=title, labels={metric: title}, opacity=0.75)

    # Update layout
    fig.update_layout(
        **BASE_LAYOUT,
        **COMMON_LAYOUT,
        # showlegend=False,
        height=350,
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis=dict(title=title, **GRID_SETTINGS),
        yaxis=dict(title="Count", **GRID_SETTINGS),
    )

    # Add mean line
    mean_val = df[metric].mean()
    fig.add_vline(
        x=mean_val,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Mean: {format_value(mean_val, is_estimate=False, is_percent=False)}",
        annotation_position="top right",
    )

    return dcc.Graph(figure=fig, style={"height": "100%"}, config={"displayModeBar": False})


def create_corr_matrix(data: pl.DataFrame) -> dcc.Graph:
    """Create a correlation matrix of all numeric columns in the data."""

    corr_matrix = data.corr()
    fig = px.imshow(corr_matrix, text_auto=".2f", color_continuous_scale="blues")
    fig.update_layout(
        **BASE_LAYOUT,
        **COMMON_LAYOUT,
        title=dict(
            text="Correlation Matrix",
            y=0.95,
            x=0.5,
            xanchor="center",
            yanchor="top",
            font=dict(size=14),
        ),
    )
    return dcc.Graph(figure=fig, style={"height": "100%"}, config={"displayModeBar": False})
