import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def aggregate_by_channel(df: pd.DataFrame) -> pd.DataFrame:
    agg = df.groupby("channel").agg(
        spend=("spend_usd", "sum"),
        conversions=("conversions", "sum"),
        clicks=("clicks", "sum")
    )
    agg["CPA"] = agg["spend"] / agg["conversions"].replace(0, np.nan)
    agg["CTR"] = agg["clicks"] / df.groupby("channel")["impressions"].sum()
    agg["ROI"] = agg["conversions"] / agg["spend"].replace(0, np.nan)
    return agg

def fit_response_model(df: pd.DataFrame):
    # Simple model: conversions as function of spend and bid
    X = df[["spend_usd", "bid"]].values
    y = df["conversions"].values
    model = LinearRegression()
    model.fit(X, y)
    return model

def recommend_budget_shift(df: pd.DataFrame, total_budget: float = 5000.0):
    channel_agg = aggregate_by_channel(df)
    roi = channel_agg["ROI"].fillna(0.0)
    weights = roi.clip(lower=0)
    if weights.sum() == 0:
        weights[:] = 1.0
    weights = weights / weights.sum()
    recommended = (weights * total_budget).to_frame(name="recommended_budget")
    result = channel_agg.join(recommended)
    return result.sort_values("ROI", ascending=False)

if __name__ == "__main__":
    df = pd.read_csv("bid_data.csv", parse_dates=["date"])
    print("===== Channel performance summary =====")
    channel_summary = aggregate_by_channel(df)
    print(channel_summary)

    print("\n===== Fitted response model (conversions ~ spend + bid) =====")
    model = fit_response_model(df)
    print(f"Intercept: {model.intercept_:.4f}")
    print(f"Coefficients (spend, bid): {model.coef_}")

    print("\n===== Recommended budget allocation (example, total 5000 USD) =====")
    rec = recommend_budget_shift(df, total_budget=5000.0)
    print(rec[["spend", "conversions", "ROI", "recommended_budget"]])
