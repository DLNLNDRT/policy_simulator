# Data Quality Report

## 1) Executive Summary
- **Overall Quality Score:** 98.4 / 100
- **Critical Issues (datasets/sheets failing key thresholds):** 0

**Scoring model:** 40% completeness, 30% consistency (duplicates & type uniformity), 30% validity (ranges & finite values).

## 2) Dataset Overview
### File Inventory & Schema Summary
**merged_dataset.xlsx**
- *Sheet:* `Sheet1` — rows: 288, columns: 7
  - Columns (sample): `Sex` (object), `F` (object), `Portugal` (float64), `Spain` (float64), `Sweden` (float64), `age_group` (object), `year` (int64)
  - Coverage: countries=8, years=6
**Density of pharmacists.csv**
- *Sheet:* `main` — rows: 117, columns: 8
  - Columns (sample): `IND_UUID` (object), `IND_NAME` (object), `DIM_GEO_CODE_TYPE` (object), `DIM_GEO_CODE_M49` (int64), `GEO_NAME_SHORT` (object), `DIM_TIME_TYPE` (object), `DIM_TIME` (int64), `RATE_PER_10000_N` (float64)
  - Coverage: countries=1, years=33
**Life Expectancy.csv**
- *Sheet:* `main` — rows: 594, columns: 13
  - Columns (sample): `IND_ID` (object), `IND_CODE` (object), `IND_UUID` (object), `IND_PER_CODE` (object), `DIM_TIME` (int64), `DIM_TIME_TYPE` (object), `DIM_GEO_CODE_M49` (int64), `DIM_GEO_CODE_TYPE` (object), `DIM_PUBLISH_STATE_CODE` (object), `IND_NAME` (object), `GEO_NAME_SHORT` (object), `DIM_SEX` (object), `AMOUNT_N` (float64)
  - Coverage: countries=9, years=22
**Government Spending.csv**
- *Sheet:* `main` — rows: 92, columns: 8
  - Columns (sample): `IND_UUID` (object), `IND_NAME` (object), `DIM_GEO_CODE_TYPE` (object), `DIM_GEO_CODE_M49` (int64), `GEO_NAME_SHORT` (object), `DIM_TIME_TYPE` (object), `DIM_TIME` (int64), `RATE_PER_100_N` (float64)
  - Coverage: countries=1, years=23
**Density.csv**
- *Sheet:* `main` — rows: 359, columns: 8
  - Columns (sample): `IND_UUID` (object), `IND_NAME` (object), `DIM_GEO_CODE_TYPE` (object), `DIM_GEO_CODE_M49` (int64), `GEO_NAME_SHORT` (object), `DIM_TIME_TYPE` (object), `DIM_TIME` (int64), `RATE_PER_10000_N` (float64)
  - Coverage: countries=3, years=34
**Density of nurses and midwives.csv**
- *Sheet:* `main` — rows: 111, columns: 8
  - Columns (sample): `IND_UUID` (object), `IND_NAME` (object), `DIM_GEO_CODE_TYPE` (object), `DIM_GEO_CODE_M49` (int64), `GEO_NAME_SHORT` (object), `DIM_TIME_TYPE` (object), `DIM_TIME` (int64), `RATE_PER_10000_N` (float64)
  - Coverage: countries=1, years=34
**Density of Doctors.csv**
- *Sheet:* `main` — rows: 131, columns: 8
  - Columns (sample): `IND_UUID` (object), `IND_NAME` (object), `DIM_GEO_CODE_TYPE` (object), `DIM_GEO_CODE_M49` (int64), `GEO_NAME_SHORT` (object), `DIM_TIME_TYPE` (object), `DIM_TIME` (int64), `RATE_PER_10000_N` (float64)
  - Coverage: countries=1, years=33
**Cause of Death.csv**
- *Sheet:* `main` — rows: 1072, columns: 5
  - Columns (sample): `DIM_COUNTRY_CODE` (object), `DIM_YEAR_CODE` (int64), `DIM_GHECAUSE_TITLE` (object), `DIM_SEX_CODE` (object), `VAL_DTHS_RATE100K_NUMERIC` (float64)
  - Coverage: countries=134, years=1
**Access to affordable medicine.csv**
- *Sheet:* `main` — rows: 99, columns: 8
  - Columns (sample): `IND_UUID` (object), `IND_NAME` (object), `DIM_GEO_CODE_TYPE` (object), `DIM_GEO_CODE_M49` (int64), `GEO_NAME_SHORT` (object), `DIM_TIME_TYPE` (object), `DIM_TIME` (int64), `RATE_PER_100_N` (int64)
  - Coverage: countries=1, years=25

## 3) Quality Metrics by Dataset
| Dataset/Sheet | Rows | Cols | Completeness % | Consistency % | Validity % | Quality Score | Duplicates % |
|---|---:|---:|---:|---:|---:|---:|---:|
| merged_dataset.xlsx::Sheet1 | 288 | 7 | 100.0 | 100.0 | 100.0 | 100.0 | 0.0 |
| Density of pharmacists.csv::main | 117 | 8 | 100.0 | 100.0 | 100.0 | 100.0 | 0.0 |
| Life Expectancy.csv::main | 594 | 13 | 100.0 | 100.0 | 100.0 | 100.0 | 0.0 |
| Government Spending.csv::main | 92 | 8 | 100.0 | 100.0 | 100.0 | 100.0 | 0.0 |
| Density.csv::main | 359 | 8 | 100.0 | 100.0 | 90.0 | 97.0 | 0.0 |
| Density of nurses and midwives.csv::main | 111 | 8 | 100.0 | 100.0 | 90.0 | 97.0 | 0.0 |
| Density of Doctors.csv::main | 131 | 8 | 100.0 | 100.0 | 100.0 | 100.0 | 0.0 |
| Cause of Death.csv::main | 1072 | 5 | 100.0 | 100.0 | 90.0 | 97.0 | 0.0 |
| Access to affordable medicine.csv::main | 99 | 8 | 100.0 | 100.0 | 100.0 | 100.0 | 0.0 |

## 4) Issue Analysis
### Critical Issues (High Business Impact)
- None detected under current thresholds.

### Moderate Issues (Medium Business Impact)
- **Density.csv::main** — 29 values in 'RATE_PER_10000_N' outside 0–100.
- **Density of nurses and midwives.csv::main** — 29 values in 'RATE_PER_10000_N' outside 0–100.
- **Cause of Death.csv::main** — 18 values in 'VAL_DTHS_RATE100K_NUMERIC' outside 0–100.

## 5) Recommendations
### Immediate Fixes (next 1–2 days)
- **Fill critical nulls**: Impute or backfill essential fields (Country, Year, target metrics). For numeric indicators, use forward-fill by (Country, Metric) grouped time series; otherwise, use domain defaults or mark as 'Unknown' with a data_provenance flag.
- **Remove or deduplicate exact duplicates** with a deterministic key (Country, Year, Metric) before modeling/embedding.
- **Sanitize ranges**: Clip percent/rate fields to [0,100], densities to ≥0, and life expectancy to [0,120]. Write exceptions to an `anomaly_log` table for review.
- **Standardize schemas**: Rename columns to a canonical set: `country`, `iso3`, `year`, `metric_name`, `value`, `unit`, `source`.

### Data Cleaning Pipeline (proposed)
1. **Ingest**: Read CSV/XLSX, enforce UTF-8, trim whitespace, normalize column names (snake_case).
2. **Schema Align**: Map source columns to canonical schema; assert required columns (`country`, `year`, `value`).
3. **Type Cast**: Coerce `year` to int, numeric fields to float; collect parse errors in `ingest_errors`.
4. **Deduplicate**: Drop full-row duplicates; then drop duplicates by (`country`,`year`,`metric_name`) keeping latest `source_date`.
5. **Range Validate**: Apply field rules (percent in [0,100], density ≥0, life_expectancy in [0,120]).
6. **Temporal Validate**: For rates per capita, flag spikes > 5σ or > 50% WoY change.
7. **Impute**: Group by country and do linear interpolation on yearly series; else KNN impute within region cluster.
8. **Enrich**: Attach ISO3 codes & regions from a reference table for cross-dataset joins.
9. **Persist**: Write clean tables plus `quality_metrics` snapshot (per run) to a warehouse (e.g., Supabase/Postgres).
10. **Publish**: Produce model-ready parquet & a metrics JSON consumed by the GenAI application.

### Monitoring & Governance Setup
- **Data contracts**: Define required columns, dtypes, and allowed ranges per dataset. Enforce with checks (e.g., Great Expectations / Pandera).
- **SLIs/SLOs**: Track completeness≥95%, duplicates≤0.5%, validity≥98%. Alert if breached.
- **Drift checks**: Kolmogorov–Smirnov by country for key metrics across monthly snapshots; alert on p<0.01.
- **Provenance**: Store `source_url`, `ingest_run_id`, `hash` per file; expose in GenAI app for transparency.
- **Bias auditing**: Ensure equitable country coverage; flag underrepresented regions that could bias the model.

## 6) Visual Insights Generated
- Bar chart: **Completeness by dataset/sheet** ![Completeness](completeness_by_dataset.png)
- Bar chart: **Validity by dataset/sheet** ![Validity](validity_by_dataset.png)
- Bar chart: **Consistency by dataset/sheet** ![Consistency](consistency_by_dataset.png)

## Validation Checklist
- [x] Overall quality score provided (0-100)
- [x] Each dataset has individual quality metrics
- [x] Issues prioritized by business impact
- [x] Actionable recommendations provided
- [x] Data pipeline guidance included
