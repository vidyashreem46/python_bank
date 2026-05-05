# python_bank
---
PROJECT OVERVIEW

Python National Bank PRO is a command-line based banking system developed using Python. It simulates real-world banking operations such as account management, transactions, loans, and analytics.

# This project demonstrates:
File handling using JSON
Secure authentication system
Financial calculations
Modular programming

# FEATURES

Security:
PIN-based login (SHA-256 encryption)
OTP verification (simulated)
Account freeze and unfreeze

# Banking Operations:
Create account
Deposit and withdraw money
Fund transfer with OTP for large amounts
Daily transaction limits

# Advanced Features:
Net worth dashboard
Multi-currency balance view
Spending analytics

# Financial Services:
Fixed deposit system
Loan management with EMI calculation
Bill payments

# Smart Tools:
Savings goals tracker
Reward points system

# Admin Panel:
View all accounts
Search account
Freeze/unfreeze account
View bank statistics


# REQUIREMENTS

Python 3.x
No external libraries required

# HOW TO RUN

Step 1: Open terminal or command prompt
Step 2: Navigate to project folder
Step 3: Run the program using:

python main.py
For Jupyter Notebook:
!python main.py
DEFAULT ADMIN LOGIN
Admin PIN: admin123

# DATA STORAGE
All data is stored in the file:
bank_pro_data.json

# It includes:
Account details
Transactions
Loans
Fixed deposits
Reward points

# KEY MODULES
Account Management
Account creation with OTP
Secure login system
Transactions
Deposit and withdrawal
Fund transfer
Financial Services
Loan EMI calculation
Fixed deposit maturity
Analytics
Spending by category
Monthly analysis
Net savings calculation

# IMPORTANT FORMULAS
EMI Formula:
EMI = (P × r × (1 + r)^n) / ((1 + r)^n - 1)
Where:
P = Principal amount
r = Monthly interest rate
n = Number of months
Fixed Deposit Formula:
Maturity = P × (1 + (r/100 × t/12))

# LEARNING OUTCOMES
Understanding banking systems
Secure authentication implementation
JSON data handling
Financial logic implementation
Large-scale Python project development

# LIMITATIONS
OTP is simulated (not real)
No database used (JSON only)
Command-line interface (no GUI)

# FUTURE ENHANCEMENTS
Add graphical interface (GUI)
Integrate real OTP system
Use database (MySQL/MongoDB)
Develop web or mobile app
Add AI-based analytics


# CONCLUSION
In this project is a complete mini banking system that demonstrates real-world banking operations, security features, and financial analytics. It is suitable for academic projects and practical learning.
