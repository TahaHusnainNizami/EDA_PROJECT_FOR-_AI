# Pew World Religion Projections EDA

Exploratory data analysis of Pew's world religion population projections from 2010 to 2050.

## Project Files

- `main.py` - Python script containing the complete analysis workflow.
- `eda-project.ipynb` - Original Jupyter Notebook version of the analysis.
- `rounded_population (1).csv` - Required input dataset. Place this file in the project folder before running the script.

## Analysis Includes

- Dataset inspection and descriptive statistics
- Missing-value and duplicate checks
- Cleanup of region and country names
- Feature engineering for religious population totals and unaffiliated population percentages
- Histograms, bar charts, countplots, boxplots, and scatterplots
- Heatmaps showing religious share changes by region and country
- Interactive Plotly charts showing religious share over time
- An interactive world map of religious share changes

## Requirements

- Python 3.9 or newer
- The CSV dataset named `rounded_population (1).csv`

Install the required Python packages:

```bash
python -m pip install numpy pandas matplotlib seaborn plotly
```

## Run the Analysis

From the project directory, run:

```bash
python main.py
```

The script prints dataset summaries and opens the generated charts. Plotly visualizations may open in a browser or in the configured Python environment.

## Input Data

The dataset should contain columns for `Year`, `Region`, `Country`, `All Religions`, `Unaffiliated`, and the religion population categories used by the analysis, including `Christians`, `Muslims`, `Hindus`, `Buddhists`, `Jews`, `Folk Religions`, and `Other Religions`.