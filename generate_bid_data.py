import numpy as np
import pandas as pd

def generate_bid_data(n_rows: int = 8000, random_state: int = 123) -> pd.DataFrame:
    rng = np.random.default_rng(random_state)
    channels = np.array(['Google', 'Facebook', 'Baidu', 'Naver', 'Twitter'])
    campaigns = np.array(['Hotel', 'Flight', 'Vacation'])
    countries = np.array(['TH', 'TW', 'KR', 'JP', 'SG'])

    rows = []
    dates = pd.date_range('2025-01-01', periods=60, freq='D')
    for i in range(n_rows):
        date = rng.choice(dates)
        channel = rng.choice(channels)
        campaign = rng.choice(campaigns)
        country = rng.choice(countries)

        base_bid = rng.uniform(0.1, 2.0)
        budget = rng.uniform(50, 500)

        impressions = rng.integers(200, 20000)
        ctr_factor = 0.02 + 0.01 * (base_bid > 1.0)
        clicks = rng.binomial(impressions, min(ctr_factor, 0.35))
        clicks = max(clicks, 1)

        cvr_factor = 0.03 + 0.01 * (channel in ['Google', 'Baidu'])
        conversions = rng.binomial(clicks, min(cvr_factor, 0.5))

        avg_cpc = base_bid * rng.uniform(0.7, 1.3)
        spend = min(clicks * avg_cpc, budget)

        rows.append({
            "date": date,
            "channel": channel,
            "campaign": campaign,
            "country": country,
            "bid": round(float(base_bid), 3),
            "daily_budget": round(float(budget), 2),
            "impressions": int(impressions),
            "clicks": int(clicks),
            "conversions": int(conversions),
            "spend_usd": float(round(spend, 2)),
        })

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    df.to_csv("bid_data.csv", index=False)
    print(f"Generated bid_data.csv with {len(df)} rows")
    return df

if __name__ == "__main__":
    generate_bid_data()
