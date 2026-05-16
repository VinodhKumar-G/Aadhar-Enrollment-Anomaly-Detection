# Aadhaar Enrollment Trend, EDA, and Anomaly Detection

Expanded exploratory data analysis and statistical review of public Aadhaar enrollment data, focused on spotting operational shifts, demographic mix changes, and unusual enrollment patterns through transparent statistical methods.

## Project Goal
Build explainable decision-support analysis for Aadhaar enrollment operations using:
- data validation and quality review
- exploratory data analysis (EDA)
- descriptive and inferential statistics
- anomaly detection with interpretable rules
- reusable visuals for operational reporting

## Current Dataset Scope
- Source: public aggregated Aadhaar enrollment records
- File: `Data/aadhar_enrollment_bengaluru_rural.csv`
- Geographic values inside file: `Bengaluru Urban`, `Karnataka`
- Granularity in file: irregular snapshot dates, not a complete monthly time series
- Columns:
  - `date`
  - `state`
  - `district`
  - `pincode`
  - `age_0_5`
  - `age_5_17`
  - `age_18_greater`

Note: file name says `bengaluru_rural`, but dataset values currently point to `Bengaluru Urban`. Analysis uses file contents as source of truth.

## Analysis Added
Issue `#34` scope is covered through:
- dataset profiling and data-quality checks
- date coverage audit and snapshot-level aggregation
- descriptive statistics with skewness, kurtosis, and coefficient of variation
- correlation analysis across age cohorts and total enrollment
- top-pincode concentration analysis
- growth-rate and rolling-trend analysis
- anomaly detection using Z-score, modified Z-score, and IQR rules
- statistical tests:
  - Shapiro-Wilk normality test
  - linear trend regression
  - Wilcoxon signed-rank test for matched pincode shifts
  - chi-square test for age-mix shift between major snapshots

## Repository Structure

```text
Aadhar-Enrollment-Anomaly-Detection
|
+-- Data/
|   +-- aadhar_enrollment_bengaluru_rural.csv
+-- Notebook/
|   +-- Analysis.ipynb
|   +-- comprehensive_eda.py
+-- Visuals/
|   +-- eda_total_enrollment_trend.png
|   +-- eda_age_mix_trend.png
|   +-- eda_distribution_overview.png
|   +-- eda_correlation_heatmap.png
|   +-- eda_top_pincodes.png
+-- README.md
+-- requirements.txt
+-- .gitignore
```

## How To Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run full analysis script:

```bash
python Notebook/comprehensive_eda.py
```

Open notebook for guided EDA:

```bash
jupyter notebook Notebook/Analysis.ipynb
```

## Responsible AI Notes
- Uses only aggregated public data
- No personal or biometric information
- Statistical logic is transparent and auditable
- Intended for operational insight, not automated decision-making about individuals

## Key Caution
Because dataset currently contains only four snapshot dates, results are useful for monitoring and hypothesis generation, but not for strong causal or seasonal claims.
