# Correlation & Pattern Analysis

## 1) Executive Summary
- **Strong relationships (|r| ≥ 0.7, p<0.05):** 4 pairs.
- **Moderate relationships (0.3 ≤ |r| < 0.7, p<0.05):** 0 pairs.

**Key patterns:**
- Merged Dataset Sheet1 → Year ↔ Year → 2 (r=1.00, n=288, p=0): Likely driven by shared socio-economic factors or definitional overlap.
- Merged Dataset Sheet1 → Portugal ↔ Merged Dataset Sheet1 → Spain (r=0.93, n=288, p=0): Likely driven by shared socio-economic factors or definitional overlap.
- Merged Dataset Sheet1 → Portugal ↔ Merged Dataset Sheet1 → Sweden (r=0.84, n=288, p=0): Likely driven by shared socio-economic factors or definitional overlap.
- Merged Dataset Sheet1 → Spain ↔ Merged Dataset Sheet1 → Sweden (r=0.97, n=288, p=0): Likely driven by shared socio-economic factors or definitional overlap.

## 2) Data Dictionary
| Feature | Source | Original Column | Business Definition | Example | Min | Max | Non-null | Country Key | Year Key |
|---|---|---|---|---:|---:|---:|---:|---|---|
| `access_to_affordable_medicine__dim_geo_code_m49` | Access to affordable medicine.csv::main | `DIM_GEO_CODE_M49` | Index or percentage of essential medicine affordability/availability. | 300.0 | 300.0 | 752.0 | 99 | IND_UUID | DIM_TIME |
| `access_to_affordable_medicine__dim_time` | Access to affordable medicine.csv::main | `DIM_TIME` | Index or percentage of essential medicine affordability/availability. | 2002.0 | 2000.0 | 2024.0 | 99 | IND_UUID | DIM_TIME |
| `access_to_affordable_medicine__rate_per_100_n` | Access to affordable medicine.csv::main | `RATE_PER_100_N` | Index or percentage of essential medicine affordability/availability. | 92.0 | 89.0 | 99.0 | 99 | IND_UUID | DIM_TIME |
| `cause_of_death__dim_year_code` | Cause of Death.csv::main | `DIM_YEAR_CODE` | Share/rate of deaths by cause; epidemiological burden. | 2021.0 | 2021.0 | 2021.0 | 1072 | DIM_GHECAUSE_TITLE | DIM_YEAR_CODE |
| `cause_of_death__val_dths_rate100k_numeric` | Cause of Death.csv::main | `VAL_DTHS_RATE100K_NUMERIC` | Share/rate of deaths by cause; epidemiological burden. | 0.0 | 0.0 | 283.75 | 1072 | DIM_GHECAUSE_TITLE | DIM_YEAR_CODE |
| `density__dim_geo_code_m49` | Density.csv::main | `DIM_GEO_CODE_M49` | Population-adjusted resource count; check unit (per 1k or per 10k). | 300.0 | 300.0 | 752.0 | 359 | IND_UUID | DIM_TIME |
| `density__dim_time` | Density.csv::main | `DIM_TIME` | Population-adjusted resource count; check unit (per 1k or per 10k). | 1999.0 | 1990.0 | 2023.0 | 359 | IND_UUID | DIM_TIME |
| `density__rate_per_10000_n` | Density.csv::main | `RATE_PER_10000_N` | Population-adjusted resource count; check unit (per 1k or per 10k). | 42.99 | 4.03 | 148.11 | 359 | IND_UUID | DIM_TIME |
| `density_of_doctors__dim_geo_code_m49` | Density of Doctors.csv::main | `DIM_GEO_CODE_M49` | Physicians per population (often per 1,000); access to clinical care. | 300.0 | 300.0 | 752.0 | 131 | IND_UUID | DIM_TIME |
| `density_of_doctors__dim_time` | Density of Doctors.csv::main | `DIM_TIME` | Physicians per population (often per 1,000); access to clinical care. | 1999.0 | 1990.0 | 2022.0 | 131 | IND_UUID | DIM_TIME |
| `density_of_doctors__rate_per_10000_n` | Density of Doctors.csv::main | `RATE_PER_10000_N` | Physicians per population (often per 1,000); access to clinical care. | 42.99 | 20.37 | 65.76 | 131 | IND_UUID | DIM_TIME |
| `density_of_nurses_and_midwives__dim_geo_code_m49` | Density of nurses and midwives.csv::main | `DIM_GEO_CODE_M49` | Nurses/midwives per population; nursing and maternal care capacity. | 300.0 | 300.0 | 752.0 | 111 | IND_UUID | DIM_TIME |
| `density_of_nurses_and_midwives__dim_time` | Density of nurses and midwives.csv::main | `DIM_TIME` | Nurses/midwives per population; nursing and maternal care capacity. | 2004.0 | 1990.0 | 2023.0 | 111 | IND_UUID | DIM_TIME |
| `density_of_nurses_and_midwives__rate_per_10000_n` | Density of nurses and midwives.csv::main | `RATE_PER_10000_N` | Nurses/midwives per population; nursing and maternal care capacity. | 35.31 | 28.3 | 148.11 | 111 | IND_UUID | DIM_TIME |
| `density_of_pharmacists__dim_geo_code_m49` | Density of pharmacists.csv::main | `DIM_GEO_CODE_M49` | Pharmacists per population; medication access/counseling. | 300.0 | 300.0 | 752.0 | 117 | IND_UUID | DIM_TIME |
| `density_of_pharmacists__dim_time` | Density of pharmacists.csv::main | `DIM_TIME` | Pharmacists per population; medication access/counseling. | 2004.0 | 1990.0 | 2022.0 | 117 | IND_UUID | DIM_TIME |
| `density_of_pharmacists__rate_per_10000_n` | Density of pharmacists.csv::main | `RATE_PER_10000_N` | Pharmacists per population; medication access/counseling. | 8.64 | 4.03 | 13.07 | 117 | IND_UUID | DIM_TIME |
| `government_spending__dim_geo_code_m49` | Government Spending.csv::main | `DIM_GEO_CODE_M49` | Government health expenditure (share of GDP or per capita). | 300.0 | 300.0 | 752.0 | 92 | IND_UUID | DIM_TIME |
| `government_spending__dim_time` | Government Spending.csv::main | `DIM_TIME` | Government health expenditure (share of GDP or per capita). | 2004.0 | 2000.0 | 2022.0 | 92 | IND_UUID | DIM_TIME |
| `government_spending__rate_per_100_n` | Government Spending.csv::main | `RATE_PER_100_N` | Government health expenditure (share of GDP or per capita). | 9.96563244 | 8.25187302 | 19.44090652 | 92 | IND_UUID | DIM_TIME |
| `life_expectancy__amount_n` | Life Expectancy.csv::main | `AMOUNT_N` | Average years a newborn is expected to live, given current mortality rates. | 82.47890882 | 52.08671592 | 85.66031336 | 594 | GEO_NAME_SHORT | DIM_TIME |
| `life_expectancy__dim_geo_code_m49` | Life Expectancy.csv::main | `DIM_GEO_CODE_M49` | Average years a newborn is expected to live, given current mortality rates. | 724.0 | 1.0 | 914.0 | 594 | GEO_NAME_SHORT | DIM_TIME |
| `life_expectancy__dim_time` | Life Expectancy.csv::main | `DIM_TIME` | Average years a newborn is expected to live, given current mortality rates. | 2000.0 | 2000.0 | 2021.0 | 594 | GEO_NAME_SHORT | DIM_TIME |
| `merged_dataset_sheet1__portugal` | merged_dataset.xlsx::Sheet1 | `Portugal` | Numeric indicator from source dataset; unit per original field. | 16.3178154461266 | 0.0 | 23.7578276763549 | 288 | age_group | year |
| `merged_dataset_sheet1__spain` | merged_dataset.xlsx::Sheet1 | `Spain` | Numeric indicator from source dataset; unit per original field. | 63.142510383337 | 0.0 | 63.142510383337 | 288 | age_group | year |
| `merged_dataset_sheet1__sweden` | merged_dataset.xlsx::Sheet1 | `Sweden` | Numeric indicator from source dataset; unit per original field. | 26.256468427661 | 0.0 | 26.256468427661 | 288 | age_group | year |
| `merged_dataset_sheet1__year` | merged_dataset.xlsx::Sheet1 | `year` | Numeric indicator from source dataset; unit per original field. | 2000.0 | 2000.0 | 2021.0 | 288 | age_group | year |

## 3) Correlation Analysis
Pearson correlations with approximate two-tailed p-values (Fisher z). Only **p < 0.05** pairs are included.
### Strong (|r| ≥ 0.7)
| Feature X | Feature Y | r | n | p | Interpretation |
|---|---|---:|---:|---:|---|
| `merged_dataset_sheet1__year` | `year__2` | 1.00 | 288 | 0 | Likely driven by shared socio-economic factors or definitional overlap. |
| `merged_dataset_sheet1__spain` | `merged_dataset_sheet1__sweden` | 0.97 | 288 | 0 | Likely driven by shared socio-economic factors or definitional overlap. |
| `merged_dataset_sheet1__portugal` | `merged_dataset_sheet1__spain` | 0.93 | 288 | 0 | Likely driven by shared socio-economic factors or definitional overlap. |
| `merged_dataset_sheet1__portugal` | `merged_dataset_sheet1__sweden` | 0.84 | 288 | 0 | Likely driven by shared socio-economic factors or definitional overlap. |

### Moderate (0.3 ≤ |r| < 0.7)
- None.

## 4) Entity Relationships (Join Feasibility)
| Dataset A | Dataset B | Join Feasibility (0-1) |
|---|---|---:|
| Density.csv::main | Density of nurses and midwives.csv::main | 0.51 |
| Density of pharmacists.csv::main | Density.csv::main | 0.50 |
| Density.csv::main | Density of Doctors.csv::main | 0.50 |
| merged_dataset.xlsx::Sheet1 | Density of pharmacists.csv::main | 0.00 |
| merged_dataset.xlsx::Sheet1 | Life Expectancy.csv::main | 0.00 |
| merged_dataset.xlsx::Sheet1 | Government Spending.csv::main | 0.00 |
| merged_dataset.xlsx::Sheet1 | Density.csv::main | 0.00 |
| merged_dataset.xlsx::Sheet1 | Density of nurses and midwives.csv::main | 0.00 |
| merged_dataset.xlsx::Sheet1 | Density of Doctors.csv::main | 0.00 |
| merged_dataset.xlsx::Sheet1 | Cause of Death.csv::main | 0.00 |
| merged_dataset.xlsx::Sheet1 | Access to affordable medicine.csv::main | 0.00 |
| Density of pharmacists.csv::main | Life Expectancy.csv::main | 0.00 |
| Density of pharmacists.csv::main | Government Spending.csv::main | 0.00 |
| Density of pharmacists.csv::main | Density of nurses and midwives.csv::main | 0.00 |
| Density of pharmacists.csv::main | Density of Doctors.csv::main | 0.00 |
| Density of pharmacists.csv::main | Cause of Death.csv::main | 0.00 |
| Density of pharmacists.csv::main | Access to affordable medicine.csv::main | 0.00 |
| Life Expectancy.csv::main | Government Spending.csv::main | 0.00 |
| Life Expectancy.csv::main | Density.csv::main | 0.00 |
| Life Expectancy.csv::main | Density of nurses and midwives.csv::main | 0.00 |
| Life Expectancy.csv::main | Density of Doctors.csv::main | 0.00 |
| Life Expectancy.csv::main | Cause of Death.csv::main | 0.00 |
| Life Expectancy.csv::main | Access to affordable medicine.csv::main | 0.00 |
| Government Spending.csv::main | Density.csv::main | 0.00 |
| Government Spending.csv::main | Density of nurses and midwives.csv::main | 0.00 |
| Government Spending.csv::main | Density of Doctors.csv::main | 0.00 |
| Government Spending.csv::main | Cause of Death.csv::main | 0.00 |
| Government Spending.csv::main | Access to affordable medicine.csv::main | 0.00 |
| Density.csv::main | Cause of Death.csv::main | 0.00 |
| Density.csv::main | Access to affordable medicine.csv::main | 0.00 |

- Keys inferred: country and year. Normalize to ISO3 codes and integer year for robust joins.
- Anticipated risks: country naming mismatches and non-overlapping year ranges; introduce a reference country table and enforce `year` int.

## 5) Temporal Patterns
No sufficient yearly coverage to estimate trends.

## 6) Business Context Integration
- **Benchmarks:** Life expectancy commonly ~65–85 years; physician density ~1–6 per 1,000; nurses ~3–15 per 1,000; health spending ~5–12% of GDP. Align units to these bands.
- **Regulatory notes:** When surfacing health insights, avoid clinical advice. Cite sources and methodology in UI (WHO definitions may vary).
- **GenAI feature ideas:**
  - *Explanatory insights*: tooltips linking workforce density to outcomes with context and uncertainty.
  - *What-if*: sliders for workforce or spending changes projecting expected directional impact on outcomes.
  - *Data hygiene guardrails*: auto-flag and annotate values outside benchmark bands before answer generation.
- **Link to Data Quality Findings:** Prioritize cleaning datasets flagged as critical to prevent spurious correlations; prefer features with high completeness/validity in retrieval-augmented pipelines.

## Visuals
- Correlation heatmap: ![correlation_heatmap.png](correlation_heatmap.png)

## Validation Checklist
- ) Data dictionary complete with business context
- ) Correlation analysis includes statistical significance
- ) Entity relationships mapped with join success rates
- ) Temporal patterns documented with seasonality
- ) Business domain knowledge integrated