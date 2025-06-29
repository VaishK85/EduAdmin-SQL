# ---------- Import Required Libraries ----------
import tkinter as tk                             # Main GUI module
from tkinter import messagebox, ttk              # messagebox for alerts, ttk for modern widgets like Treeview
import mysql.connector                           # For connecting and interacting with MySQL database

# ---------- Function to Connect to MySQL Database ----------
def connect_db():
    # This function establishes a connection to your MySQL database
    # Make sure MySQL is running and database/table exists
    return mysql.connector.connect(
        host="localhost",            # Server location
        user="root",                 # Your MySQL username
        password="Root@123",         # Your MySQL password
        database="CollegeDB"         # Your database name
    )

# ---------- Function to Save Student Data ----------
def save_student():
    # Read input values from Entry fields
    name = entry_name.get()
    roll = entry_roll.get()
    dept = entry_dept.get()
    total = entry_total.get()
    paid = entry_paid.get()

    # Validate that all fields are filled
    if not name or not roll or not dept or not total or not paid:
        messagebox.showwarning("Missing", "All fields are required")
        return  # Exit function if validation fails

    try:
        # Convert total and paid to float for calculation
        total = float(total)
        paid = float(paid)
        remaining = total - paid  # Calculate remaining fees

        # Connect to MySQL
        con = connect_db()
        cur = con.cursor()  # Cursor is used to execute SQL commands

        # Insert student record into the Students table
        cur.execute("""INSERT INTO Students 
            (Name, RollNo, Department, TotalFees, FeesPaid, RemainingFees) 
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (name, roll, dept, total, paid, remaining))  # Use placeholders for safety

        con.commit()  # Save the changes permanently
        con.close()   # Close the DB connection

        # Notify user of successful save
        messagebox.showinfo("Success", "Student data saved with fee info.")

        # Update the table display with new data
        show_students()

        # Clear all entry fields for the next input
        for e in [entry_name, entry_roll, entry_dept, entry_total, entry_paid]:
            e.delete(0, tk.END)  # Clear text in entry

    except Exception as e:
        # Show error popup if anything goes wrong (e.g. DB error)
        messagebox.showerror("Error", str(e))

# ---------- Function to Show All Student Records ----------
def show_students():
    # Clear current Treeview rows (to avoid duplicates when refreshing)
    for row in tree.get_children():
        tree.delete(row)

    try:
        # Connect to database
        con = connect_db()
        cur = con.cursor()

        # Get all student records from database
        cur.execute("SELECT ID, Name, RollNo, Department, TotalFees, FeesPaid, RemainingFees FROM Students")
        rows = cur.fetchall()  # Fetch all rows at once and it is a bulitin function
        con.close()

        # Loop through each row and insert into Treeview
        for row in rows:
            tree.insert("", tk.END, values=row)  # Insert as a new row in the table

    except Exception as e:
        # Show error if database fails or no data found
        messagebox.showerror("Error", str(e))

# ---------- Function to Logout and Go Back to Login Window ----------
def logout():
    main_win.destroy()    # Close the current window (Admin Panel)
    login_window()        # Open the login window again

# ---------- Function to Open Main Admin Panel ----------
def open_main_window():
    global main_win, entry_name, entry_roll, entry_dept, entry_total, entry_paid, tree

    # Create main admin window
    main_win = tk.Tk()
    main_win.title("College Admin Panel")
    main_win.geometry("750x600")
    main_win.config(bg="lightcyan")  # Set background color

    # Title Label
    tk.Label(main_win, text="College Administration System", font=("Arial", 16), bg="lightcyan").pack(pady=10)

    # ------------ Form Fields for Student Data Input ------------
    # Name
    tk.Label(main_win, text="Name", bg="lightcyan").pack()
    entry_name = tk.Entry(main_win)
    entry_name.pack()

    # Roll Number
    tk.Label(main_win, text="Roll Number", bg="lightcyan").pack()
    entry_roll = tk.Entry(main_win)
    entry_roll.pack()

    # Department
    tk.Label(main_win, text="Department", bg="lightcyan").pack()
    entry_dept = tk.Entry(main_win)
    entry_dept.pack()

    # Total Fees
    tk.Label(main_win, text="Total Fees", bg="lightcyan").pack()
    entry_total = tk.Entry(main_win)
    entry_total.pack()

    # Fees Paid
    tk.Label(main_win, text="Fees Paid", bg="lightcyan").pack()
    entry_paid = tk.Entry(main_win)
    entry_paid.pack()

    # Button to Save Data
    tk.Button(main_win, text="Save Student", command=save_student, bg="green", fg="white").pack(pady=10)

    # ------------ Treeview Table to Display Students ------------
    columns = ("ID", "Name", "RollNo", "Department", "Total", "Paid", "Remaining")  # Column headers
    tree = ttk.Treeview(main_win, columns=columns, show="headings")  # Only show column headers, no tree

    # Set table headings and column widths
    for col in columns:
        tree.heading(col, text=col)        # Column header
        tree.column(col, width=100)        # Width of each column

    tree.pack(pady=10)  # Add space before and after

    # Logout Button
    tk.Button(main_win, text="Logout", command=logout, bg="red", fg="white").pack(pady=5)

    # Load student records immediately on start
    show_students()

    # Start the GUI main loop
    main_win.mainloop()

# ---------- Function to Create Admin Login Window ----------
def login_window():
    def check_login():
        username = user_entry.get()
        password = pass_entry.get()

        # Simple check with fixed credentials (can be made dynamic)
        if username == "admin" and password == "admin123":
            login.destroy()           # Close login window
            open_main_window()        # Open main admin panel
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password")

    # Create login window
    login = tk.Tk()
    login.title("Admin Login")
    login.geometry("300x200")
    login.config(bg="lightgray")

    # Login Title
    tk.Label(login, text="Admin Login", font=("Arial", 16), bg="lightgray").pack(pady=10)

    # Username Field
    tk.Label(login, text="Username", bg="lightgray").pack()
    user_entry = tk.Entry(login)
    user_entry.pack()

    # Password Field (hidden characters)
    tk.Label(login, text="Password", bg="lightgray").pack()
    pass_entry = tk.Entry(login, show="*")  # show="*" hides the text
    pass_entry.pack()

    # Login Button
    tk.Button(login, text="Login", command=check_login, bg="blue", fg="white").pack(pady=15)

    # Run the login window
    login.mainloop()

# ---------- Start the Program from Login Window ----------
login_window()  # Entry point of the application
