# Customer Churn & Retention Analysis

A beginner-friendly **portfolio demonstration** of customer churn analysis using Python, Pandas, SQL (SQLite), and Matplotlib.

> **Dataset disclosure:** `customer_churn.csv` is synthetic, generated for learning. Results are illustrative, not findings about a real business.

## Business questions
- What percentage of customers churned?
- How does churn vary by contract type?
- How does churn vary with customer tenure?

## Files
- `customer_churn.csv` — synthetic customer-level data
- `analysis.py` — validation, descriptive analysis, SQL aggregation, charts
- `requirements.txt` — Python dependencies
- `outputs/` — created when the script runs; includes CSV summaries and PNG charts

## Run locally
```bash
pip install -r requirements.txt
python analysis.py
```

## Methods
- **Churn rate:** number of customers with `churn=1` / total customers.
- **SQL:** SQLite `GROUP BY` analysis for churn rate by contract type.
- **Segmentation:** tenure buckets (0–6, 7–12, 13–24, 25+ months).

## Interpret responsibly
Differences between groups are **associations, not causal evidence**. With a real dataset, validate data quality, sample sizes, confounders, and business context before making retention recommendations.

## Possible next steps
- Replace synthetic data with a licensed, documented real dataset.
- Add retention cohorts, customer lifetime value, and statistical uncertainty.
- Build a Power BI dashboard using the exported summary CSV files.
