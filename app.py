from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import mysql.connector
import os
from werkzeug.utils import secure_filename
import datetime

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

# ── DB CONFIG ──────────────────────────────────────────────
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",   
    "database": "sales_dashboard"
}

@app.route('/test-db')
def test_db():
    try:
        db = get_db()
        return "DB Connected ✅"
    except Exception as e:
        return str(e)
def get_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        print(f"DB CONNECTION ERROR: {e}")
        raise

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ── ROUTES ─────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Only CSV, XLSX, XLS files allowed'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)

        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

        required = ['date', 'product', 'category', 'quantity', 'price', 'region']
        missing = [col for col in required if col not in df.columns]
        if missing:
            return jsonify({'error': f'Missing columns: {", ".join(missing)}'}), 400

        # TEST — skip MySQL, just return success
        return jsonify({'success': True, 'rows': len(df)})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/summary')
def api_summary():
    try:
        # Read directly from uploaded file instead of MySQL
        upload_folder = app.config['UPLOAD_FOLDER']
        files = [f for f in os.listdir(upload_folder) if f.endswith(('.csv', '.xlsx', '.xls'))]
        if not files:
            return jsonify({'error': 'No data found'}), 404

        latest_file = os.path.join(upload_folder, files[-1])
        if latest_file.endswith('.csv'):
            df = pd.read_csv(latest_file)
        else:
            df = pd.read_excel(latest_file)

        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        df['date'] = pd.to_datetime(df['date'])
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0)
        df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0)
        df['revenue'] = df['quantity'] * df['price']

        total_revenue   = float(np.sum(df['revenue'].values))
        total_orders    = int(len(df))
        avg_order_value = float(np.mean(df['revenue'].values))
        total_units     = int(np.sum(df['quantity'].values))

        df['month'] = df['date'].dt.to_period('M').astype(str)
        monthly = df.groupby('month')['revenue'].sum().reset_index().sort_values('month')
        by_category = df.groupby('category')['revenue'].sum().reset_index().sort_values('revenue', ascending=False)
        by_region = df.groupby('region')['revenue'].sum().reset_index().sort_values('revenue', ascending=False)
        top_products = df.groupby('product')['revenue'].sum().reset_index().sort_values('revenue', ascending=False).head(5)
        units_by_cat = df.groupby('category')['quantity'].sum().reset_index()
        daily = df.groupby(df['date'].dt.date)['revenue'].sum().reset_index()
        daily.columns = ['date', 'revenue']
        daily['date'] = daily['date'].astype(str)
        daily = daily.sort_values('date')

        return jsonify({
            'kpis': {
                'total_revenue': round(total_revenue, 2),
                'total_orders': total_orders,
                'avg_order_value': round(avg_order_value, 2),
                'total_units': total_units
            },
            'monthly_revenue': {'labels': monthly['month'].tolist(), 'values': [round(v,2) for v in monthly['revenue'].tolist()]},
            'by_category': {'labels': by_category['category'].tolist(), 'values': [round(v,2) for v in by_category['revenue'].tolist()]},
            'by_region': {'labels': by_region['region'].tolist(), 'values': [round(v,2) for v in by_region['revenue'].tolist()]},
            'top_products': {'labels': top_products['product'].tolist(), 'values': [round(v,2) for v in top_products['revenue'].tolist()]},
            'units_by_category': {'labels': units_by_cat['category'].tolist(), 'values': units_by_cat['quantity'].tolist()},
            'daily_trend': {'labels': daily['date'].tolist(), 'values': [round(v,2) for v in daily['revenue'].tolist()]}
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)
