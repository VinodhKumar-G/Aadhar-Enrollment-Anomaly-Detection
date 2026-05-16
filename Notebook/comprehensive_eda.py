from __future__ import annotations

import inspect
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "Data" / "aadhar_enrollment_bengaluru_rural.csv"
VISUALS_DIR = BASE_DIR / "Visuals"
AGE_COLUMNS = ["age_0_5", "age_5_17", "age_18_greater"]


def load_enrollment_data(csv_path: Path = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")

    if df["date"].isna().any():
        raise ValueError("Date parsing failed for one or more rows.")

    df = df.sort_values(["date", "pincode"]).reset_index(drop=True)
    df["total_enrollment"] = df[AGE_COLUMNS].sum(axis=1)

    for column in AGE_COLUMNS:
        share_column = f"{column}_share"
        df[share_column] = np.where(
            df["total_enrollment"] > 0,
            df[column] / df["total_enrollment"],
            np.nan,
        )

    df["month"] = df["date"].dt.to_period("M").astype(str)
    return df


def dataset_profile(df: pd.DataFrame) -> pd.DataFrame:
    profile = {
        "rows": len(df),
        "columns": len(df.columns),
        "date_start": df["date"].min().date().isoformat(),
        "date_end": df["date"].max().date().isoformat(),
        "unique_dates": df["date"].nunique(),
        "unique_pincodes": df["pincode"].nunique(),
        "unique_states": df["state"].nunique(),
        "unique_districts": df["district"].nunique(),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_cells": int(df.isna().sum().sum()),
        "district_in_file": ", ".join(sorted(df["district"].unique())),
        "state_in_file": ", ".join(sorted(df["state"].unique())),
        "total_enrollment_sum": int(df["total_enrollment"].sum()),
        "median_record_total": float(df["total_enrollment"].median()),
    }
    return pd.DataFrame({"metric": list(profile.keys()), "value": list(profile.values())})


def date_coverage_summary(df: pd.DataFrame) -> pd.DataFrame:
    coverage = (
        df.groupby("date")
        .agg(
            records=("pincode", "count"),
            unique_pincodes=("pincode", "nunique"),
            total_enrollment=("total_enrollment", "sum"),
        )
        .reset_index()
    )
    coverage["date"] = coverage["date"].dt.strftime("%Y-%m-%d")
    return coverage


def descriptive_statistics(df: pd.DataFrame) -> pd.DataFrame:
    numeric_columns = AGE_COLUMNS + ["total_enrollment"]
    summary = df[numeric_columns].describe().T
    summary["skewness"] = df[numeric_columns].skew()
    summary["kurtosis"] = df[numeric_columns].kurtosis()
    summary["coefficient_of_variation_pct"] = (
        df[numeric_columns].std() / df[numeric_columns].mean() * 100
    )
    return summary.round(3)


def pincode_summary(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    summary = (
        df.groupby("pincode")
        .agg(
            records=("pincode", "count"),
            total_enrollment=("total_enrollment", "sum"),
            avg_enrollment=("total_enrollment", "mean"),
            std_enrollment=("total_enrollment", "std"),
        )
        .fillna(0.0)
        .sort_values("total_enrollment", ascending=False)
        .head(top_n)
        .reset_index()
    )
    return summary.round(2)


def aggregate_by_date(df: pd.DataFrame) -> pd.DataFrame:
    daily = (
        df.groupby("date")[AGE_COLUMNS + ["total_enrollment"]]
        .sum()
        .reset_index()
        .sort_values("date")
        .reset_index(drop=True)
    )
    daily["growth_pct"] = daily["total_enrollment"].pct_change() * 100
    daily["rolling_mean_2"] = daily["total_enrollment"].rolling(window=2, min_periods=1).mean()
    total_std = daily["total_enrollment"].std(ddof=0)
    if total_std == 0:
        daily["z_score"] = 0.0
    else:
        daily["z_score"] = stats.zscore(daily["total_enrollment"], ddof=0)

    median_total = daily["total_enrollment"].median()
    mad_total = np.median(np.abs(daily["total_enrollment"] - median_total))
    if mad_total == 0:
        daily["modified_z_score"] = 0.0
    else:
        daily["modified_z_score"] = 0.6745 * (daily["total_enrollment"] - median_total) / mad_total

    q1 = daily["total_enrollment"].quantile(0.25)
    q3 = daily["total_enrollment"].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    daily["iqr_outlier"] = (
        (daily["total_enrollment"] < lower_bound) | (daily["total_enrollment"] > upper_bound)
    )
    daily["z_outlier"] = daily["z_score"].abs() > 1.5
    daily["modified_z_outlier"] = daily["modified_z_score"].abs() > 3.5

    for column in AGE_COLUMNS:
        daily[f"{column}_share"] = daily[column] / daily["total_enrollment"]

    return daily


def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    return df[AGE_COLUMNS + ["total_enrollment"]].corr().round(3)


def statistical_tests(df: pd.DataFrame, daily: pd.DataFrame) -> pd.DataFrame:
    test_rows: list[dict[str, object]] = []

    shapiro_stat, shapiro_p = stats.shapiro(df["total_enrollment"])
    test_rows.append(
        {
            "test": "Shapiro-Wilk normality",
            "scope": "record-level total_enrollment",
            "statistic": round(float(shapiro_stat), 4),
            "p_value": round(float(shapiro_p), 6),
            "insight": "p < 0.05 suggests non-normal distribution",
        }
    )

    regression = stats.linregress(np.arange(len(daily)), daily["total_enrollment"])
    test_rows.append(
        {
            "test": "Linear trend regression",
            "scope": "date-level total_enrollment",
            "statistic": round(float(regression.slope), 4),
            "p_value": round(float(regression.pvalue), 6),
            "insight": "positive slope means upward trend across snapshots",
        }
    )

    pivot = (
        df.assign(snapshot=df["date"].dt.strftime("%Y-%m-%d"))
        .pivot_table(index="pincode", columns="snapshot", values="total_enrollment", aggfunc="sum")
    )
    if {"2025-06-01", "2025-07-01"}.issubset(pivot.columns):
        matched = pivot[["2025-06-01", "2025-07-01"]].dropna()
        if not matched.empty:
            wilcoxon_stat, wilcoxon_p = stats.wilcoxon(
                matched["2025-06-01"], matched["2025-07-01"]
            )
            test_rows.append(
                {
                    "test": "Wilcoxon signed-rank",
                    "scope": "matched pincode totals: 2025-06-01 vs 2025-07-01",
                    "statistic": round(float(wilcoxon_stat), 4),
                    "p_value": round(float(wilcoxon_p), 6),
                    "insight": "tests whether paired pincode totals shifted between major snapshots",
                }
            )

    age_mix = df[df["date"].isin(pd.to_datetime(["2025-06-01", "2025-07-01"]))].groupby("date")[
        AGE_COLUMNS
    ].sum()
    if len(age_mix) == 2:
        chi2, p_value, _, _ = stats.chi2_contingency(age_mix)
        test_rows.append(
            {
                "test": "Chi-square composition shift",
                "scope": "age mix: 2025-06-01 vs 2025-07-01",
                "statistic": round(float(chi2), 4),
                "p_value": round(float(p_value), 6),
                "insight": "tests whether age-group shares changed between major snapshots",
            }
        )

    return pd.DataFrame(test_rows)


def anomaly_summary(daily: pd.DataFrame) -> pd.DataFrame:
    anomalies = daily.loc[
        daily["z_outlier"] | daily["modified_z_outlier"] | daily["iqr_outlier"],
        [
            "date",
            "total_enrollment",
            "growth_pct",
            "z_score",
            "modified_z_score",
            "z_outlier",
            "modified_z_outlier",
            "iqr_outlier",
        ],
    ].copy()
    anomalies["date"] = anomalies["date"].dt.strftime("%Y-%m-%d")
    return anomalies.round(3)


def create_visuals(df: pd.DataFrame, daily: pd.DataFrame, output_dir: Path = VISUALS_DIR) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    created_files: list[Path] = []

    plt.style.use("ggplot")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(daily["date"], daily["total_enrollment"], marker="o", linewidth=2, label="Total")
    ax.plot(daily["date"], daily["rolling_mean_2"], linestyle="--", linewidth=2, label="2-point rolling mean")
    anomaly_dates = daily.loc[daily["z_outlier"], "date"]
    anomaly_values = daily.loc[daily["z_outlier"], "total_enrollment"]
    ax.scatter(anomaly_dates, anomaly_values, color="crimson", s=80, label="Z-score anomaly")
    ax.set_title("Aadhaar Enrollment Trend Across Available Snapshots")
    ax.set_xlabel("Date")
    ax.set_ylabel("Enrollment Count")
    ax.legend()
    fig.autofmt_xdate()
    trend_path = output_dir / "eda_total_enrollment_trend.png"
    fig.tight_layout()
    fig.savefig(trend_path, dpi=200)
    plt.close(fig)
    created_files.append(trend_path)

    share_columns = [f"{column}_share" for column in AGE_COLUMNS]
    fig, ax = plt.subplots(figsize=(10, 5))
    for share_column, label in zip(
        share_columns,
        ["Age 0-5 share", "Age 5-17 share", "Age 18+ share"],
    ):
        ax.plot(daily["date"], daily[share_column], marker="o", linewidth=2, label=label)
    ax.set_title("Age-Group Mix by Snapshot")
    ax.set_xlabel("Date")
    ax.set_ylabel("Share of Total Enrollment")
    ax.legend()
    fig.autofmt_xdate()
    share_path = output_dir / "eda_age_mix_trend.png"
    fig.tight_layout()
    fig.savefig(share_path, dpi=200)
    plt.close(fig)
    created_files.append(share_path)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].hist(df["total_enrollment"], bins=12, color="#4C72B0", edgecolor="black")
    axes[0].set_title("Distribution of Record-Level Total Enrollment")
    axes[0].set_xlabel("Total Enrollment")
    axes[0].set_ylabel("Frequency")
    boxplot_data = [df[column] for column in AGE_COLUMNS + ["total_enrollment"]]
    boxplot_labels = ["Age 0-5", "Age 5-17", "Age 18+", "Total"]
    boxplot_signature = inspect.signature(axes[1].boxplot)
    if "tick_labels" in boxplot_signature.parameters:
        axes[1].boxplot(boxplot_data, tick_labels=boxplot_labels)
    else:
        axes[1].boxplot(boxplot_data, labels=boxplot_labels)
    axes[1].set_title("Boxplots for Age Segments and Total")
    axes[1].set_ylabel("Enrollment Count")
    distribution_path = output_dir / "eda_distribution_overview.png"
    fig.tight_layout()
    fig.savefig(distribution_path, dpi=200)
    plt.close(fig)
    created_files.append(distribution_path)

    corr = correlation_matrix(df)
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(corr.values, cmap="Blues", vmin=0, vmax=1)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_xticklabels(["Age 0-5", "Age 5-17", "Age 18+", "Total"], rotation=30, ha="right")
    ax.set_yticks(range(len(corr.index)))
    ax.set_yticklabels(["Age 0-5", "Age 5-17", "Age 18+", "Total"])
    ax.set_title("Correlation Heatmap")
    for row in range(corr.shape[0]):
        for col in range(corr.shape[1]):
            ax.text(col, row, f"{corr.iloc[row, col]:.2f}", ha="center", va="center", color="black")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    correlation_path = output_dir / "eda_correlation_heatmap.png"
    fig.tight_layout()
    fig.savefig(correlation_path, dpi=200)
    plt.close(fig)
    created_files.append(correlation_path)

    top_pincodes = pincode_summary(df, top_n=10).sort_values("total_enrollment")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top_pincodes["pincode"].astype(str), top_pincodes["total_enrollment"], color="#55A868")
    ax.set_title("Top 10 Pincodes by Total Enrollment")
    ax.set_xlabel("Total Enrollment")
    ax.set_ylabel("Pincode")
    top_pincode_path = output_dir / "eda_top_pincodes.png"
    fig.tight_layout()
    fig.savefig(top_pincode_path, dpi=200)
    plt.close(fig)
    created_files.append(top_pincode_path)

    return created_files


def run_full_analysis() -> dict[str, pd.DataFrame]:
    df = load_enrollment_data()
    daily = aggregate_by_date(df)
    results = {
        "profile": dataset_profile(df),
        "coverage": date_coverage_summary(df),
        "descriptive_statistics": descriptive_statistics(df),
        "correlation_matrix": correlation_matrix(df),
        "pincode_summary": pincode_summary(df),
        "statistical_tests": statistical_tests(df, daily),
        "anomalies": anomaly_summary(daily),
        "daily_summary": daily,
    }
    create_visuals(df, daily)
    return results


if __name__ == "__main__":
    analysis = run_full_analysis()
    for section_name, section_df in analysis.items():
        print(f"\n=== {section_name.upper()} ===")
        print(section_df.to_string(index=section_name == "descriptive_statistics"))
