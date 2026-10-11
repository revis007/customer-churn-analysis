"""Customer churn analysis on a synthetic demo dataset."""
from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'outputs'
OUT.mkdir(exist_ok=True)
df = pd.read_csv(ROOT / 'customer_churn.csv')
required = {'customer_id', 'tenure_months', 'monthly_charges', 'contract_type', 'support_tickets', 'churn'}
if not required.issubset(df.columns):
    raise ValueError(f'Missing columns: {required - set(df.columns)}')
if df[list(required)].isna().any().any():
    raise ValueError('Missing values found in required columns')
print(f'Customers: {len(df)}')
print(f'Overall churn rate: {df.churn.mean():.1%}')

with sqlite3.connect(':memory:') as conn:
    df.to_sql('customers', conn, index=False)
    sql = '''SELECT contract_type, COUNT(*) AS customers,
                    SUM(churn) AS churned,
                    ROUND(100.0 * SUM(churn) / COUNT(*), 2) AS churn_rate_pct
             FROM customers GROUP BY contract_type ORDER BY churn_rate_pct DESC'''
    contract = pd.read_sql_query(sql, conn)
    print('\nChurn by contract type (SQL):\n', contract.to_string(index=False))
    contract.to_csv(OUT / 'churn_by_contract.csv', index=False)

bins = [-1, 6, 12, 24, 1000]
labels = ['0-6 months', '7-12 months', '13-24 months', '25+ months']
df['tenure_group'] = pd.cut(df.tenure_months, bins=bins, labels=labels)
tenure = df.groupby('tenure_group', observed=True).agg(customers=('churn', 'size'), churn_rate=('churn', 'mean')).reset_index()
tenure['churn_rate_pct'] = (tenure.churn_rate * 100).round(2)
tenure[['tenure_group', 'customers', 'churn_rate_pct']].to_csv(OUT / 'churn_by_tenure.csv', index=False)

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(contract.contract_type, contract.churn_rate_pct)
ax.set(ylabel='Churn rate (%)', title='Customer churn by contract type')
fig.tight_layout()
fig.savefig(OUT / 'churn_by_contract.png', dpi=150)
plt.close(fig)

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(tenure.tenure_group.astype(str), tenure.churn_rate_pct)
ax.set(ylabel='Churn rate (%)', title='Customer churn by tenure')
fig.tight_layout()
fig.savefig(OUT / 'churn_by_tenure.png', dpi=150)
plt.close(fig)

print('\nChurn by tenure:\n', tenure[['tenure_group', 'customers', 'churn_rate_pct']].to_string(index=False))
print('\nOutputs saved in:', OUT)
