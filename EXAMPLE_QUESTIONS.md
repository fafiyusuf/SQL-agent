# Example Questions for the Comprehensive Database

This document provides example natural language questions you can ask the SQL agent, organized by topic.

## 📊 Database Overview

**8 Tables:**
- departments (7 records)
- employees (24 records)
- products (20 products)
- customers (25 customers)
- orders (43 orders)
- order_items (104 line items)
- customer_notes (20 notes)
- chat_history (54 messages)

**Total: 297 records**

---

## 👥 Employee & Department Questions

### Basic Queries
- "How many employees work in each department?"
- "List all employees in the Engineering department"
- "Who are the managers?" (employees with no manager_id)
- "Show me all employees hired in 2021"
- "Which department has the most employees?"

### Salary Analysis
- "What is the average salary by department?"
- "Who are the top 5 highest paid employees?"
- "What's the salary range in Engineering?"
- "Show me employees earning more than $100,000"
- "What is the total payroll cost?"

### Department Insights
- "Which department has the largest budget?"
- "What is the total budget across all departments?"
- "List departments with their locations"
- "Show me remote departments"
- "Which departments were created in 2018?"

---

## 🛍️ Product & Inventory Questions

### Product Catalog
- "How many products do we have in each category?"
- "List all products in the Electronics category"
- "What are our top 10 most expensive products?"
- "Show me products under $50"
- "Which products are out of stock?" (stock_quantity = 0)

### Inventory Management
- "Which products have low stock?" (e.g., < 100 units)
- "What's the total value of our inventory?" (price * stock_quantity)
- "Show me products from supplier 'FitGear'"
- "Which products were last updated in November 2024?"
- "What's the average profit margin?" ((price - cost) / price)

### Product Performance
- "Which products have never been ordered?"
- "What are the most popular products?" (based on order_items)
- "Show me products with stock above 400 units"
- "List all active products"
- "What's the price range for each category?"

---

## 🛒 Customer & Orders Questions

### Customer Analysis
- "How many customers do we have by state?"
- "Who are our top 5 customers by total spent?"
- "List customers with loyalty points over 1000"
- "Show me customers who joined in 2024"
- "Which customers haven't purchased recently?" (last_purchase_date)

### Order Analysis
- "How many orders were placed in November 2024?"
- "What's the average order value?"
- "Show me all pending or processing orders"
- "Which payment method is most popular?"
- "What's the total revenue from completed orders?"

### Order Details
- "How many items were in order #5?"
- "Show me orders over $1000"
- "Which orders had free shipping?" (shipping_cost = 0)
- "List orders placed by customer Emma Williams"
- "What's the total tax collected?"

### Complex Joins
- "Which products were purchased by customer Olivia Brown?"
- "Show me the top 3 best-selling products"
- "List customers who bought fitness products"
- "Which employees processed the most customer orders?" (via customer_notes)
- "What's the average number of items per order?"

---

## 📝 Customer Service Questions

### Customer Notes
- "How many customer support tickets are still open?"
- "List all high-priority customer notes"
- "Show me complaints from the last month"
- "Which employees have handled the most customer notes?"
- "What are the most common note types?"

### Chat History
- "How many chat sessions were resolved?"
- "Show me chats with negative sentiment"
- "Which customers have the most chat messages?"
- "List all messages from session CHAT-001"
- "What percentage of chats are resolved?"

### Support Performance
- "Which support agents are most active?" (via customer_notes)
- "Show me recent product inquiries"
- "List all warranty claims"
- "What are the most common customer issues?"
- "How many return requests do we have?"

---

## 💰 Revenue & Financial Questions

### Revenue Analysis
- "What's our total revenue for 2024?"
- "Show me monthly revenue trends" (by order_date)
- "What's the average order value by month?"
- "How much revenue came from Electronics products?"
- "Which state generates the most revenue?"

### Profit Analysis
- "What's our total profit margin?" (based on product cost vs price)
- "Which products are most profitable?"
- "Show me the profit for each product category"
- "What's the cost of goods sold for completed orders?"
- "Calculate profit from order #10"

### Customer Lifetime Value
- "What's the average customer lifetime value?"
- "Which customers have spent over $2000?"
- "Show me customers with only one order"
- "What's the repeat purchase rate?"
- "Who are our most loyal customers?"

---

## 🔗 Advanced Multi-Table Questions

### Customer Journey
- "Show me Emma Williams' complete order history"
- "Which products did customers from California buy most?"
- "List customers who bought both fitness and electronics products"
- "Show me customers with support tickets and their order history"
- "Which customers chatted with support before ordering?"

### Product Insights
- "Which products have the most customer notes/complaints?"
- "Show me products frequently returned" (via customer_notes)
- "What products do Engineering employees buy?" (if applicable)
- "Which products are in the most orders?"
- "List products ordered by high-spending customers"

### Operations
- "How many orders are in each status?"
- "Which products need restocking?" (low stock + high demand)
- "Show me the conversion rate from chat to purchase"
- "What's the average time between customer registration and first order?"
- "Which departments handle the most customer support?"

---

## 📈 Trend & Pattern Questions

### Time-Based Analysis
- "Show me order volume by month in 2024"
- "Which day of the week has the most orders?"
- "What's the trend in customer registrations?"
- "How has average order value changed over time?"
- "Show me employee hire dates by year"

### Seasonal Patterns
- "Which products sell best in Q4?"
- "Compare sales in summer vs winter"
- "Show me holiday season revenue"
- "When do customers contact support most?"
- "What's the busiest month for orders?"

---

## 🎯 Business Intelligence Questions

### Performance Metrics
- "What's our customer retention rate?"
- "Calculate the cart abandonment rate" (if applicable)
- "What's the average items per order?"
- "Show me the support ticket resolution rate"
- "What's our inventory turnover ratio?"

### Competitive Analysis
- "Which product categories are most profitable?"
- "What's the price range for each category?"
- "Show me our pricing compared to cost"
- "Which suppliers provide the most products?"
- "What's the margin on each product category?"

### Growth Opportunities
- "Which states have no customers yet?"
- "What products have high stock but low sales?"
- "Show me customers who haven't ordered in 6 months"
- "Which product categories have the fewest items?"
- "What's the potential revenue from low-stock items?"

---

## 🔍 Specific Scenario Questions

### Customer Service Scenarios
- "Show me all unresolved support tickets"
- "Which customers need follow-up?"
- "List warranty claims in the last 30 days"
- "Show me customers with multiple complaints"
- "Which products have the most technical support questions?"

### Sales Scenarios
- "Who are our VIP customers?" (high spend, many orders)
- "Show me customers ready for upsell" (based on purchase history)
- "List customers with abandoned carts" (chat but no recent order)
- "Which products are frequently bought together?"
- "Show me bulk order inquiries"

### Inventory Scenarios
- "Which products are overstocked?" (high stock, low sales)
- "Show me products that need reordering" (low stock, high sales)
- "List products from suppliers with quality issues" (based on returns)
- "What's the value of slow-moving inventory?"
- "Show me products with negative profit margins"

---

## 💡 Tips for Asking Questions

### Be Specific
✅ Good: "Show me customers who spent over $1000 in 2024"
❌ Vague: "Show me good customers"

### Use Natural Language
✅ Good: "Which products are most popular?"
❌ Too technical: "SELECT product_id, COUNT(*) FROM order_items GROUP BY product_id"

### Combine Conditions
✅ Good: "Show me high-priority open support tickets from last week"
✅ Good: "List customers in California with loyalty points over 1000"

### Ask for Aggregations
✅ Good: "What's the average order value by state?"
✅ Good: "How many products are in each price range?"

### Request Rankings
✅ Good: "Top 10 customers by revenue"
✅ Good: "Most popular products by order count"

---

## 🚀 Try These Now!

**Start with these easy questions:**
1. "How many customers do we have?"
2. "What are our top 5 products by price?"
3. "Show me all orders from November 2024"
4. "Which department has the most employees?"
5. "What's the total revenue from completed orders?"

**Then try intermediate questions:**
1. "Which customers have the most loyalty points?"
2. "Show me products with profit margin over 50%"
3. "What's the average order value by payment method?"
4. "List employees who handle customer support"
5. "Which products are frequently bought together?"

**Challenge yourself with complex questions:**
1. "Show me revenue by product category for Q4 2024"
2. "Which customers bought products from multiple categories?"
3. "What's the correlation between chat interactions and purchases?"
4. "Calculate customer lifetime value for top 10 customers"
5. "Show me product performance by supplier"

---

**Ready to explore your data? Start the agent with:**
```bash
python main.py
```

**Happy querying! 🎉**
