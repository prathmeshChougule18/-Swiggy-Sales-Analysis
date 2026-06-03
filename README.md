# 🍕 Swiggy Sales Analysis

An exploratory data analysis project on Swiggy order data to uncover sales trends, customer preferences, and performance insights across cities and states in India.

---

## 📁 Project Structure

```
swiggy-sales-analysis/
├── Swiggy_Sales_Analysis.ipynb   ← Main analysis notebook
├── swiggy_data.csv               ← Dataset
└── README.md
```

---

## 📊 Dataset Overview

| Column | Description |
|---|---|
| `State` | State where order was placed |
| `City` | City of the order |
| `Order Date` | Date of the order |
| `Restaurant Name` | Name of the restaurant |
| `Location` | Restaurant location |
| `Category` | Food category |
| `Dish Name` | Name of the dish ordered |
| `Price (INR)` | Order price in Indian Rupees |
| `Rating` | Restaurant rating |
| `Rating Count` | Number of ratings |

---

## 🔍 Analysis Performed

### 📌 KPIs Calculated
- **Total Sales (INR)** — Overall revenue generated
- **Average Rating** — Mean restaurant rating across all orders
- **Average Order Value** — Mean spend per order
- **Total Rating Count** — Cumulative customer ratings
- **Total Orders** — Overall order volume

### 📈 Charts & Visualizations

| Analysis | Insight |
|---|---|
| Monthly Sales Trend | Revenue pattern across months using line chart |
| Daily Sales Trend | Revenue breakdown by day of week (Mon–Sun) |
| Veg vs Non-Veg Revenue | Donut chart comparing revenue contribution |
| Revenue by State | Horizontal bar chart — top performing states |
| Quarterly Performance Summary | Quarter-wise Total Sales, Avg Rating & Orders |
| Top 5 Cities by Sales | Highest revenue generating cities |

---

## 💡 Key Highlights

- Classified dishes into **Veg / Non-Veg** using keyword matching on dish names
- Analyzed **seasonal and weekly order patterns** to identify peak days
- Compared **state-wise and city-wise performance** to find top markets
- Generated **quarterly summaries** combining sales, ratings, and order counts

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| `Python 3` | Core language |
| `Pandas` | Data manipulation & aggregation |
| `NumPy` | Numerical operations |
| `Matplotlib` | Static charts |
| `Seaborn` | Statistical visualizations |
| `Plotly Express` | Interactive charts (pie, bar) |

---

## ⚙️ How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/prathmeshChougule18/swiggy-sales-analysis.git
   cd swiggy-sales-analysis
   ```

2. **Install dependencies**
   ```bash
   pip install pandas numpy matplotlib seaborn plotly
   ```

3. **Run the notebook**
   ```
   Open Swiggy_Sales_Analysis.ipynb in Jupyter Notebook and run all cells
   ```

---

## 👨‍💻 Author

**Prathamesh Chougule**
- GitHub: [@prathmeshChougule18](https://github.com/prathmeshChougule18)
- LinkedIn: [prathmesh-chougule](https://www.linkedin.com/in/prathmesh-chougule-7b8733219/)

---

© 2026 Prathamesh Chougule · All Rights Reserved
