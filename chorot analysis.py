import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("cleaned_customer_purchase_history.csv")

# Convert PurchaseDate to datetime
df["PurchaseDate"] = pd.to_datetime(df["PurchaseDate"], dayfirst=True)

# Create Purchase Month
df["PurchaseMonth"] = df["PurchaseDate"].dt.to_period("M")

# Find first purchase (Cohort Month)
df["CohortMonth"] = df.groupby("CustomerID")["PurchaseMonth"].transform("min")

# Calculate Cohort Index (months since first purchase)
df["CohortIndex"] = (df["PurchaseMonth"] - df["CohortMonth"]).apply(lambda x: x.n)

# Create cohort table
cohort_data = df.groupby(["CohortMonth", "CohortIndex"])["CustomerID"].nunique()

cohort_table = cohort_data.reset_index().pivot(
    index="CohortMonth",
    columns="CohortIndex",
    values="CustomerID"
)

print("\nCohort Table:\n")
print(cohort_table)

# Plot heatmap
plt.figure(figsize=(10,6))
sns.heatmap(cohort_table, annot=True, fmt=".0f", cmap="YlGnBu")

plt.title("Customer Retention Cohort Analysis")
plt.xlabel("Months Since First Purchase")
plt.ylabel("Cohort Month")

plt.show()