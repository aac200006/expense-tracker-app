import csv
import uuid
from datetime import datetime, timedelta
from collections import defaultdict
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file, make_response
import os
import io

# PDF functionality temporarily removed for stability

app = Flask(__name__)

# CSV File to store expense transactions
FILE_NAME = "expenses.csv"

# ----------------------------- Transaction Classes -----------------------------

class Transaction:
    def __init__(self, expense_name, amount, date, category):
        self.transaction_id = str(uuid.uuid4())
        self.expense_name = expense_name
        self.amount = float(amount)
        self.date = date  # Format: YYYY-MM-DD
        self.category = category

    def to_dict(self):
        return {
            "ID": self.transaction_id,
            "Name": self.expense_name,
            "Amount": self.amount,
            "Date": self.date,
            "Category": self.category,
        }

    def modify(self, name=None, amount=None, date=None, category=None):
        if name: self.expense_name = name
        if amount: self.amount = float(amount)
        if date: self.date = date
        if category: self.category = category


class FoodTransaction(Transaction):
    def __init__(self, expense_name, amount, date, meal_type, location):
        super().__init__(expense_name, amount, date, "Food")
        self.meal_type = meal_type
        self.location = location

    def to_dict(self):
        data = super().to_dict()
        data.update({"MealType": self.meal_type, "Location": self.location})
        return data


class TravelTransaction(Transaction):
    def __init__(self, expense_name, amount, date, transport_mode, destination):
        super().__init__(expense_name, amount, date, "Travel")
        self.transport_mode = transport_mode
        self.destination = destination

    def to_dict(self):
        data = super().to_dict()
        data.update({"TransportMode": self.transport_mode, "Destination": self.destination})
        return data


# ----------------------------- Utility Functions -----------------------------

def save_transaction(transaction):
    header_exists = os.path.exists(FILE_NAME) and os.path.getsize(FILE_NAME) > 0
    
    with open(FILE_NAME, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=transaction.to_dict().keys())
        if not header_exists:
            writer.writeheader()
        writer.writerow(transaction.to_dict())


def load_transactions():
    transactions = []
    try:
        # Check if file exists, if not create it
        if not os.path.exists(FILE_NAME):
            # Create empty CSV file with headers
            with open(FILE_NAME, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['ID', 'Name', 'Amount', 'Date', 'Category'])
                writer.writeheader()
            return transactions
            
        with open(FILE_NAME, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Skip empty rows
                if row and any(row.values()):
                    transactions.append(row)
    except Exception as e:
        print(f"Error loading transactions: {e}")
        # Create empty CSV file with headers if there's any error
        try:
            with open(FILE_NAME, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['ID', 'Name', 'Amount', 'Date', 'Category'])
                writer.writeheader()
        except Exception as create_error:
            print(f"Error creating CSV file: {create_error}")
    return transactions


def filter_transactions(transactions, key, value):
    field_map = {
        "date": "Date",
        "category": "Category",
        "name": "Name"
    }
    actual_key = field_map.get(key.lower(), key)
    return [t for t in transactions if actual_key in t and str(t[actual_key]).lower() == str(value).lower()]


def get_statistics(transactions):
    category_totals = defaultdict(float)
    total_amount = 0
    
    for t in transactions:
        amount = float(t["Amount"])
        category_totals[t["Category"]] += amount
        total_amount += amount
    
    return {
        "category_totals": dict(category_totals),
        "total_amount": total_amount,
        "transaction_count": len(transactions)
    }


# PDF functionality temporarily removed for stability


# ----------------------------- Routes -----------------------------

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test')
def test():
    return jsonify({"status": "App is working!", "timestamp": datetime.now().isoformat()})


@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    transactions = load_transactions()
    
    # Apply filters if provided
    category_filter = request.args.get('category')
    date_filter = request.args.get('date')
    name_filter = request.args.get('name')
    
    if category_filter:
        transactions = filter_transactions(transactions, 'category', category_filter)
    if date_filter:
        transactions = filter_transactions(transactions, 'date', date_filter)
    if name_filter:
        transactions = filter_transactions(transactions, 'name', name_filter)
    
    return jsonify(transactions)


@app.route('/api/transactions', methods=['POST'])
def add_transaction():
    data = request.get_json()
    
    try:
        category = data['category'].lower()
        name = data['name']
        amount = float(data['amount'])
        date = data['date']
        
        if category == 'food':
            meal_type = data.get('meal_type', '')
            location = data.get('location', '')
            transaction = FoodTransaction(name, amount, date, meal_type, location)
        elif category == 'travel':
            transport_mode = data.get('transport_mode', '')
            destination = data.get('destination', '')
            transaction = TravelTransaction(name, amount, date, transport_mode, destination)
        else:
            transaction = Transaction(name, amount, date, category.title())
        
        save_transaction(transaction)
        return jsonify({"status": "success", "message": "Transaction added successfully"})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route('/api/transactions/<transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    data = request.get_json()
    transactions = load_transactions()
    
    # Find and update the transaction
    for t in transactions:
        if t["ID"] == transaction_id:
            t["Name"] = data.get("name", t["Name"])
            t["Amount"] = data.get("amount", t["Amount"])
            t["Date"] = data.get("date", t["Date"])
            t["Category"] = data.get("category", t["Category"])
            
            # Update special fields if they exist
            if "meal_type" in data and "MealType" in t:
                t["MealType"] = data["meal_type"]
            if "location" in data and "Location" in t:
                t["Location"] = data["location"]
            if "transport_mode" in data and "TransportMode" in t:
                t["TransportMode"] = data["transport_mode"]
            if "destination" in data and "Destination" in t:
                t["Destination"] = data["destination"]
            break
    
    # Rewrite the entire file
    if transactions:
        with open(FILE_NAME, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=transactions[0].keys())
            writer.writeheader()
            writer.writerows(transactions)
    
    return jsonify({"status": "success", "message": "Transaction updated successfully"})


@app.route('/api/transactions/<transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    transactions = load_transactions()
    transactions = [t for t in transactions if t["ID"] != transaction_id]
    
    # Rewrite the file without the deleted transaction
    if transactions:
        with open(FILE_NAME, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=transactions[0].keys())
            writer.writeheader()
            writer.writerows(transactions)
    else:
        # If no transactions left, create empty file
        open(FILE_NAME, 'w').close()
    
    return jsonify({"status": "success", "message": "Transaction deleted successfully"})


@app.route('/api/statistics')
def get_statistics_api():
    transactions = load_transactions()
    stats = get_statistics(transactions)
    return jsonify(stats)


@app.route('/api/debug')
def debug_info():
    """Debug endpoint to see what's happening with transactions"""
    try:
        import os
        file_exists = os.path.exists(FILE_NAME)
        file_size = os.path.getsize(FILE_NAME) if file_exists else 0
        
        transactions = load_transactions()
        
        debug_info = {
            "file_exists": file_exists,
            "file_size": file_size,
            "transaction_count": len(transactions),
            "transactions": transactions[:5],  # First 5 transactions only
            "file_name": FILE_NAME
        }
        
        return jsonify(debug_info)
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/api/init-data')
def init_data():
    """Initialize the app with some sample data"""
    try:
        # Create a few sample transactions
        sample_transactions = [
            FoodTransaction("Starbucks Coffee", 5.45, datetime.now().strftime("%Y-%m-%d"), "breakfast", "Downtown"),
            Transaction("Netflix Subscription", 15.99, (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"), "Entertainment"),
            FoodTransaction("Lunch at Chipotle", 12.50, datetime.now().strftime("%Y-%m-%d"), "lunch", "Mall")
        ]
        
        # Save each transaction
        for transaction in sample_transactions:
            save_transaction(transaction)
        
        return jsonify({
            "status": "success", 
            "message": f"Created {len(sample_transactions)} sample transactions",
            "transactions": len(load_transactions())
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/export-pdf')
def export_pdf():
    return jsonify({"status": "error", "message": "PDF export feature temporarily disabled for stability"}), 503


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)