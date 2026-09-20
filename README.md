# Brazilian E-Commerce SQL Analytics & Business Intelligence Platform

A professional end-to-end data analytics project built using the **Olist Brazilian E-Commerce Public Dataset**.

The project demonstrates how raw e-commerce CSV data can be transformed into a relational SQLite database, analyzed with SQL, visualized with Python and Plotly, and presented through an interactive Streamlit business intelligence dashboard.

---

## 1. Project Overview

### Project Title

**Brazilian E-Commerce SQL Analytics & Business Intelligence Platform**

### Objective

The primary objective of this project is to demonstrate practical database querying and business intelligence skills using a real-world e-commerce dataset.

The project covers:

* Relational database design
* CSV data ingestion
* ETL processing
* SQLite database creation
* SQL querying
* Filtering with `WHERE`
* Aggregation with `GROUP BY`
* Sorting with `ORDER BY`
* Multi-table analysis with `JOIN`
* SQL views
* Business KPI analysis
* Customer analytics
* Product analytics
* Seller analytics
* Payment analysis
* Review analysis
* Data visualization
* Interactive dashboard development
* Automated analytical outputs
* Professional project documentation

---

## 2. Technology Stack

| Technology | Purpose                         |
| ---------- | ------------------------------- |
| Python     | Data processing and automation  |
| Pandas     | Data manipulation               |
| SQLite     | Relational database             |
| SQL        | Database querying and analytics |
| Plotly     | Interactive visualization       |
| Streamlit  | Business intelligence dashboard |
| Markdown   | Documentation                   |
| Git        | Version control                 |
| GitHub     | Project hosting                 |

---

## 3. Project Architecture

The project follows an end-to-end analytics architecture:

```text
                    ┌──────────────────────────┐
                    │   Olist CSV Dataset      │
                    │       Raw Data           │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │       Python ETL         │
                    │  01_load_database.py     │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │      SQLite Database     │
                    │   olist_ecommerce.db     │
                    └────────────┬─────────────┘
                                 │
                 ┌───────────────┼────────────────┐
                 │               │                │
                 ▼               ▼                ▼
        ┌────────────────┐ ┌──────────────┐ ┌───────────────┐
        │ Basic SQL      │ │ Aggregation  │ │ JOIN Analysis │
        │ Queries        │ │ Queries      │ │ Queries       │
        └───────┬────────┘ └──────┬───────┘ └───────┬───────┘
                │                 │                 │
                └─────────────────┼─────────────────┘
                                  ▼
                    ┌──────────────────────────┐
                    │ Business SQL Analytics   │
                    │       SQL Views          │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ Python Analytics          │
                    │ Pandas + SQL              │
                    └────────────┬─────────────┘
                                 │
                    ┌────────────┴─────────────┐
                    ▼                          ▼
          ┌──────────────────┐       ┌──────────────────┐
          │ Plotly Charts    │       │ Streamlit BI     │
          │ Static Outputs   │       │ Dashboard        │
          └──────────────────┘       └──────────────────┘
```

---

## 4. Dataset

### Olist Brazilian E-Commerce Public Dataset

This project uses the **Brazilian E-Commerce Public Dataset by Olist**.

The dataset contains approximately 100,000 orders from a Brazilian e-commerce marketplace and provides information about orders, customers, products, sellers, payments, reviews, freight, and locations.

Official Kaggle dataset:

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Download the dataset from Kaggle and extract the CSV files into:

```text
data/raw/
```

---

## 5. Dataset Tables

The project works with the following relational tables:

```text
customers
orders
order_items
order_payments
order_reviews
products
sellers
geolocation
product_category_translation
```

### Customers

Contains customer information.

Important fields include:

```text
customer_id
customer_unique_id
customer_zip_code_prefix
customer_city
customer_state
```

---

### Orders

Contains order-level information.

Important fields include:

```text
order_id
customer_id
order_status
order_purchase_timestamp
order_approved_at
order_delivered_carrier_date
order_delivered_customer_date
order_estimated_delivery_date
```

---

### Order Items

Contains individual products purchased within orders.

Important fields include:

```text
order_id
order_item_id
product_id
seller_id
shipping_limit_date
price
freight_value
```

---

### Order Payments

Contains payment information.

Important fields include:

```text
order_id
payment_sequential
payment_type
payment_installments
payment_value
```

---

### Order Reviews

Contains customer review information.

Important fields include:

```text
review_id
order_id
review_score
review_comment_title
review_comment_message
review_creation_date
review_answer_timestamp
```

---

### Products

Contains product-level information.

Important fields include:

```text
product_id
product_category_name
product_name_lenght
product_description_lenght
product_photos_qty
product_weight_g
product_length_cm
product_height_cm
product_width_cm
```

---

### Sellers

Contains seller information.

Important fields include:

```text
seller_id
seller_zip_code_prefix
seller_city
seller_state
```

---

### Geolocation

Contains Brazilian postal-code geographic information.

Important fields include:

```text
geolocation_zip_code_prefix
geolocation_lat
geolocation_lng
geolocation_city
geolocation_state
```

---

### Product Category Translation

Maps Portuguese product category names to English.

Important fields include:

```text
product_category_name
product_category_name_english
```

---

## 6. Project Structure

```text
olist_sql_analytics/
│
├── data/
│   ├── raw/
│   │   ├── olist_customers_dataset.csv
│   │   ├── olist_orders_dataset.csv
│   │   ├── olist_order_items_dataset.csv
│   │   ├── olist_order_payments_dataset.csv
│   │   ├── olist_order_reviews_dataset.csv
│   │   ├── olist_products_dataset.csv
│   │   ├── olist_sellers_dataset.csv
│   │   ├── olist_geolocation_dataset.csv
│   │   └── product_category_name_translation.csv
│   │
│   └── processed/
│
├── database/
│   └── olist_ecommerce.db
│
├── sql/
│   ├── 01_basic_queries.sql
│   ├── 02_aggregation_queries.sql
│   ├── 03_join_queries.sql
│   ├── 04_business_analysis.sql
│   └── 05_views.sql
│
├── src/
│   ├── 01_load_database.py
│   ├── 02_run_sql_analysis.py
│   ├── 03_create_visualizations.py
│   └── 04_generate_report.py
│
├── dashboard/
│   └── app.py
│
├── outputs/
│   ├── charts/
│   ├── csv/
│   └── reports/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 7. Installation

### Step 1 — Clone the Repository

If the project is hosted on GitHub:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd olist_sql_analytics
```

---

### Step 2 — Create a Virtual Environment

#### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

#### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 8. Install Dependencies

Run:

```bash
pip install -r requirements.txt
```

The required Python libraries are defined in:

```text
requirements.txt
```

---

## 9. Download the Dataset

Download the Olist dataset from Kaggle:

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Extract the CSV files into:

```text
data/raw/
```

The folder should contain:

```text
data/raw/
├── olist_customers_dataset.csv
├── olist_orders_dataset.csv
├── olist_order_items_dataset.csv
├── olist_order_payments_dataset.csv
├── olist_order_reviews_dataset.csv
├── olist_products_dataset.csv
├── olist_sellers_dataset.csv
├── olist_geolocation_dataset.csv
└── product_category_name_translation.csv
```

---

## 10. Build the SQLite Database

Run:

```bash
python src/01_load_database.py
```

This script:

1. Locates the raw CSV files.
2. Loads the datasets using Pandas.
3. Performs basic data preparation.
4. Creates the SQLite database.
5. Creates the relational tables.
6. Loads the CSV data into SQLite.
7. Creates the required database structure.

The resulting database will be:

```text
database/olist_ecommerce.db
```

---

## 11. Run SQL Analysis

The SQL analysis is separated into multiple files so that each SQL concept can be studied independently.

### Basic Queries

```text
sql/01_basic_queries.sql
```

Covers:

```sql
SELECT
WHERE
ORDER BY
LIMIT
DISTINCT
```

---

### Aggregation Queries

```text
sql/02_aggregation_queries.sql
```

Covers:

```sql
COUNT()
SUM()
AVG()
MIN()
MAX()
GROUP BY
HAVING
```

---

### JOIN Queries

```text
sql/03_join_queries.sql
```

Covers relationships between:

```text
customers
orders
order_items
products
sellers
payments
reviews
```

---

### Business Analysis

```text
sql/04_business_analysis.sql
```

Contains business-oriented analytical queries such as:

* Revenue analysis
* Top-selling products
* Top categories
* Top sellers
* Monthly revenue
* Average order value
* Customer-state performance
* Payment analysis
* Review performance
* Delivery performance

---

### SQL Views

```text
sql/05_views.sql
```

Creates reusable analytical views that simplify downstream analysis.

---

## 12. Run the SQL Analysis Script

Run:

```bash
python src/02_run_sql_analysis.py
```

The script executes the analytical SQL queries and exports the results into:

```text
outputs/csv/
```

These CSV files can then be used by Python visualization and reporting workflows.

---

## 13. Generate Professional Visualizations

Run:

```bash
python src/03_create_visualizations.py
```

The visualization script uses:

```text
Python
Pandas
Plotly
SQLite
```

and generates professional interactive charts.

Charts are saved under:

```text
outputs/charts/
```

Expected analytical visualizations include:

* Monthly revenue trend
* Monthly order volume
* Top product categories
* Top products
* Top sellers
* Revenue by customer state
* Payment method distribution
* Review score distribution
* Order status distribution
* Freight/revenue analysis

---

## 14. Launch the Interactive Dashboard

Run:

```bash
streamlit run dashboard/app.py
```

The Streamlit dashboard provides multiple analytical sections.

---

## 15. Dashboard Sections

### Executive Overview

The executive dashboard provides high-level KPIs such as:

* Total orders
* Total customers
* Total products
* Total sellers
* Total sales
* Average item price

It also includes:

* Monthly revenue trend
* Top product categories
* Order-status distribution

---

### Sales Performance

Provides:

* Monthly revenue
* Monthly order volume
* Payment-type analysis
* Payment value
* Average payment
* Payment transaction distribution

---

### Product Analytics

Provides:

* Top products by revenue
* Product category performance
* Units sold
* Number of orders
* Average product price
* Revenue by category

---

### Customer Analytics

Provides:

* Customers by state
* Orders by state
* Revenue by state
* Average order value
* Customer base versus revenue

---

### Seller Analytics

Provides:

* Top sellers
* Seller revenue
* Items sold
* Seller order volume
* Seller performance by state

---

### Reviews & Payments

Provides:

* Review-score distribution
* Average review score
* Number of reviews
* Payment installments
* Payment value by installment count

---

### Data Explorer

The Data Explorer allows users to:

* Inspect database tables
* Preview table records
* Count table rows
* Download table previews
* Execute read-only SQL queries
* Download SQL query results

Only analytical `SELECT` and `WITH` queries are permitted through the dashboard query interface.

---

## 16. Example Business Questions

This project can answer questions such as:

### Sales

1. What is the total revenue?
2. How many orders were placed?
3. Which months generated the highest revenue?
4. What is the average order value?
5. Which states generate the most revenue?

### Products

6. Which products generate the most revenue?
7. Which categories sell the most units?
8. Which categories generate the highest revenue?
9. What is the average product price?

### Sellers

10. Which sellers generate the most revenue?
11. Which seller states have the highest sales?
12. Which sellers process the most orders?

### Customers

13. Which states have the most customers?
14. Which states have the highest customer revenue?
15. How does customer volume relate to revenue?

### Payments

16. Which payment methods are most commonly used?
17. Which payment method generates the highest payment value?
18. What is the average payment value?
19. Which installment counts are most common?

### Reviews

20. What is the average customer review score?
21. What percentage of reviews are positive?
22. How are review scores distributed?

### Operations

23. How many orders are delivered?
24. How many orders are canceled?
25. How long does delivery take?
26. How does freight value compare with product price?

---

## 17. Key SQL Concepts Demonstrated

The project demonstrates practical SQL concepts including:

```sql
SELECT
FROM
WHERE
DISTINCT
ORDER BY
LIMIT
GROUP BY
HAVING
COUNT
SUM
AVG
MIN
MAX
CASE
COALESCE
NULLIF
INNER JOIN
LEFT JOIN
CTE
WINDOW FUNCTIONS
DATE/TIME FUNCTIONS
CREATE VIEW
```

These concepts provide a strong foundation for relational database analytics.

---

## 18. Data Relationships

The central relationship is based around orders.

```text
customers
    │
    │ customer_id
    ▼
orders
    │
    ├──────────────► order_payments
    │                 order_id
    │
    ├──────────────► order_reviews
    │                 order_id
    │
    ▼
order_items
    │
    ├──────────────► products
    │                 product_id
    │
    └──────────────► sellers
                      seller_id
```

Products can additionally be connected to:

```text
product_category_translation
```

using:

```text
product_category_name
```

---

## 19. Important Analytical Considerations

### Order-Level vs Item-Level Revenue

An order can contain multiple products.

Therefore, revenue calculated from:

```text
order_items.price
```

is an item-level aggregation.

It should not be interpreted as the number of unique orders.

For order counts, use:

```sql
COUNT(DISTINCT order_id)
```

when joining orders with order items.

---

### Freight Value

The `freight_value` column represents freight/shipping value associated with order items.

Revenue and freight should therefore be analyzed separately unless a specific business definition requires combining them.

---

### Multiple Payment Records

An order can have multiple payment records.

When combining payments with order items, careless joins can duplicate values.

Analytical queries should therefore consider the grain of each table before aggregating.

---

### Multiple Order Items

One order can contain multiple order items.

Therefore:

```sql
COUNT(order_id)
```

after joining to `order_items` can overcount orders.

Use:

```sql
COUNT(DISTINCT order_id)
```

when calculating unique orders.

---

## 20. Data Quality

The project should consider:

* Missing values
* Duplicate records
* Null timestamps
* Unknown product categories
* Orders without associated items
* Multiple payments per order
* Multiple review records
* Geographic inconsistencies
* Product-category translation gaps

The ETL and analytical SQL layers should preserve the original information while handling missing values appropriately.

---

## 21. Reproducibility

To reproduce the project:

### Windows

```bash
git clone YOUR_GITHUB_REPOSITORY_URL

cd olist_sql_analytics

python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt

python src/01_load_database.py

python src/02_run_sql_analysis.py

python src/03_create_visualizations.py

streamlit run dashboard/app.py
```

### macOS/Linux

```bash
git clone YOUR_GITHUB_REPOSITORY_URL

cd olist_sql_analytics

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

python src/01_load_database.py

python src/02_run_sql_analysis.py

python src/03_create_visualizations.py

streamlit run dashboard/app.py
```

---

## 22. Outputs

The project generates:

```text
outputs/
├── charts/
│   ├── monthly_revenue.html
│   ├── top_categories.html
│   ├── top_products.html
│   ├── top_sellers.html
│   ├── customer_state_revenue.html
│   ├── payment_analysis.html
│   └── review_analysis.html
│
├── csv/
│   ├── SQL query results
│   ├── product analysis
│   ├── customer analysis
│   ├── seller analysis
│   └── dashboard datasets
│
└── reports/
    └── analytical reports
```

Actual filenames may vary depending on the SQL and visualization scripts.

---

## 23. GitHub Recommendations

Before pushing the project to GitHub, do not commit:

```text
.venv/
__pycache__/
*.pyc
database/*.db
large raw CSV datasets
temporary files
```

The `.gitignore` file should exclude generated and environment-specific files.

The README should remain committed because it provides the project's documentation and setup instructions.

---

## 24. Suggested Git Workflow

Initialize Git:

```bash
git init
```

Add project files:

```bash
git add .
```

Create the first commit:

```bash
git commit -m "Initial Brazilian e-commerce SQL analytics project"
```

Create or connect a GitHub repository and then push the project.

---

## 25. Recommended GitHub Repository Description

Use:

```text
End-to-end Brazilian e-commerce analytics platform using SQLite, SQL, Python, Pandas, Plotly, and Streamlit.
```

---

## 26. Portfolio Description

A concise portfolio description:

> Built an end-to-end Brazilian e-commerce business intelligence platform using the Olist public dataset. Designed a SQLite relational database, developed analytical SQL queries and views, automated analysis with Python/Pandas, created interactive Plotly visualizations, and developed a Streamlit dashboard for sales, product, customer, seller, payment, and review analytics.

---

## 27. Skills Demonstrated

This project demonstrates practical experience in:

### Database

* Relational database concepts
* SQLite
* Database normalization concepts
* Table relationships
* Primary/foreign-key relationships
* Data loading

### SQL

* Data extraction
* Filtering
* Aggregation
* Grouping
* Sorting
* Joins
* CTEs
* Window functions
* Views
* Business analytics

### Python

* Pandas
* SQLite integration
* Automation
* Data transformation
* File management

### Visualization

* Plotly
* Interactive charts
* KPI design
* Business dashboards
* Professional color systems

### BI

* Executive KPIs
* Sales analysis
* Customer segmentation
* Product performance
* Seller performance
* Payment analysis
* Customer satisfaction

### Software Engineering

* Project organization
* Reusable scripts
* Modular architecture
* Git/GitHub readiness
* Reproducible execution

---

## 28. Future Improvements

Potential future enhancements include:

1. Add automated data validation.
2. Add a data-quality report.
3. Add delivery-time KPIs.
4. Add customer retention analysis.
5. Add repeat-customer analysis.
6. Add cohort analysis.
7. Add RFM customer segmentation.
8. Add geographic visualization.
9. Add advanced seller performance scoring.
10. Add automated PDF/DOCX reporting.
11. Add scheduled ETL execution.
12. Add CI/CD validation with GitHub Actions.
13. Add unit tests.
14. Add database indexes for performance.
15. Deploy the Streamlit dashboard.

---

## 29. Project Completion Checklist

Before considering the project complete, verify:

* [ ] Dataset downloaded
* [ ] Raw CSV files placed in `data/raw/`
* [ ] SQLite database successfully created
* [ ] All expected tables loaded
* [ ] Basic SQL queries executed
* [ ] Aggregation queries executed
* [ ] JOIN queries executed
* [ ] Business-analysis queries executed
* [ ] SQL views created
* [ ] SQL results exported
* [ ] Plotly visualizations generated
* [ ] Streamlit dashboard launched
* [ ] Dashboard KPIs verified
* [ ] Dashboard charts verified
* [ ] CSV downloads tested
* [ ] SQL Explorer tested
* [ ] Documentation completed
* [ ] `.gitignore` configured
* [ ] Git repository initialized
* [ ] Project tested from a clean environment

---

## 30. Final Project Workflow

The completed system follows this workflow:

```text
        Olist Dataset
             │
             ▼
        Raw CSV Files
             │
             ▼
       Python ETL Process
             │
             ▼
      SQLite Relational DB
             │
             ▼
       SQL Query Layer
             │
       ┌─────┼─────┐
       ▼     ▼     ▼
     Basic  JOIN  Business
     SQL    SQL    Analytics
       │     │     │
       └─────┼─────┘
             ▼
        SQL Views
             │
             ▼
       Python + Pandas
             │
       ┌─────┴─────┐
       ▼           ▼
     Plotly     Streamlit
    Charts      Dashboard
       │           │
       └─────┬─────┘
             ▼
     Business Insights
```

---

## 31. Conclusion

The **Brazilian E-Commerce SQL Analytics & Business Intelligence Platform** demonstrates a complete data analytics workflow from raw data ingestion through database querying, business analysis, visualization, and interactive reporting.

The project is designed to demonstrate not only individual SQL commands but also how SQL fits into a realistic analytics pipeline.

The final platform combines:

```text
SQLite
+
SQL
+
Python
+
Pandas
+
Plotly
+
Streamlit
```

to transform raw e-commerce data into actionable business intelligence.

---

## Dataset Attribution

Data source:

**Olist Brazilian E-Commerce Public Dataset**

Kaggle:

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

The dataset should be used according to its original licensing and attribution requirements.
