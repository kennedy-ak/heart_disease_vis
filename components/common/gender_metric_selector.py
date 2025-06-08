"""Module for selecting gender-specific metrics and columns."""


def get_metric_column(gender: str, metric: str) -> str:
    """Get the appropriate column name based on gender and metric.

    Args:
        gender (str): Gender selection ('Female', 'Male', or 'Both')
        metric (str): Selected metric name

    Returns:
        str: Column name for the selected metric and gender
    """
    gender_suffix = "female" if gender == "Female" else "male" if gender == "Male" else "both"

    metric_mapping = {
        "Prevalence Percent": f"valprevpercent{gender_suffix}",
        "Prevalence Rate": f"valprevrate{gender_suffix}",
        "Prevalence": f"valprevnumber{gender_suffix}",
        "Death Percent": f"valdeathspercent{gender_suffix}",
        "Death Rate": f"valdeathsrate{gender_suffix}",
        "Death": f"valdeathsnumber{gender_suffix}",
    }

    return metric_mapping.get(metric)
