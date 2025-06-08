# Code Reference

## Main Functions

### `interpolate_series(group_data, column_name)`
Interpolates missing values in time series data using cubic spline interpolation.
- Requires at least 2 data points
- Falls back to linear interpolation if cubic spline fails
- Returns original values for valid data points

### `impute_extremes(group_data, column_name)`
Handles missing values at the start/end of time series.
- Uses mode for categorical variables
- Applies exponential weighted means for numeric data
- Combines forward/backward fills for robust imputation

## Week 1: Data Processing Pipeline

1. **Initial Data Load**
   ```python
   merged_df = pd.read_excel("path/to/base/data.xlsx")
   for source_file in data_sources:
       temp_df = pd.read_excel/csv(source_file)
       merged_df = pd.merge(merged_df, temp_df, on=["Entity", "Code", "Year"], how="outer")
   ```

2. **Data Cleaning**
   ```python
   # Standardize country names
   ihme_data["location"] = ihme_data["location"].replace(name_mapping)
   
   # Process by entity
   for entity in result_df["Entity"].unique():
       entity_data = result_df[result_df["Entity"] == entity]
       for col in numeric_cols:
           result_df.loc[entity_data.index, col] = interpolate_series(entity_data, col)
   ```

3. **Final Processing**
   ```python
   # Merge population data
   result_df = result_df.merge(pop[["Entity", "Year", "Population"]], 
                              on=["Entity", "Year"], how="left")
   
   # Save processed data
   result_df.to_csv("../heart_disease_data.csv", index=False)
   ```

## Week 2: Initial Visualizations and Layout Design

1. **Core Visualizations**
   ```python
   import plotly.express as px

   # Choropleth map
   fig_choropleth = px.choropleth(
       merged_df,
       locations="Code",
       color="Heart Disease Prevalence",
       hover_name="Entity",
       title="World Heart Disease Prevalence"
   )

   # Time series plot
   fig_timeseries = px.line(
       merged_df,
       x="Year",
       y="Mortality Rate",
       color="Region",
       title="Time Series of Mortality Rates"
   )
   ```

## Week 3: Interactive Features and Advanced Visualizations

1. **Interactive Features**
   ```python
   from dash import Input, Output

   #  Year Slider
   def update_year_on_interval(n_intervals, current_year, min_year, max_year):
    """Funtion to update the year slider"""
    if current_year is None:
        return min_year

    next_year = current_year + 1 if current_year < max_year else min_year
    return next_year
   ```
   ```python
      # sidebar toggle and dropdown for selectors
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

      #dropdown
    """Update country dropdown options based on selected region."""
    if not data or not selected_region:
        return []

    df = pd.DataFrame(data)
    countries = df[df["region"] == selected_region]["Entity"].unique()
    return [{"label": country, "value": country} for country in sorted(countries)]
 
   ```


2. **Advanced Visualizations**
   ```python
   # Scatter plot example
   fig_scatter = px.scatter(
       merged_df,
       x="GDP",
       y="Heart Disease Prevalence",
       color="Region",
       size="Population",
       title="Heart Disease Prevalence vs GDP"
   )

   # Sankey diagram example
   from plotly.graph_objects import Sankey

   fig_sankey = Sankey(
       node=dict(
           pad=15,
           thickness=20,
           label=["Risk Factor A", "Risk Factor B", "Outcome A", "Outcome B"]
       ),
       link=dict(
           source=[0, 1, 0, 1],
           target=[2, 2, 3, 3],
           value=[10, 20, 30, 40]
       )
   ).to_plotly_json()
   ```