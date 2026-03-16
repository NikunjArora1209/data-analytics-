use consumer360;
select*from purchase;
CREATE or replace  VIEW rfm_base AS
SELECT 
    CustomerID,
    CustomerName,
   
    DATEDIFF((SELECT MAX(PurchaseDate) FROM purchase), MAX(PurchaseDate)) AS recency,
   
    COUNT(*) AS frequency,
    
    SUM(TotalPrice) AS monetary
FROM purchase
GROUP BY CustomerID, CustomerName;
CREATE  or replace VIEW customer_segmentation AS
SELECT *,
    CASE 
        WHEN recency <= 30 AND frequency >= 5 THEN 'Champion'
        WHEN recency <= 90 AND frequency >= 3 THEN 'Loyal Customer'
        WHEN recency > 180 AND monetary > 2000 THEN 'At Risk (High Value)'
        WHEN recency > 365 THEN 'Churned/Lost'
        ELSE 'Potential/Standard'
    END AS segment_label
FROM rfm_base;
SELECT 
    segment_label, 
    COUNT(CustomerID) AS total_customers, 
    ROUND(SUM(monetary), 2) AS total_revenue,
    ROUND(AVG(recency), 0) AS avg_days_since_last_purchase
FROM customer_segmentation
GROUP BY segment_label
ORDER BY total_revenue DESC;
select*from purchase;
select customerid,customername, 
NTILE (5)over(order by MAX(purchasedate) asc) as recency_rank,
ntile(5)over(order by count(*) asc )as frequency_rank,
ntile(5)over(order by sum(totalprice) asc)as monetary_rank
from consumer360.purchase
group by customerid,customername;
select product,
sum(quantity) as total_volume,
round(sum(totalprice),2)as total_revenue, 
rank () over(order by sum(totalprice) desc)as revenue_rank
from consumer360.purchase 
group by product
order by total_revenue desc;



