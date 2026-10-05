"""Exploratory data analysis for Pew's World Religion Projections dataset."""

import numpy as ny
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


def main():
    # Data loading and inspection
    df = pd.read_csv("rounded_population (1).csv", skipinitialspace=True)

    print(df.dtypes)
    df.info()
    print(df.shape)
    print(df.describe())
    print(df.head())

    # Data cleaning
    # No missing values or duplicate rows were found in the notebook checks.
    print(df.isnull().sum())
    print(df.duplicated().sum())

    # Strip extra spaces so region and country values match reliably.
    df["Region"] = df["Region"].str.strip()
    df["Country"] = df["Country"].str.strip()

    # Feature engineering
    df["Major_Religions_Population"] = df[
        ["Christians", "Muslims", "Hindus", "Buddhists"]
    ].sum(axis=1)

    religions = [
        "Christians",
        "Muslims",
        "Hindus",
        "Buddhists",
        "Jews",
        "Folk Religions",
        "Other Religions",
    ]
    df["Religious Total"] = df[religions].sum(axis=1)
    df["Atheists/Agnostics %"] = df["Unaffiliated"] / df["All Religions"] * 100

    print(df.head())

    # Univariate analysis: histogram of Muslim population
    plt.figure(figsize=(8, 5))
    sns.histplot(data=df, x="Muslims", bins=20, kde=True)
    plt.title("Distribution of Muslim Population")
    plt.xlabel("Muslim Population")
    plt.ylabel("Frequency")
    plt.show()

    # Univariate analysis: total population of major religions
    religions = ["Christians", "Muslims", "Hindus", "Buddhists"]
    religion_totals = df[religions].sum()

    plt.figure(figsize=(9, 5))
    sns.barplot(x=religion_totals.index, y=religion_totals.values)
    plt.title("Total Population of Major Religions")
    plt.xlabel("Religion")
    plt.ylabel("Total Population")
    plt.show()

    # Univariate analysis: regional record distribution
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x="Region")
    plt.title("Number of Records by Region")
    plt.xlabel("Region")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.show()

    # Univariate analysis: population outliers
    religions = ["Christians", "Muslims", "Hindus", "Buddhists"]
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df[religions])
    plt.title("Population Distribution and Outliers of Major Religions")
    plt.xlabel("Religion")
    plt.ylabel("Population")
    plt.show()

    # Bivariate analysis: Muslim population versus Christian population
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x="Muslims", y="Christians")
    plt.title("Muslim Population vs Christian Population")
    plt.xlabel("Muslim Population")
    plt.ylabel("Christian Population")
    plt.show()

    # Bivariate analysis: Muslim population by region
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x="Region", y="Muslims")
    plt.title("Muslim Population Distribution by Region")
    plt.xlabel("Region")
    plt.ylabel("Muslim Population")
    plt.xticks(rotation=45)
    plt.show()

    # Heatmaps: religious composition shifts from 2010 to 2050
    religions = list(df.columns[3:-1])  # The eight religion columns.

    def share_change(data, key):
        """Return the 2050 minus 2010 share change in percentage points."""
        data_2010 = data[data.Year == 2010].set_index(key)
        data_2050 = data[data.Year == 2050].set_index(key)
        change = (
            data_2050[religions].div(data_2050["All Religions"], axis=0) * 100
            - data_2010[religions].div(data_2010["All Religions"], axis=0) * 100
        )
        too_small = (data_2010[religions] <= 10_000) | (data_2050[religions] <= 10_000)
        return change.mask(too_small)

    # Reload the source data for the religion-share comparisons.
    rel_df = pd.read_csv("rounded_population (1).csv", skipinitialspace=True)
    rel_df["Region"] = rel_df["Region"].str.strip()
    rel_df["Country"] = rel_df["Country"].str.strip()

    rel_regions = rel_df[
        (rel_df.Country == "All Countries") & (rel_df.Region != "World")
    ]

    plt.figure(figsize=(9, 4.5))
    sns.heatmap(
        share_change(rel_regions, "Region"),
        cmap="RdBu",
        center=0,
        annot=True,
        fmt="+.1f",
    )
    plt.title("Change in religious share by region, 2010 to 2050")
    plt.ylabel("")
    plt.show()

    # Heatmap: top 30 country movers with at least one million people.
    rel_countries = rel_df[rel_df.Country != "All Countries"]
    rel_change = share_change(rel_countries, "Country")
    rel_big = rel_countries[
        (rel_countries.Year == 2010)
        & (rel_countries["All Religions"] >= 1_000_000)
    ].Country
    rel_top = rel_change[rel_change.index.isin(rel_big)].abs().max(axis=1).nlargest(30).index

    plt.figure(figsize=(10, 11))
    sns.heatmap(rel_change.loc[rel_top], cmap="RdBu", center=0, annot=True, fmt="+.1f")
    plt.title("Top 30 country movers, 2010 to 2050")
    plt.ylabel("")
    plt.show()

    # Interactive chart: religious share over time by region.
    rel_regions = rel_df[
        (rel_df.Country == "All Countries") & (rel_df.Region != "World")
    ]
    rel_groups = list(rel_df.columns[3:-1])  # The eight religion columns.
    long = rel_regions.melt(
        id_vars=["Year", "Region", "All Religions"],
        value_vars=rel_groups,
        var_name="Religion",
        value_name="People",
    )
    long["Share (%)"] = long["People"] / long["All Religions"] * 100

    fig = px.line(
        long,
        x="Year",
        y="Share (%)",
        color="Religion",
        facet_col="Region",
        facet_col_wrap=3,
        markers=True,
        height=650,
        title="Religious share by region, 2010 to 2050",
    )
    fig.update_xaxes(dtick=10)
    fig.show()

    # Interactive world map: change in religious share by country.
    map_df = rel_change.reset_index().melt(
        id_vars="Country", var_name="Religion", value_name="Change (pp)"
    )
    fig = px.choropleth(
        map_df,
        locations="Country",
        locationmode="country names",
        color="Change (pp)",
        animation_frame="Religion",
        color_continuous_scale="RdBu",
        color_continuous_midpoint=0,
        range_color=(-20, 20),
        title="Change in religious share, 2010 to 2050",
    )
    fig.show()


if __name__ == "__main__":
    main()