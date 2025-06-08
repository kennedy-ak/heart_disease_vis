#! usr/bin/env python3.12
"""
Data cleaning and merging script for cardiovascular disease datasets.
Combines and standardizes data from multiple sources, handles missing values,
and prepares a comprehensive dataset for analysis.
"""

import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline

# Data source paths
ourworldindata = [
    "./cardiovascular-disease-death-rate-age-group-who-mdb/cardiovascular-disease-death-rate-age-group-who-mdb.csv",
    "./cardiovascular-disease-death-rate-males-vs-females/cardiovascular-disease-death-rate-males-vs-females.csv",
    "./death-rate-from-cardiovascular-disease-age-standardized-ghe/death-rate-from-cardiovascular-disease-age-standardized-ghe.csv",
    "./deaths-from-cardiovascular-disease-ghe/deaths-from-cardiovascular-disease-ghe.csv",
    "./share-of-deaths-from-cardiovascular-diseases-men-women/share-of-deaths-from-cardiovascular-diseases-men-women.csv",
    "./cardiovascular-disease-death-rate-crude-versus-age-standardized - cardiovascular-disease-death-rate-crude-versus-age-standardized.csv",
    "./deaths-from-cardiovascular-diseases-by-region.csv",
    "./CVD_Death_Rate (Age vs Raw).csv",
    "./death-rate-from-ischaemic-heart-disease-who-ghe-age-standardized/death-rate-from-ischaemic-heart-disease-who-ghe-age-standardized.csv",
    "./death-rate-from-rheumatic-heart-disease-who-ghe-age-standardized/death-rate-from-rheumatic-heart-disease-who-ghe-age-standardized.csv",
    "./obesity-prevalence-adults-who-gho/obesity-prevalence-adults-who-gho.csv",
    "./pacemaker-implantations-per-million-people/pacemaker-implantations-per-million-people.csv",
    "./share-of-deaths-from-major-causes/share-of-deaths-from-major-causes.csv",
    "./utilization-of-statins/utilization-of-statins.csv",
    "./women-high-blood-pressure/women-high-blood-pressure.csv",
    "./death-rate-from-hypertensive-heart-disease-who-ghe-age-standardized/death-rate-from-hypertensive-heart-disease-who-ghe-age-standardized.csv",
]

# Load base dataset
merged_df = pd.read_excel(
    "./cardiovascular-death-rate-vs-gdp-per-capita/Cardiovascular Death Rate vs GDP per Capita.xlsx"
)

# Merge additional datasets
for source_file in ourworldindata:
    temp_df = pd.read_excel(source_file) if "xlsx" in source_file else pd.read_csv(source_file)
    merged_df = pd.merge(merged_df, temp_df, on=["Entity", "Code", "Year"], how="outer")

# Load IHME dataset
ihme_data = pd.read_csv("./IHME-GBD_2021_DATA-7438e2ae-1.csv")

# Country name mapping
name_mapping = {
    "American Samoa": "American Samoa",
    "Antigua and Barbuda": "Antigua and Barbuda",
    "Arab Republic of Egypt": "Egypt",
    "Argentine Republic": "Argentina",
    "Barbados": "Barbados",
    "Belize": "Belize",
    "Bermuda": "Bermuda",
    "Bolivarian Republic of Venezuela": "Venezuela",
    "Bosnia and Herzegovina": "Bosnia and Herzegovina",
    "Brunei Darussalam": "Brunei",
    "Burkina Faso": "Burkina Faso",
    "Central African Republic": "Central African Republic",
    "Commonwealth of Dominica": "Dominica",
    "Commonwealth of the Bahamas": "Bahamas",
    "Cook Islands": "Cook Islands",
    "Czech Republic": "Czechia",
    "Democratic People's Republic of Korea": "North Korea",
    "Democratic Republic of Sao Tome and Principe": "Sao Tome and Principe",
    "Democratic Republic of Timor-Leste": "Timor-Leste",
    "Democratic Republic of the Congo": "Democratic Republic of the Congo",
    "Democratic Socialist Republic of Sri Lanka": "Sri Lanka",
    "Dominican Republic": "Dominican Republic",
    "Eastern Republic of Uruguay": "Uruguay",
    "Federal Democratic Republic of Ethiopia": "Ethiopia",
    "Federal Democratic Republic of Nepal": "Nepal",
    "Federal Republic of Germany": "Germany",
    "Federal Republic of Nigeria": "Nigeria",
    "Federal Republic of Somalia": "Somalia",
    "Federated States of Micronesia": "Micronesia (Federated States of)",
    "Federative Republic of Brazil": "Brazil",
    "French Republic": "France",
    "Gabonese Republic": "Gabon",
    "Georgia": "Georgia",
    "Grand Duchy of Luxembourg": "Luxembourg",
    "Greenland": "Greenland",
    "Grenada": "Grenada",
    "Guam": "Guam",
    "Hashemite Kingdom of Jordan": "Jordan",
    "Hellenic Republic": "Greece",
    "Hungary": "Hungary",
    "Independent State of Papua New Guinea": "Papua New Guinea",
    "Independent State of Samoa": "Samoa",
    "Ireland": "Ireland",
    "Islamic Republic of Afghanistan": "Afghanistan",
    "Islamic Republic of Iran": "Iran",
    "Islamic Republic of Mauritania": "Mauritania",
    "Islamic Republic of Pakistan": "Pakistan",
    "Jamaica": "Jamaica",
    "Japan": "Japan",
    "Kingdom of Bahrain": "Bahrain",
    "Kingdom of Belgium": "Belgium",
    "Kingdom of Bhutan": "Bhutan",
    "Kingdom of Cambodia": "Cambodia",
    "Kingdom of Denmark": "Denmark",
    "Kingdom of Eswatini": "Eswatini",
    "Kingdom of Lesotho": "Lesotho",
    "Kingdom of Morocco": "Morocco",
    "Kingdom of Norway": "Norway",
    "Kingdom of Saudi Arabia": "Saudi Arabia",
    "Kingdom of Spain": "Spain",
    "Kingdom of Sweden": "Sweden",
    "Kingdom of Thailand": "Thailand",
    "Kingdom of Tonga": "Tonga",
    "Kingdom of the Netherlands": "Netherlands",
    "Kyrgyz Republic": "Kyrgyzstan",
    "Lao People's Democratic Republic": "Laos",
    "Lebanese Republic": "Lebanon",
    "Malaysia": "Malaysia",
    "Mongolia": "Mongolia",
    "Montenegro": "Montenegro",
    "New Zealand": "New Zealand",
    "North Macedonia": "North Macedonia",
    "Northern Mariana Islands": "Northern Mariana Islands",
    "Palestine": "Palestine",
    "People's Democratic Republic of Algeria": "Algeria",
    "People's Republic of Bangladesh": "Bangladesh",
    "People's Republic of China": "China",
    "Plurinational State of Bolivia": "Bolivia",
    "Portuguese Republic": "Portugal",
    "Principality of Andorra": "Andorra",
    "Principality of Monaco": "Monaco",
    "Puerto Rico": "Puerto Rico",
    "Republic of Albania": "Albania",
    "Republic of Angola": "Angola",
    "Republic of Armenia": "Armenia",
    "Republic of Austria": "Austria",
    "Republic of Azerbaijan": "Azerbaijan",
    "Republic of Belarus": "Belarus",
    "Republic of Benin": "Benin",
    "Republic of Botswana": "Botswana",
    "Republic of Bulgaria": "Bulgaria",
    "Republic of Burundi": "Burundi",
    "Republic of Cabo Verde": "Cabo Verde",
    "Republic of Cameroon": "Cameroon",
    "Republic of Chad": "Chad",
    "Republic of Chile": "Chile",
    "Republic of Colombia": "Colombia",
    "Republic of Costa Rica": "Costa Rica",
    "Republic of Croatia": "Croatia",
    "Republic of Cuba": "Cuba",
    "Republic of Cyprus": "Cyprus",
    "Republic of Djibouti": "Djibouti",
    "Republic of Ecuador": "Ecuador",
    "Republic of El Salvador": "El Salvador",
    "Republic of Equatorial Guinea": "Equatorial Guinea",
    "Republic of Estonia": "Estonia",
    "Republic of Fiji": "Fiji",
    "Republic of Finland": "Finland",
    "Republic of Ghana": "Ghana",
    "Republic of Guatemala": "Guatemala",
    "Republic of Guinea": "Guinea",
    "Republic of Guinea-Bissau": "Guinea-Bissau",
    "Republic of Guyana": "Guyana",
    "Republic of Haiti": "Haiti",
    "Republic of Honduras": "Honduras",
    "Republic of Iceland": "Iceland",
    "Republic of India": "India",
    "Republic of Indonesia": "Indonesia",
    "Republic of Iraq": "Iraq",
    "Republic of Kazakhstan": "Kazakhstan",
    "Republic of Kenya": "Kenya",
    "Republic of Kiribati": "Kiribati",
    "Republic of Korea": "South Korea",
    "Republic of Latvia": "Latvia",
    "Republic of Liberia": "Liberia",
    "Republic of Lithuania": "Lithuania",
    "Republic of Madagascar": "Madagascar",
    "Republic of Malawi": "Malawi",
    "Republic of Maldives": "Maldives",
    "Republic of Mali": "Mali",
    "Republic of Malta": "Malta",
    "Republic of Mauritius": "Mauritius",
    "Republic of Moldova": "Moldova",
    "Republic of Mozambique": "Mozambique",
    "Republic of Namibia": "Namibia",
    "Republic of Nauru": "Nauru",
    "Republic of Nicaragua": "Nicaragua",
    "Republic of Niger": "Niger",
    "Republic of Panama": "Panama",
    "Republic of Paraguay": "Paraguay",
    "Republic of Peru": "Peru",
    "Republic of Poland": "Poland",
    "Republic of Rwanda": "Rwanda",
    "Republic of San Marino": "San Marino",
    "Republic of Senegal": "Senegal",
    "Republic of Serbia": "Serbia",
    "Republic of Seychelles": "Seychelles",
    "Republic of Sierra Leone": "Sierra Leone",
    "Republic of Singapore": "Singapore",
    "Republic of Slovenia": "Slovenia",
    "Republic of South Africa": "South Africa",
    "Republic of South Sudan": "South Sudan",
    "Republic of Sudan": "Sudan",
    "Republic of Suriname": "Suriname",
    "Republic of Tajikistan": "Tajikistan",
    "Republic of the Gambia": "Gambia",
    "Republic of the Philippines": "Philippines",
    "Republic of the Union of Myanmar": "Myanmar",
    "Republic of Trinidad and Tobago": "Trinidad and Tobago",
    "Republic of Tunisia": "Tunisia",
    "Republic of Turkey": "Turkey",
    "Republic of Uganda": "Uganda",
    "Republic of Uzbekistan": "Uzbekistan",
    "Republic of Vanuatu": "Vanuatu",
    "Republic of Yemen": "Yemen",
    "Republic of Zambia": "Zambia",
    "Republic of Zimbabwe": "Zimbabwe",
    "Republic of Italy": "Italy",
    "Romania": "Romania",
    "Russian Federation": "Russia",
    "Saint Kitts and Nevis": "Saint Kitts and Nevis",
    "Saint Lucia": "Saint Lucia",
    "Saint Vincent and the Grenadines": "Saint Vincent and the Grenadines",
    "Slovak Republic": "Slovakia",
    "Socialist Republic of Viet Nam": "Vietnam",
    "Solomon Islands": "Solomon Islands",
    "State of Eritrea": "Eritrea",
    "State of Israel": "Israel",
    "State of Kuwait": "Kuwait",
    "State of Libya": "Libya",
    "State of Qatar": "Qatar",
    "Sultanate of Oman": "Oman",
    "Swiss Confederation": "Switzerland",
    "Syrian Arab Republic": "Syria",
    "Taiwan (Province of China)": "Taiwan",
    "Togolese Republic": "Togo",
    "Tokelau": "Tokelau",
    "Turkmenistan": "Turkmenistan",
    "Tuvalu": "Tuvalu",
    "Ukraine": "Ukraine",
    "Union of the Comoros": "Comoros",
    "United Arab Emirates": "United Arab Emirates",
    "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
    "United Mexican States": "Mexico",
    "United Republic of Tanzania": "Tanzania",
    "United States Virgin Islands": "United States Virgin Islands",
    "United States of America": "United States",
    "Venezuela (Bolivarian Republic of)": "Venezuela",
    "Micronesia (Federated States of)": "Micronesia",
    "Republic of Niue": "Niue",
    "occupied Palestinian territory, including east Jerusalem": "Palestine",
}

ihme_data["location"] = ihme_data["location"].replace(name_mapping)

# Splitting the deaths and prevalence data
deaths_df = ihme_data[ihme_data["measure"] == "Deaths"].copy()
prev_df = ihme_data[ihme_data["measure"] == "Prevalence"].copy()

# Efficient merge and cleanup operations
wide_ihme = pd.merge(
    deaths_df,
    prev_df,
    on=["location", "sex", "age", "year", "metric"],
    how="outer",
    suffixes=("_deaths", "_prev"),
)
columns_to_drop = ["measure_deaths", "measure_prev", "cause_deaths", "cause_prev", "age"]
wide_ihme.drop(columns=columns_to_drop, inplace=True)

# Rename columns for clarity
wide_ihme.rename(
    columns={
        "sex": "gender",
        "location": "Entity",
        "val_deaths": "deaths",
        "val_prev": "prevalence",
        "year": "Year",
    },
    inplace=True,
)

# Merge with main dataset
primary_df = wide_ihme.merge(merged_df, on=["Entity", "Year"], how="outer")

# Drop unnecessary columns in a single call
unnecessary_columns = [
    "Total deaths from cardiovascular diseases among both sexes_x",
    "Share of total deaths in males in those aged all ages that are from cardiovascular diseases",
    "Share of total deaths in females in those aged all ages that are from cardiovascular diseases",
    "Share of total deaths in both sexes in those aged all ages that are from cardiovascular diseases",
    "Deaths from cardiovascular diseases per 100,000 people in, both sexes aged all ages",
]
primary_df.drop(columns=unnecessary_columns, inplace=True)

# Load additional datasets with streamlined renaming and merging
add_datasets = [
    (
        "./Cleaned-Secondary-Data/Global_CVD_Deaths.csv",
        {"Gender": "gender", "Total_Number_of_Deaths": "Total_Number_of_Deaths"},
    ),
    (
        "./Cleaned-Secondary-Data/Global_WHO_data.csv",
        {"Country": "Entity", "WHO_Region": "Region", "Gender": "gender"},
    ),
    ("./Cleaned-Secondary-Data/Our-World-Cleaned/CT_Units.csv", {"Country": "Entity"}),
    ("./Cleaned-Secondary-Data/Our-World-Cleaned/Ischaemic_Death_Rate.csv", {"Country": "Entity"}),
    ("./Cleaned-Secondary-Data/Our-World-Cleaned/Obesity_Rate.csv", {"Country": "Entity"}),
    (
        "./Cleaned-Secondary-Data/Our-World-Cleaned/Pacemaker_Implantations_per_1M.csv",
        {"Country": "Entity"},
    ),
    ("./Cleaned-Secondary-Data/Our-World-Cleaned/Rheumatic_Death_Rate.csv", {"Country": "Entity"}),
    ("./Cleaned-Secondary-Data/Our-World-Cleaned/satins_availablity.csv", {"Country": "Entity"}),
    ("./Cleaned-Secondary-Data/Our-World-Cleaned/Statin_use_(1000).csv", {"Country": "Entity"}),
]

for file_path, rename_dict in add_datasets:
    add_df = pd.read_csv(file_path).rename(columns=rename_dict)
    primary_df = primary_df.merge(
        add_df, on=["Entity", "Year", "gender"], how="outer", suffixes=("", "_global_deaths")
    )

# Select relevant columns
keep_cols = [
    "Entity",
    "Code",
    "Year",
    "gender",
    "metric",
    "deaths",
    "prevalence",
    "GDP per capita, PPP (constant 2017 international $)",
    "WB_Income",
    "Population",
    "World regions according to OWID",
    "Indicator Name",
    "Numeric_Females",
    "Numeric_Males",
    "Numeric_Total",
    "age_standardized_death_rate",
    "CT_Units",
    "Ischaemic_Death_Rate (100,000)",
    "Obesity_Rate (%)",
    "Pacemaker_Implantations_per_1M",
    "Rheumatic_Death_Rate (100,000)",
    "Availability_of_Statins",
    "Statin_use_(1000)",
    "Age-standardized death rate from hypertensive heart disease among both sexes",
    "Age-standardized death rate from ischaemic heart disease among both sexes",
    "Age-standardized death rate from rheumatic heart disease among both sexes",
    "Share of total deaths in both sexes in those aged all ages that are from cardiovascular diseases",
]

final_df = primary_df[keep_cols]

# Pivot table for deaths and prevalence
pivot_df = final_df.pivot_table(
    index=["Entity", "Year", "gender"],
    columns=["metric"],
    values=["deaths", "prevalence"],
    aggfunc="first",
).reset_index()

# Clean up column names
pivot_df.columns = [
    "".join(col).strip() if isinstance(col, tuple) else col for col in pivot_df.columns
]

# Rename to more intuitive names
pivot_df.rename(
    columns={
        "deaths_Number": "deaths_value",
        "deaths_Percent": "deaths_percent",
        "deaths_Rate": "deaths_rate",
        "prevalence_Number": "prevalence_value",
        "prevalence_Percent": "prevalence_percent",
        "prevalence_Rate": "prevalence_rate",
    },
    inplace=True,
)

# Merge with original dataframe
final_df = final_df.merge(pivot_df, on=["Entity", "Year", "gender"], how="left")

# Drop original deaths and prevalence columns and metric column
final_df.drop(columns=["deaths", "prevalence", "metric"], inplace=True)

# Pivot table for gender
gender_pivot = final_df.pivot_table(
    index=["Entity", "Year"],  # Remove gender from index since we're pivoting it
    columns=["gender"],
    values=[
        "deathsNumber",
        "deathsPercent",
        "deathsRate",
        "prevalenceNumber",
        "prevalencePercent",
        "prevalenceRate",
    ],
    aggfunc="first",
).reset_index()

# Clean up column names
gender_pivot.columns = [
    ("".join(str(col) for col in col_tuple).strip() if isinstance(col_tuple, tuple) else col_tuple)
    for col_tuple in gender_pivot.columns
]

# Merge with original dataframe
final_df = final_df.merge(gender_pivot, on=["Entity", "Year"], how="left")

# Drop original columns, gender column, and unnamed index
cols_to_drop = [
    "Unnamed: 0",
    "gender",
    "deathsNumber",
    "deathsPercent",
    "deathsRate",
    "prevalenceNumber",
    "prevalencePercent",
    "prevalenceRate",
]

final_df = final_df.drop(columns=cols_to_drop)

final_df = final_df.drop_duplicates()

# Pivot table for indicator name
indicator_pivot = final_df.pivot_table(
    index=["Entity", "Year"],
    columns=["Indicator Name"],
    values=["Numeric_Females", "Numeric_Males", "Numeric_Total"],
    aggfunc="first",
).reset_index()

# Clean up column names - replace spaces and special characters
indicator_pivot.columns = [
    (
        "".join(
            str(col)
            .replace(" ", "_")
            .replace("-", "_")
            .replace(",", "")
            .replace("(", "")
            .replace(")", "")
            for col in col_tuple
        ).strip()
        if isinstance(col_tuple, tuple)
        else col_tuple
    )
    for col_tuple in indicator_pivot.columns
]

# Merge with original dataframe
final_df = final_df.merge(indicator_pivot, on=["Entity", "Year"], how="left")

# Drop original columns
final_df.drop(
    columns=["Indicator Name", "Numeric_Females", "Numeric_Males", "Numeric_Total"], inplace=True
)
final_df.dropna(axis=1, how="all", inplace=True)

# Set first 7 columns as index
final_df.set_index(final_df.columns[:7].tolist(), inplace=True)

# Drop rows where all non-index values are NaN
final_df.dropna(how="all", inplace=True)

# Reset the index to get the columns back
final_df.reset_index(inplace=True)


def interpolate_series(group_data, column_name):
    """
    Interpolate missing values in a time series using cubic spline.
    Returns interpolated values for the given group and column.
    """
    years = group_data["Year"].values
    values = group_data[column_name].values
    mask = ~np.isnan(values)

    if np.sum(mask) < 2:
        return values

    try:
        spline = CubicSpline(years[mask], values[mask], extrapolate=False)
        return np.where(mask, values, spline(years))
    except ValueError:
        return values


def impute_extremes(group_data, column_name):
    if group_data[column_name].isna().sum() == 0:
        return group_data[column_name]

    if column_name in categorical_cols:
        fill_value = (
            group_data[column_name].mode().iloc[0]
            if not group_data[column_name].mode().empty
            else None
        )
        if fill_value is not None:
            return group_data[column_name].fillna(value=fill_value)
        return group_data[column_name]

    sorted_data = group_data.sort_values("Year")[column_name]
    fwd = sorted_data.fillna(method="ffill")
    bwd = sorted_data.fillna(method="bfill")
    fwd_ewm = fwd.ewm(span=3, min_periods=1, adjust=False).mean()
    bwd_ewm = bwd[::-1].ewm(span=3, min_periods=1, adjust=False).mean()[::-1]
    filled = pd.concat([fwd_ewm, bwd_ewm], axis=1).mean(axis=1)
    return filled[group_data.index]


# Process data
result_df = final_df.copy()

# Process each entity separately
for entity in result_df["Entity"].unique():
    entity_data = result_df[result_df["Entity"] == entity].sort_values("Year")

    # Interpolate numeric columns
    for col in [
        "deaths_total",
        "deaths_female",
        "deaths_male",
        "deaths_pct_total",
        "deaths_pct_female",
        "deaths_pct_male",
        "death_rate_total",
        "death_rate_female",
        "death_rate_male",
        "prev_total",
        "prev_female",
        "prev_male",
        "prev_pct_total",
        "prev_pct_female",
        "prev_pct_male",
        "prev_rate_total",
        "prev_rate_female",
        "prev_rate_male",
        "obesity_rate%",
        "ct_units",
        "ischemic_death_rate",
        "pacemaker_per_1m",
        "rheumatic_death_rate",
        "statin_use_k",
        "hypertensive_death_rate",
        "ischemic_death_rate_std",
        "rheumatic_death_rate_std",
        "cvd_death_share",
        "f_cvd_death_rate_std",
        "f_hypertension_controlled",
        "f_hypertension_diagnosed",
        "f_hypertension",
        "f_cvd_deaths_under_70_pct",
        "f_high_bp",
        "f_hypertension_treated",
        "m_cvd_death_rate_std",
        "m_hypertension_controlled",
        "m_hypertension_diagnosed",
        "m_hypertension",
        "m_cvd_deaths_under_70_pct",
        "m_high_bp",
        "m_hypertension_treated",
        "t_cvd_death_rate_std",
        "t_hypertension_controlled",
        "t_hypertension_diagnosed",
        "t_hypertension",
        "t_cvd_deaths_under_70_pct",
        "t_high_bp",
        "t_hypertension_treated",
    ]:
        if col in entity_data.columns:
            result_df.loc[entity_data.index, col] = interpolate_series(entity_data, col)
            result_df.loc[entity_data.index, col] = impute_extremes(entity_data, col)

# Print statistics about remaining missing values
print("\nRemaining missing values after extreme imputation:\n")
missing_stats = (
    result_df[
        [
            "deaths_total",
            "deaths_female",
            "deaths_male",
            "deaths_pct_total",
            "deaths_pct_female",
            "deaths_pct_male",
            "death_rate_total",
            "death_rate_female",
            "death_rate_male",
            "prev_total",
            "prev_female",
            "prev_male",
            "prev_pct_total",
            "prev_pct_female",
            "prev_pct_male",
            "prev_rate_total",
            "prev_rate_female",
            "prev_rate_male",
            "obesity_rate%",
            "ct_units",
            "ischemic_death_rate",
            "pacemaker_per_1m",
            "rheumatic_death_rate",
            "statin_use_k",
            "hypertensive_death_rate",
            "ischemic_death_rate_std",
            "rheumatic_death_rate_std",
            "cvd_death_share",
            "f_cvd_death_rate_std",
            "f_hypertension_controlled",
            "f_hypertension_diagnosed",
            "f_hypertension",
            "f_cvd_deaths_under_70_pct",
            "f_high_bp",
            "f_hypertension_treated",
            "m_cvd_death_rate_std",
            "m_hypertension_controlled",
            "m_hypertension_diagnosed",
            "m_hypertension",
            "m_cvd_deaths_under_70_pct",
            "m_high_bp",
            "m_hypertension_treated",
            "t_cvd_death_rate_std",
            "t_hypertension_controlled",
            "t_hypertension_diagnosed",
            "t_hypertension",
            "t_cvd_deaths_under_70_pct",
            "t_high_bp",
            "t_hypertension_treated",
        ]
    ]
    .isnull()
    .sum()
)
print(missing_stats[missing_stats > 0].sort_values(ascending=False))

# Load population data
pop = pd.read_excel(
    "/Users/dna/Library/CloudStorage/GoogleDrive-dna@reallygreattech.com/Shared drives/Heart Disease Data/Primary Data/Derek/cardiovascular-death-rate-vs-gdp-per-capita/Cardiovascular Death Rate vs GDP per Capita.xlsx"
)

# Rename columns in pop dataframe for consistency
pop = pop.rename(columns={"Country": "Entity", "Population (historical)": "Population"})

# Merge population data with interpolated dataframe
result_df = result_df.merge(
    pop[["Entity", "Year", "Population"]], on=["Entity", "Year"], how="left"
)

# Update the Population column, keeping the original values where no match is found
result_df["Population"] = result_df["Population_y"].fillna(result_df["Population_x"])

# Drop the temporary columns
result_df = result_df.drop(["Population_x", "Population_y"], axis=1)

# Final column renaming for better programmatic handling
column_mapping = {
    "Age-standardized death rate from cardiovascular diseases among both sexes": "cvd_death_std",
    "GDP per capita, PPP (constant 2017 international $)": "gdp_pc",
    "Population (historical)": "pop_hist",
    "World Bank's income classification": "wb_income",
    "World regions according to OWID": "region",
    "age_standardized_death_rate": "death_std",
    "CT_Units": "ct_units",
    "Ischaemic_Death_Rate (100,000)": "ischemic_rate",
    "Obesity_Rate (%)": "obesity%",
    "Pacemaker_Implantations_per_1M": "pacemaker_1m",
    "Rheumatic_Death_Rate (100,000)": "rheumatic_rate",
    "Availability_of_Statins": "statin_avail",
    "Statin_use_(1000)": "statin_use_k",
    "Age-standardized death rate from hypertensive heart disease among both sexes": "htn_death_std",
    "Age-standardized death rate from ischaemic heart disease among both sexes": "ischemic_std",
    "Age-standardized death rate from rheumatic heart disease among both sexes": "rheumatic_std",
    "Share of total deaths in both sexes in those aged all ages that are from cardiovascular diseases": "cvd_share",
    "Numeric_FemalesCVD_age_standardized_death_rate": "f_cvd_std",
    "Numeric_FemalesControlled_hypertension_adults_aged_30–79_with_hypertension": "f_htn_ctrl",
    "Numeric_FemalesDiagnosed_hypertension_adults_aged_30–79_with_hypertension": "f_htn_diag",
    "Numeric_FemalesHypertension_adults_aged_30–79": "f_htn",
    "Numeric_FemalesPercentage_of_CVD_deaths_occurring_under_70_years": "f_cvd_u70%",
    "Numeric_FemalesRaised_blood_pressure_adults_aged_30–79_years": "f_high_bp",
    "Numeric_FemalesTreated_hypertension_adults_aged_30–79_with_hypertension": "f_htn_rx",
    "Numeric_MalesCVD_age_standardized_death_rate": "m_cvd_std",
    "Numeric_MalesControlled_hypertension_adults_aged_30–79_with_hypertension": "m_htn_ctrl",
    "Numeric_MalesDiagnosed_hypertension_adults_aged_30–79_with_hypertension": "m_htn_diag",
    "Numeric_MalesHypertension_adults_aged_30–79": "m_htn",
    "Numeric_MalesPercentage_of_CVD_deaths_occurring_under_70_years": "m_cvd_u70%",
    "Numeric_MalesRaised_blood_pressure_adults_aged_30–79_years": "m_high_bp",
    "Numeric_MalesTreated_hypertension_adults_aged_30–79_with_hypertension": "m_htn_rx",
    "Numeric_TotalCVD_age_standardized_death_rate": "t_cvd_std",
    "Numeric_TotalControlled_hypertension_adults_aged_30–79_with_hypertension": "t_htn_ctrl",
    "Numeric_TotalDiagnosed_hypertension_adults_aged_30–79_with_hypertension": "t_htn_diag",
    "Numeric_TotalHypertension_adults_aged_30–79": "t_htn",
    "Numeric_TotalPercentage_of_CVD_deaths_occurring_under_70_years": "t_cvd_u70%",
    "Numeric_TotalRaised_blood_pressure_adults_aged_30–79_years": "t_high_bp",
    "Numeric_TotalTreated_hypertension_adults_aged_30–79_with_hypertension": "t_htn_rx",
    # Keep existing death/prevalence mappings
    "deathsNumberBoth": "deaths",
    "deathsNumberFemale": "f_deaths",
    "deathsNumberMale": "m_deaths",
    "deathsPercentBoth": "deaths%",
    "deathsPercentFemale": "f_deaths%",
    "deathsPercentMale": "m_deaths%",
    "deathsRateBoth": "death_rate",
    "deathsRateFemale": "f_death_rate",
    "deathsRateMale": "m_death_rate",
    "prevalenceNumberBoth": "prev",
    "prevalenceNumberFemale": "f_prev",
    "prevalenceNumberMale": "m_prev",
    "prevalencePercentBoth": "prev%",
    "prevalencePercentFemale": "f_prev%",
    "prevalencePercentMale": "m_prev%",
    "prevalenceRateBoth": "prev_rate",
    "prevalenceRateFemale": "f_prev_rate",
    "prevalenceRateMale": "m_prev_rate",
}

# Rename columns
result_df = result_df.rename(columns=column_mapping)

# Update numeric_cols with new names
numeric_cols = [
    "deaths",
    "f_deaths",
    "m_deaths",
    "deaths%",
    "f_deaths%",
    "m_deaths%",
    "death_rate",
    "f_death_rate",
    "m_death_rate",
    "prev",
    "f_prev",
    "m_prev",
    "prev%",
    "f_prev%",
    "m_prev%",
    "prev_rate",
    "f_prev_rate",
    "m_prev_rate",
    "obesity%",
    "ct_units",
    "ischemic_rate",
    "pacemaker_1m",
    "rheumatic_rate",
    "statin_use_k",
    "htn_death_std",
    "ischemic_std",
    "rheumatic_std",
    "cvd_share",
    "f_cvd_std",
    "f_htn_ctrl",
    "f_htn_diag",
    "f_htn",
    "f_cvd_u70%",
    "f_high_bp",
    "f_htn_rx",
    "m_cvd_std",
    "m_htn_ctrl",
    "m_htn_diag",
    "m_htn",
    "m_cvd_u70%",
    "m_high_bp",
    "m_htn_rx",
    "t_cvd_std",
    "t_htn_ctrl",
    "t_htn_diag",
    "t_htn",
    "t_cvd_u70%",
    "t_high_bp",
    "t_htn_rx",
]

# Update categorical_cols
categorical_cols = ["wb_income", "region", "statin_availability"]

# Process each entity separately
for entity in result_df["Entity"].unique():
    entity_data = result_df[result_df["Entity"] == entity].sort_values("Year")

    # Interpolate numeric columns
    for col in numeric_cols:
        if col in entity_data.columns:
            result_df.loc[entity_data.index, col] = interpolate_series(entity_data, col)

    # Fill 'Code' column with forward and backward fill
    if "Code" in entity_data.columns:
        result_df.loc[entity_data.index, "Code"] = (
            entity_data["Code"].fillna(method="ffill").fillna(method="bfill")
        )

    # Fill other categorical columns with mode
    for col in categorical_cols:
        if col in entity_data.columns:
            mode_val = (
                entity_data[col].mode().iloc[0] if not entity_data[col].mode().empty else None
            )
            if mode_val is not None:
                result_df.loc[entity_data.index, col] = result_df.loc[
                    entity_data.index, col
                ].fillna(mode_val)

# Apply extreme value imputation
for entity in result_df["Entity"].unique():
    entity_mask = result_df["Entity"] == entity
    entity_data = result_df[entity_mask].copy()

    # Process numeric columns
    for col in numeric_cols:
        if col in entity_data.columns and entity_data[col].isna().any():
            result_df.loc[entity_mask, col] = impute_extremes(entity_data, col)

    # Process categorical columns
    for col in categorical_cols:
        if col in entity_data.columns and entity_data[col].isna().any():
            result_df.loc[entity_mask, col] = impute_extremes(entity_data, col)

# Print statistics about remaining missing values
print("\nRemaining missing values after extreme imputation:\n")
missing_stats = result_df[numeric_cols + categorical_cols].isnull().sum()
print(missing_stats[missing_stats > 0].sort_values(ascending=False))

original = final_df
interpolated = result_df

print("Original missing values:\n")
print(original[numeric_cols + categorical_cols].isnull().sum().sort_values(ascending=False))

print("\nInterpolated missing values:\n")
print(interpolated[numeric_cols + categorical_cols].isnull().sum().sort_values(ascending=False))

# Calculate improvement
print("\nImprovement in missing values:\n")
for col in numeric_cols + categorical_cols:
    orig_missing = original[col].isnull().sum()
    interp_missing = interpolated[col].isnull().sum()
    if orig_missing > interp_missing:
        print(
            f"{col}: Filled {orig_missing - interp_missing} values ({(orig_missing - interp_missing)/orig_missing*100:.1f}% improvement)"
        )

pop = pd.read_excel(
    "/Users/dna/Library/CloudStorage/GoogleDrive-dna@reallygreattech.com/Shared drives/Heart Disease Data/Primary Data/Derek/cardiovascular-death-rate-vs-gdp-per-capita/Cardiovascular Death Rate vs GDP per Capita.xlsx"
)
# Rename columns in pop dataframe for consistency
pop = pop.rename(columns={"Country": "Entity", "Population (historical)": "Population"})
result_df = interpolated
# Merge population data with interpolated dataframe
result_df = result_df.merge(
    pop[["Entity", "Year", "Population"]], on=["Entity", "Year"], how="left"
)

# Update the Population column, keeping the original values where no match is found
result_df["Population"] = result_df["Population_y"].fillna(result_df["Population_x"])

# Drop the temporary columns
result_df = result_df.drop(["Population_x", "Population_y"], axis=1)

result_df.to_csv("../heart_disease_data.csv", index=False)
print(
    f"Data has {result_df.shape[0]} rows and {result_df.shape[1]} columns, representing {len(result_df['Entity'].unique())} entities(including 'Global')"
)
print(result_df.head())
