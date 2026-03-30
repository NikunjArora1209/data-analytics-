select * from supplychain;
SELECT 
    `Delivery Status`, 
    COUNT(`Order Id`) AS Total_Orders,
    ROUND(COUNT(`Order Id`) * 100.0 / SUM(COUNT(`Order Id`)) OVER(), 2) AS Percentage
FROM supplychain 
group by  `Delivery Status`
ORDER BY Total_Orders DESC;
SELECT 
    `Product Name`, 
    `Category Name`,
    SUM(`Order Item Quantity`) AS Total_Quantity_Dispatched,
    COUNT(DISTINCT `Order Id`) AS Unique_Orders
From supplychain
WHERE `Order Status` != 'CANCELED'
GROUP BY `Product Name`, `Category Name`
ORDER BY Total_Quantity_Dispatched DESC;
SELECT 
    `Order Id`,
    `Order City`,
    `Order Country`,
    `Shipping Mode`,
    `Days for shipping (real)` AS ATA,
    `Days for shipment (scheduled)` AS ETA,
    (`Days for shipping (real)` - `Days for shipment (scheduled)`) AS Delivery_Variance,
    CASE 
        WHEN `Days for shipping (real)` > `Days for shipment (scheduled)` THEN 'Late'
        WHEN `Days for shipping (real)` < `Days for shipment (scheduled)` THEN 'Early'
        ELSE 'On-Time'
    END AS Efficiency_Label
FROM supplychain
WHERE `Delivery Status` != 'Shipping canceled'
ORDER BY Delivery_Variance DESC;
SELECT 
    `Delivery Status`, 
    COUNT(`Order Id`) AS Total_Orders
FROM supplychain
GROUP BY `Delivery Status`;
