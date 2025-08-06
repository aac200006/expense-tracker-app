# Expense Tracker Web App

A beautiful and modern web application for tracking your expenses, built with Flask and featuring a responsive design.

## Features

- **Add Transactions**: Create expense entries with categories (Food, Travel, Other)
- **Specialized Fields**: Food transactions include meal type and location; Travel transactions include transport mode and destination
- **Real-time Statistics**: View total spending, transaction counts, and category breakdowns
- **Filtering**: Filter transactions by category, date, or name
- **Edit & Delete**: Modify or remove existing transactions
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Modern UI**: Beautiful gradient design with smooth animations

## Installation

1. **Clone or download the project**:
   ```bash
   cd expense_tracker_app
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and go to:
   ```
   http://localhost:5000
   ```

## Usage

### Adding Transactions

1. Select a category (Food, Travel, or Other)
2. Fill in the expense name and amount
3. Choose the date
4. For Food: Add meal type and location
5. For Travel: Add transport mode and destination
6. Click "Add Transaction"

### Viewing and Filtering

- All transactions are displayed in a beautiful card layout
- Use the filters to find specific transactions by category, date, or name
- Click "Clear Filters" to see all transactions

### Editing Transactions

- Click the edit button (pencil icon) on any transaction
- Modify the details in the popup modal
- Click "Save Changes" to update

### Deleting Transactions

- Click the delete button (trash icon) on any transaction
- Confirm the deletion when prompted

### Statistics

- View your total spending and transaction count
- See breakdown by category
- Statistics update automatically when transactions are added, edited, or deleted

## Data Storage

Transactions are stored in a CSV file (`expenses.csv`) in the application directory. This file is created automatically when you add your first transaction.

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Modern CSS with gradients and animations
- **Icons**: Font Awesome
- **Fonts**: Google Fonts (Inter)
- **Data Storage**: CSV files

## Project Structure

```
expense_tracker_app/
├── app.py              # Flask application and API routes
├── templates/
│   └── index.html      # Main HTML template with embedded CSS/JS
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── expenses.csv       # Data storage (created automatically)
```

## API Endpoints

- `GET /` - Main application page
- `GET /api/transactions` - Get all transactions (with optional filters)
- `POST /api/transactions` - Add new transaction
- `PUT /api/transactions/<id>` - Update existing transaction
- `DELETE /api/transactions/<id>` - Delete transaction
- `GET /api/statistics` - Get spending statistics

## Contributing

This application was converted from a Jupyter notebook command-line interface to a modern web application. Feel free to enhance it further by:

- Adding user authentication
- Implementing data export features
- Adding charts and graphs
- Creating transaction categories management
- Adding budget tracking features

## License

This project is open source and available under the MIT License.