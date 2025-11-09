# Project 2 – Bid & Budget Optimization Across Channels

This project simulates a portfolio of campaigns across channels with different bids and budgets.
We:

- Generate synthetic auction-level performance data.
- Aggregate by channel and bid bucket.
- Fit a regression model to estimate conversions as a function of spend and bid.
- Run simple scenario analysis to recommend budget reallocation towards high-ROI channels.

## Files

- `generate_bid_data.py` – create synthetic bidding data.
- `bid_optimization_analysis.py` – fit model and print recommendations.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python generate_bid_data.py
python bid_optimization_analysis.py
```
