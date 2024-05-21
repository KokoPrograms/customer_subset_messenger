# Default subset criteria
default_subset_criteria = "spent more than $200 in the last 6 months"

# Default SQL query
default_sql_query = """
SELECT c.CustomerID, c.Name, c.Phone, SUM(o.TotalAmount) as TotalAmount, MAX(o.OrderDate) as LastOrderDate
FROM Orders o
JOIN Customers c ON o.CustomerID = c.CustomerID
WHERE o.OrderDate >= DATE('now', '-6 months') AND o.TotalAmount > 200
GROUP BY c.CustomerID
ORDER BY TotalAmount DESC;
"""

# Default SQL query explanation
default_sql_explanation = "Customers who spent more than $200 in the last 6 months, ordered by the total amount spent."

# Default promotion information
default_promotion_info = "additional 10% off during happy hour 4-6pm through the end of the month"

# Default promotional message template
default_promotion_message_template = "🍻✨ Enjoy an extra 10% discount during our happy hour from 4-6 PM, available every day until the end of this month! 🎉"
