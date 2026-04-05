# 📊 SalesPulse — Sales Data Dashboard

> A full-stack Sales Analytics web app built with **Python Flask**, **Pandas**, **NumPy**, **MySQL**, **Bootstrap**, and **Chart.js**.

---

## ✨ Features

- 📁 Upload CSV or Excel sales files
- 🧹 Auto data cleaning using Pandas
- 📊 6 interactive Chart.js charts
- 💰 KPI cards — Total Revenue, Orders, Avg Order Value, Units Sold
- 📈 Monthly & daily revenue trends
- 🥧 Revenue breakdown by category (Doughnut chart)
- 🌍 Revenue by region (Bar chart)
- 🏆 Top 5 products by revenue (Horizontal bar)
- ⚡ NumPy-powered aggregations

---

## 🛠️ Tech Stack

| Layer    | Technology                        |
|----------|-----------------------------------|
| Backend  | Python 3, Flask                   |
| Data     | Pandas, NumPy                     |
| Database | MySQL                             |
| Frontend | HTML, CSS, Bootstrap 5, Chart.js  |

---

## 📁 Project Structure

```
sales_dashboard/
├── app.py                  # Flask app — routes & Pandas logic
├── schema.sql              # MySQL schema
├── requirements.txt        # Python dependencies
├── sample_data.csv         # Sample data to test with
├── README.md
└── templates/
    ├── index.html          # Upload page
    └── dashboard.html      # Analytics dashboard
```

---

## ⚙️ Setup Instructions

### Step 1 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Set up MySQL database
```bash
mysql -u root -p < schema.sql
```

### Step 3 — Update DB credentials in app.py
```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",  # ← change this
    "database": "sales_dashboard"
}
```

### Step 4 — Run the app
```bash
python app.py
```

### Step 5 — Open in browser
```
http://localhost:5000
```

---

## 🚀 How to Use

1. Go to `http://localhost:5000`
2. Upload the included `sample_data.csv` file
3. Click **View Dashboard** to see all charts and KPIs

---

## 📋 CSV Format Required

Your CSV/Excel file must have these columns:

| Column     | Example        |
|------------|----------------|
| date       | 2024-01-15     |
| product    | Laptop Pro     |
| category   | Electronics    |
| quantity   | 10             |
| price      | 75000          |
| region     | North          |

---

## 🐛 Common Errors

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `Access denied` | Fix MySQL password in `app.py` |
| `Missing columns` | Check your CSV has all 6 required columns |
| Port in use | Change `app.run(port=5001)` in `app.py` |
