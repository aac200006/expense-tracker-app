#!/usr/bin/env python3
"""
This script creates some sample transactions for demonstration purposes.
Run this locally or on the server to populate the app with initial data.
"""

import csv
import uuid
from datetime import datetime, timedelta

# Sample transactions data
sample_transactions = [
    {
        "ID": str(uuid.uuid4()),
        "Name": "Starbucks Coffee",
        "Amount": 5.45,
        "Date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        "Category": "Food",
        "MealType": "breakfast",
        "Location": "Downtown"
    },
    {
        "ID": str(uuid.uuid4()),
        "Name": "Netflix Subscription",
        "Amount": 15.99,
        "Date": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
        "Category": "Entertainment"
    },
    {
        "ID": str(uuid.uuid4()),
        "Name": "Lunch at Chipotle",
        "Amount": 12.50,
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Category": "Food",
        "MealType": "lunch",
        "Location": "Mall Food Court"
    }
]

def create_sample_data():
    """Create sample expenses.csv file"""
    filename = "expenses.csv"
    
    # Get all possible fieldnames from sample data
    all_fieldnames = set()
    for transaction in sample_transactions:
        all_fieldnames.update(transaction.keys())
    
    fieldnames = list(all_fieldnames)
    
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sample_transactions)
    
    print(f"Created {filename} with {len(sample_transactions)} sample transactions")

if __name__ == "__main__":
    create_sample_data()