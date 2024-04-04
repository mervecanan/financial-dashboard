# Financial Dashboard

This Streamlit application visualizes your bank transactions data through the following graphs and tables:

- Overall total: Sum of all transactions
- Monthly totals: Table showing the sum of each month's transactions
- Monthly expenses: Table showing only negative values' total for each month
- Top 10 Expenses: Highest expenses in the selected month as a table
- Top 10 Incomes: Highest incomes in the selected month as a table
- Cumulative transactions: Line chart showing the running total for the selected month
- Daily transactions: Line chart to show the transactions in the selected month
- Overall trend: All change in the entire data as a line chart

## Run Locally

Before running, replace the file path on line 5 with your own CSV file path.

This code requires pandas and streamlit libraries. You can install them using:

```bash
  pip install pandas streamlit
```

Then execute the following command:


```bash
  streamlit run app.py
```
