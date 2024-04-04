import pandas as pd
import streamlit as st

# Read the CSV file
file_path = "xxx.csv" # replace with the path of your transactions.csv
data = pd.read_csv(file_path, sep=";")

# Convert Buchungsdatum (transaction date) to datetime
data["Buchungsdatum"] = pd.to_datetime(data["Buchungsdatum"], format="%d.%m.%Y")

# Convert Betrag (amount) to float
data["Betrag"] = data["Betrag"].str.replace(".", "")
data["Betrag"] = data["Betrag"].str.replace(",", ".").astype(float)

# Calculate overall total
overall_total = data["Betrag"].sum()

# Calculate monthly total
monthly_data = (
    data.resample("M", on="Buchungsdatum")
    .agg(Total_Amount=("Betrag", "sum"))
    .reset_index()
)

# Calculate monthly expenses
monthly_expenses = (
    data[data["Betrag"] < 0]
    .resample("M", on="Buchungsdatum")
    .agg(Total_Expense=("Betrag", "sum"))
    .reset_index()
)

# Title
st.title("Financial Dashboard")

# Show overall sum
st.subheader("Overall Total")
frame = st.empty()
frame.markdown(f"**{overall_total:.2f} €**", unsafe_allow_html=True)

# Monthly totals table
st.subheader("Monthly Totals")
with st.expander("View Monthly Totals"):
    st.dataframe(monthly_data, use_container_width=True)

# Monthly Expenses Table
st.subheader("Monthly Expenses")
with st.expander("View Monthly Expenses"):
    st.dataframe(monthly_expenses, use_container_width=True)

# Month and Year Slider
min_year = data["Buchungsdatum"].dt.year.min()
max_year = data["Buchungsdatum"].dt.year.max()
selected_year = st.slider(
    "Select Year", min_value=min_year, max_value=max_year, value=max_year
)
selected_month_index = st.slider("Select Month", min_value=1, max_value=12, value=12)
selected_month = pd.to_datetime(
    str(selected_year) + "-" + str(selected_month_index).zfill(2) + "-01"
).month_name()

# Filter data based on month and year
filtered_data = data[
    (data["Buchungsdatum"].dt.year == selected_year)
    & (data["Buchungsdatum"].dt.month_name() == selected_month)
]

# Top 10 expenses for selected month
top_expenses = (
    filtered_data.nsmallest(10, "Betrag") if len(filtered_data) > 0 else pd.DataFrame()
)
with st.container():
    st.subheader(f"Top 10 Expenses for {selected_month}")
    if len(top_expenses) > 0:
        st.write(
            top_expenses[["Verwendungszweck", "Betrag"]].to_html(index=False),
            unsafe_allow_html=True,
        )
    else:
        st.write("No expenses found for this month.")

# Top 10 incomes for selected month
top_incomes = (
    filtered_data.nlargest(10, "Betrag") if len(filtered_data) > 0 else pd.DataFrame()
)
with st.container():
    st.subheader(f"Top 10 Incomes for {selected_month}")
    if len(top_incomes) > 0:
        st.write(
            top_incomes[["Verwendungszweck", "Betrag"]].to_html(index=False),
            unsafe_allow_html=True,
        )
    else:
        st.write("No income found for this month.")

# Cumulative line chart of the selected month
if len(filtered_data) > 0:
    st.subheader(f"Cumulative Transactions for {selected_month}")
    cumulative_data = filtered_data.copy()  # Copy to avoid modifying original data
    cumulative_data["Running_Total"] = cumulative_data["Betrag"].cumsum()
    st.line_chart(cumulative_data, x="Buchungsdatum", y="Running_Total")

# Daily transactions in the selected month
if len(filtered_data) > 0:
    st.subheader(f"Daily Transactions for {selected_month}")
    daily_data = (
        filtered_data.resample("D", on="Buchungsdatum")
        .agg(Daily_Amount=("Betrag", "sum"))
        .reset_index()
    )
    st.line_chart(daily_data, x="Buchungsdatum", y="Daily_Amount")

# Overall trend line chart
st.subheader("Overall Trend")
st.line_chart(monthly_data, x="Buchungsdatum", y="Total_Amount")
