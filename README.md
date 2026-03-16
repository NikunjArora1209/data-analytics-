This project focuses on building an automated Customer 360 engine using SQL and python. By analyzing 1,800+ purchase records, we developed a system that sanitizes raw transaction data and categorizes customers using RFM (Recency, Frequency, Monetary) analysis. This allows businesses to identify high-value "Champions" and proactively target "At-Risk" customers.
RFM Engine (Analytical Layer)
I created SQL Views to calculate core performance metrics for every customer:

Recency: Days since the customer's last purchase.

Frequency: Total number of unique transactions.

Monetary: Total Lifetime Value (LTV) calculated as Quantity * UnitPrice.

 Segmentation (The "Consumer360" Brain)
Using a CASE statement logic, customers are automatically labeled:

Champions: Recent shoppers with high frequency.

At-Risk (High Value): Customers who spent heavily in the past but haven't returned in 90+ days.

Churned: Customers with no activity for over 1 year.

 Key Insights
Data Volume: Analyzed 1,800 rows of customer purchase history.

Data Schema: Managed 10 distinct columns including PurchaseDate, PaymentMethod, and ReviewRating.

Business Impact: The engine identifies specific CustomerIDs that require immediate marketing intervention to prevent churn.
