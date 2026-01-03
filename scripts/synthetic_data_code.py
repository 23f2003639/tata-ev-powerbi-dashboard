"""
Synthetic Tata Motors EV Dataset Generator

This script generates a synthetic dataset for analyzing EV sales,
revenue trends, model-wise performance, state-wise adoption,
and charging infrastructure growth in India.

All data is artificially generated for learning, analysis,
and dashboarding purposes only.
"""

import numpy as np
import pandas as pd

# Reproducibility
np.random.seed(42)

# Settings
start_date = "2015-01-01"
periods = 100  # 100 months (~8 years)
dates = pd.date_range(start=start_date, periods=periods, freq="M")

states = [
    "Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "Gujarat",
    "Rajasthan", "West Bengal", "Punjab", "Kerala", "Uttar Pradesh"
]
models = ["Nexon EV", "Tigor EV", "Tiago EV", "Punch EV"]

# For cumulative charging stations per state
cumulative_charging = {state: 0 for state in states}

rows = []

for dt in dates:
    months_since_start = (
        (dt.year - pd.to_datetime(start_date).year) * 12
        + (dt.month - pd.to_datetime(start_date).month)
    )

    # National-level EV sales
    base_sales = 2000 + months_since_start * 50
    national_sales = np.random.poisson(lam=base_sales)

    # Model-wise sales distribution
    model_props = np.random.dirichlet(np.ones(len(models)))
    model_sales = (model_props * national_sales).astype(int)

    # Revenue per model (in crores)
    revenue_model = []
    for units in model_sales:
        avg_price_lakh = np.random.uniform(13, 18)
        revenue_crores = round(units * avg_price_lakh * 100_000 / 10_000_000, 2)
        revenue_model.append(revenue_crores)

    national_revenue_crores = sum(revenue_model)

    # Market share trend
    market_share = round(
        2 + np.linspace(0, 8, periods)[months_since_start]
        + np.random.normal(0, 0.5), 2
    )
    if market_share < 0:
        market_share = round(np.random.uniform(1, 3), 2)

    # Split national sales across states
    state_props = np.random.dirichlet(np.ones(len(states)))
    state_sales = (state_props * national_sales).astype(int)

    for idx, state in enumerate(states):
        added_stations = np.random.randint(5, 25)
        cumulative_charging[state] += added_stations

        state_revenue = round(
            (state_sales[idx] / national_sales) * national_revenue_crores, 2
        )

        row = {
            "date": dt,
            "year": dt.year,
            "month": dt.month,

            # National metrics
            "national_ev_sales": national_sales,
            "national_ev_revenue_crores": national_revenue_crores,
            "national_ev_market_share_pct": market_share,

            # Model-wise sales & revenue
            "nexon_ev_sales": model_sales[0],
            "tigor_ev_sales": model_sales[1],
            "tiago_ev_sales": model_sales[2],
            "punch_ev_sales": model_sales[3],
            "nexon_ev_revenue_crores": revenue_model[0],
            "tigor_ev_revenue_crores": revenue_model[1],
            "tiago_ev_revenue_crores": revenue_model[2],
            "punch_ev_revenue_crores": revenue_model[3],

            # State-level metrics
            "state": state,
            "state_ev_sales": state_sales[idx],
            "state_ev_revenue_crores": state_revenue,
            "charging_stations_added_state": added_stations,
            "cumulative_charging_stations_state": cumulative_charging[state]
        }

        rows.append(row)

# Create DataFrame
df = pd.DataFrame(rows)

# Save dataset
output_file = "Project_TataMotors_Raw_Dataset.csv"
df.to_csv(output_file, index=False)

print(f"Dataset created successfully: {output_file}")
print("Shape:", df.shape)
print(df.head())
