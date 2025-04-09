# Inventory Management System

A modern web-based inventory management system built with Flask and Bootstrap.

## Features

- User authentication (Admin/Employee roles)
- Product management (Add, Edit, Delete, View)
- Sales tracking and reporting
- Real-time inventory updates
- Modern, responsive interface
- Role-based access control

## Prerequisites

- Python 3.x
- pip (Python package installer)

## Installation

1. Clone or download this repository
2. Make sure Python 3.x is installed on your system
3. Double-click `run.bat` to start the application
   - This will automatically install required packages
   - The application will start in your default web browser

## Default Login Credentials

### Admin Account
- Username: `admin`
- Password: `admin123`

## Manual Installation (Alternative)

If you prefer to run the application manually:

1. Open a terminal/command prompt
2. Navigate to the project directory
3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python app.py
   ```
5. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Project Structure

```
inventory_system/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── run.bat            # Windows batch file to run the application
├── README.md          # This file
└── templates/         # HTML templates
    ├── base.html
    ├── login.html
    ├── dashboard.html
    ├── products.html
    ├── add_product.html
    ├── edit_product.html
    └── sales_report.html
```

## Security Notes

- Change the default admin password after first login
- The application uses SQLite for data storage
- All passwords are hashed before storage
- Session management is handled securely

## Support

For any issues or questions, please create an issue in the repository. 