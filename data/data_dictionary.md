# Heart Disease Data Dictionary

## Main Data Points

| Column Name | Description | Nullable | Data Type | Sample Value |
|------------|-------------|----------|-----------|--------------|
| Entity | Country or region name | No | string | Afghanistan |
| age | Age group | No | string | All Ages |
| cause | Type of heart disease | No | string | Cardiovascular diseases |
| Year | Year of observation | No | integer | 1980 |
| Code | Country code | Yes | string | AFG |
| gdp_pc | GDP per capita | Yes | float | 1280.46 |
| WB_Income | World Bank Income Classification | Yes | string | Low-income countries |
| Population | Total population | Yes | integer | 12045664 |
| region | Geographic region | Yes | string | South Asia |
| death_std | Standardized death rate | Yes | float | 696.06 |
| ischemic_rate | Rate of ischemic heart disease | Yes | float | 336.27 |
| rheumatic_rate | Rate of rheumatic heart disease | Yes | float | 7.24 |
| htn_death_std | Standardized hypertension death rate | Yes | float | 90.89 |
| ischemic_std | Standardized ischemic heart disease rate | Yes | float | 336.27 |
| rheumatic_std | Standardized rheumatic heart disease rate | Yes | float | 7.24 |
| cvd_share | Share of cardiovascular disease deaths | Yes | float | 36.87 |
| deaths | Total CVD deaths | No | float | 52184.06 |
| f_deaths | Female CVD deaths | No | float | 19608.30 |
| m_deaths | Male CVD deaths | No | float | 32575.76 |
| deaths% | Percentage of total deaths from CVD | No | percent | 0.1806 |
| f_deaths% | Percentage of female deaths from CVD | No | percent | 0.1500 |
| m_deaths% | Percentage of male deaths from CVD | No | percent | 0.2066 |
| death_rate | CVD death rate per 100k | No | float | 388.48 |
| f_death_rate | Female CVD death rate per 100k | No | float | 301.38 |
| m_death_rate | Male CVD death rate per 100k | No | float | 470.31 |
| prev | Total CVD prevalence | Yes | float | 687223.91 |
| f_prev | Female CVD prevalence | Yes | float | 269970.69 |
| m_prev | Male CVD prevalence | Yes | float | 417253.22 |
| prev% | Percentage of population with CVD | Yes | percent | 0.0700 |
| f_prev% | Percentage of female population with CVD | Yes | percent | 0.0538 |
| m_prev% | Percentage of male population with CVD | Yes | percent | 0.0870 |
| prev_rate | CVD prevalence rate per 100k | Yes | float | 6911.31 |
| f_prev_rate | Female CVD prevalence rate per 100k | Yes | float | 5299.19 |
| m_prev_rate | Male CVD prevalence rate per 100k | Yes | float | 8605.12 |
| f_cvd_std | Female standardized CVD rate | Yes | float | 501.00 |
| m_cvd_std | Male standardized CVD rate | Yes | float | 567.00 |
| t_cvd_std | Total standardized CVD rate | Yes | float | 531.00 |
| f_cvd_u70% | Female CVD deaths under 70% | Yes | percent | 53.57 |
| m_cvd_u70% | Male CVD deaths under 70% | Yes | percent | 62.88 |
| t_cvd_u70% | Total CVD deaths under 70% | Yes | percent | 58.13 |

## Disease Metrics

| Column Name | Description | Nullable | Data Type | Sample Value |
|------------|-------------|----------|-----------|--------------|
| valprevnumberboth | Total prevalence count for both genders | No | float | 687223.91 |
| valdeathsnumberboth | Total deaths count for both genders | No | float | 52184.06 |
| valprevrateboth | Prevalence rate per 100k for both genders | No | float | 6911.31 |
| valdeathsrateboth | Death rate per 100k for both genders | No | float | 388.48 |
| valprevpercentboth | Prevalence percentage for both genders | No | percent | 0.0700 |
| valdeathspercentboth | Death percentage for both genders | No | percent | 0.1806 |

## Gender-Specific Metrics

### Female
| Column Name | Description | Nullable | Data Type | Sample Value |
|------------|-------------|----------|-----------|--------------|
| valprevnumberfemale | Total prevalence count for females | No | float | 269970.69 |
| valdeathsnumberfemale | Total deaths count for females | No | float | 19608.30 |
| valprevratefemale | Prevalence rate per 100k for females | No | float | 5299.19 |
| valdeathsratefemale | Death rate per 100k for females | No | float | 301.38 |
| valprevpercentfemale | Prevalence percentage for females | No | percent | 0.0538 |
| valdeathspercentfemale | Death percentage for females | No | percent | 0.1500 |

### Male
| Column Name | Description | Nullable | Data Type | Sample Value |
|------------|-------------|----------|-----------|--------------|
| valprevnumbermale | Total prevalence count for males | No | float | 417253.22 |
| valdeathsnumbermale | Total deaths count for males | No | float | 32575.76 |
| valprevratemale | Prevalence rate per 100k for males | No | float | 8605.12 |
| valdeathsratemale | Death rate per 100k for males | No | float | 470.31 |
| valprevpercentmale | Prevalence percentage for males | No | percent | 0.0870 |
| valdeathspercentmale | Death percentage for males | No | percent | 0.2066 |

## Risk Factors and Healthcare Metrics

| Column Name | Description | Nullable | Data Type | Sample Value |
|------------|-------------|----------|-----------|--------------|
| ct_units | CT scanner units per million population | Yes | float | 0.19 |
| obesity% | Percentage of population with obesity | Yes | percent | 1.3 |
| pacemaker_1m | Pacemaker implants per 1 million population | Yes | float | 107.9 |
| t_htn_ctrl | Hypertension control rate | Yes | float | 23.4 |
| t_high_bp_30-79 | Prevalence of high blood pressure (ages 30-79) | Yes | float | 31.2 |
| t_htn_diag | Hypertension diagnosis rate | Yes | float | 52.1 |
| t_htn_rx_30-79 | Hypertension treatment rate (ages 30-79) | Yes | float | 47.3 |

## Notes
- Data includes both sex-specific (prefixed with f_ for female and m_ for male) and total population metrics (prefixed with t_)
- Most prevalence and risk factor data points are nullable, while core death statistics are generally complete
- Rates are typically per 100,000 population unless otherwise specified
- Percentage values are expressed in decimal form (e.g., 0.1806 = 18.06%)
- Sample values are from Afghanistan's data
- Data types:
  - string: Text values
  - integer: Whole numbers
  - float: Decimal numbers
  - percent: Decimal numbers representing percentages
