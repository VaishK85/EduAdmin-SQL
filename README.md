# College Administration System

This is a desktop-based College Administration System developed using Python (Tkinter) and MySQL. The application allows administrators to manage student fee records with a simple and interactive graphical user interface.

## Features

- Admin login system
- Student data entry form
- Fee management: Total, Paid, and Remaining fees
- MySQL database integration
- Real-time display of student records using Treeview
- Clean, user-friendly GUI built with Tkinter

## Technologies Used

- Python 3
- Tkinter (for GUI)
- MySQL (for database)
- mysql-connector-python (for DB connectivity)

## Setup Instructions

### 1. Clone the Repository

Open your terminal or command prompt and run:

```bash
git clone https://github.com/your-username/CollegeAdminSystem.git
cd CollegeAdminSystem

## Set Up the Database

1. Ensure that MySQL server is installed and running.
2. Open MySQL Workbench or Command Line.
3. Run the SQL script database_setup.sql:sql
-Copy
-Edit
-SOURCE path/to/database_setup.sql;

##  Install Required Python Packages

1. pip install -r requirements.txt

2. pip install mysql-connector-python

## Run the Application

python main.py

## SQL Schema

CREATE DATABASE IF NOT EXISTS CollegeDB;

USE CollegeDB;

CREATE TABLE IF NOT EXISTS Students (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    RollNo VARCHAR(50),
    Department VARCHAR(100),
    TotalFees FLOAT,
    FeesPaid FLOAT,
    RemainingFees FLOAT
);


