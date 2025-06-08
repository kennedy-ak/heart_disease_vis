# Heart Disease Data Visualization Dashboard - Technical Documentation

## Project Overview
An interactive dashboard built with Dash and Plotly for visualizing global heart disease data trends and patterns.

## Project Structure

```
heart-disease/
├── application.py          # Main application entry point
├── components/

│   ├── common/            # Shared components
│   │   ├── filter_slider.py
│   │   ├── plots.py
│   │   └── year_slider.py
|   ├── data
|   |   ├── data.py        # side bar selector
│   ├── tabs/              # Tab-specific components
│   │   ├── introduction.py
│   │   ├── world_map.py
│   │   ├── geo_eco.py
│   │   ├── healthcare.py
│   │   └── trends.py
│   └── sidebar.py         # Sidebar component
├── documentation/         # Project documentation
└── .ebextensions/         # AWS Elastic Beanstalk configuration
```

## Technical Implementation

### Core Components

#### 1. Sidebar (`components/sidebar.py`)
- Collapsible design with smooth transitions
- Toggle button for space efficiency
- Responsive width adjustment (250px expanded, 60px collapsed)
- Dynamic state management using Dash callbacks
- Custom styling for smooth animations

#### 2. Year Slider (`components/common/year_slider.py`)
- Range: 1950-2023
- Animation capabilities with play/pause
- 1-second interval for time series
- Callback structure:
  - `toggle_animation`: Controls play/pause state
  - `update_year_on_interval`: Handles year increments

#### 3. Filter by Top Slider (components/common/top_slider.py)

- Dynamic range based on data
- Configurable top N filtering
- Smooth sliding interaction:
  - Handles real-time data reduction without full recomputation
  - Supports flexible top N selection (e.g., top 10, top 50 entities)

#### 4. Choropleth Map (`components/tabs/world_map.py`)
- Clean interface without legends/menus
- Interactive zoom and pan
- Dynamic year-based updates
- Performance optimizations:
  - Minimal redraws
  - Efficient state management
  - Optimized callback structure

#### 5. Plot Layout (`components/common/plots.py`)
- Viewport-based sizing (37vh per plot)
- Minimal padding for maximum space utilization
- Two-row, two-column grid layout
- Responsive design using Bootstrap grid

### Application Architecture

#### Main Application (`application.py`)
- Flask server integration
- Dash initialization with:
  - Bootstrap theme
  - Font Awesome icons
  - Callback exception handling
- Tab-based navigation system
- Global state management

#### Tab Components
1. **World Map Tab**
   - Choropleth visualization
   - Year slider integration
   - Dynamic data updates

2. **GEO-ECO Tab**
   - Economic indicators
   - Regional analysis
   - Income group comparisons

3. **Healthcare Tab**
   - Healthcare metrics
   - Facility distribution
   - Accessibility analysis

4. **Trends Tab**
   - Multi-plot layout
   - Temporal analysis
   - Comparative statistics

### Callback Structure

#### Navigation Callbacks
```python
@app.callback(
    [Output(f"tab-{i}-link", "active") for i in range(1, 5)],
    [Input(f"tab-{i}-link", "n_clicks") for i in range(1, 5)]
)
```
- Manages tab activation states
- Handles navigation between views
- Updates URL without page refresh

#### Animation Callbacks
```python
@callback(
    Output("animation-interval", "disabled"),
    Output("play-button", "children"),
    Input("play-button", "n_clicks"),
    State("animation-interval", "disabled"),
)
```
- Controls animation state
- Updates button appearance
- Manages interval timing

### Styling Approach
- Bootstrap-based responsive grid
- Custom CSS for transitions
- Viewport-based sizing
- Minimal padding strategy

### Performance Optimizations
1. **Callback Efficiency**
   - Prevent unnecessary updates
   - Optimize state management
   - Use client-side callbacks where appropriate

2. **Layout Optimization**
   - Minimize DOM updates
   - Efficient component rendering
   - Responsive design patterns

3. **Data Management**
   - Efficient data loading
   - Caching strategies
   - Optimized state updates

## Deployment Configuration

### AWS Elastic Beanstalk Setup
- Flask server configuration
- NGINX proxy settings
- Environment configurations
- Static file handling

### Environment Variables
- PORT configuration
- Debug settings
- AWS specific configurations

## Development Guidelines

### Adding New Features
1. Create component in appropriate directory
2. Implement necessary callbacks
3. Update main application
4. Add documentation

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings for complex functions
- Maintain consistent formatting

### Testing
- Test callbacks independently
- Verify responsive design
- Check performance impact
- Cross-browser testing

