import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

# ---------------- DATABASE CONNECTION ----------------
def connect_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Ananya#1',  # change this if needed
            database='new_db'
        )
        return conn
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database:\n{e}")
        return None


# ---------------- MAIN APPLICATION ----------------
class DonationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Donation Management System")
        self.geometry("750x600")
        self.configure(bg="#f8f9fa")

        # Initialize Frames
        self.frames = {}
        for F in (DonorEntryPage, DonationEntryPage, ReceiptPage, ViewDonationsPage):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(DonationEntryPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# ---------------- PAGE 1: DONOR ENTRY ----------------
class DonorEntryPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f8f9fa", padx=30, pady=30, relief="raised", bd=2, highlightbackground="#d3d3d3", highlightthickness=1)
        
        self.parent = parent

        # Use a main frame to center the content
        main_frame = tk.Frame(self, bg="#ffffff", padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")

        title = tk.Label(main_frame, text="Donor Registration", font=("Arial", 18, "bold"), bg="#ffffff", fg="#0d6efd")
        title.pack(pady=10)

        # Variables
        self.donor_id_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.location_var = tk.StringVar()

        form_frame = tk.Frame(main_frame, bg="#ffffff")
        form_frame.pack(padx=20, pady=10)

        # First row: Donor ID and Name
        tk.Label(form_frame, text="Donor ID", bg="#ffffff").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        entry1 = tk.Entry(form_frame, textvariable=self.donor_id_var, width=33, font=("Arial", 10), bd=1, relief="solid")
        entry1.grid(row=1, column=0, pady=5, padx=5)
        entry1.insert(0, "e.g., DN-0001")
        entry1.bind("<FocusIn>", lambda event: self.clear_placeholder(event, entry1, "e.g., DN-0001"))
        entry1.bind("<FocusOut>", lambda event: self.add_placeholder(event, entry1, self.donor_id_var, "e.g., DN-0001"))

        tk.Label(form_frame, text="Name", bg="#ffffff").grid(row=0, column=1, sticky="w", pady=5, padx=5)
        entry2 = tk.Entry(form_frame, textvariable=self.name_var, width=33, font=("Arial", 10), bd=1, relief="solid")
        entry2.grid(row=1, column=1, pady=5, padx=5)
        entry2.insert(0, "Full name")
        entry2.bind("<FocusIn>", lambda event: self.clear_placeholder(event, entry2, "Full name"))
        entry2.bind("<FocusOut>", lambda event: self.add_placeholder(event, entry2, self.name_var, "Full name"))
        
        # Second row: Phone Number and Email
        tk.Label(form_frame, text="Phone Number", bg="#ffffff").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        entry3 = tk.Entry(form_frame, textvariable=self.phone_var, width=33, font=("Arial", 10), bd=1, relief="solid")
        entry3.grid(row=3, column=0, pady=5, padx=5)
        entry3.insert(0, "e.g., +1 555 000 1234")
        entry3.bind("<FocusIn>", lambda event: self.clear_placeholder(event, entry3, "e.g., +1 555 000 1234"))
        entry3.bind("<FocusOut>", lambda event: self.add_placeholder(event, entry3, self.phone_var, "e.g., +1 555 000 1234"))
        
        tk.Label(form_frame, text="Email", bg="#ffffff").grid(row=2, column=1, sticky="w", pady=5, padx=5)
        entry4 = tk.Entry(form_frame, textvariable=self.email_var, width=33, font=("Arial", 10), bd=1, relief="solid")
        entry4.grid(row=3, column=1, pady=5, padx=5)
        entry4.insert(0, "name@example.com")
        entry4.bind("<FocusIn>", lambda event: self.clear_placeholder(event, entry4, "name@example.com"))
        entry4.bind("<FocusOut>", lambda event: self.add_placeholder(event, entry4, self.email_var, "name@example.com"))

        # Third row: Address (spanning both columns)
        tk.Label(form_frame, text="Address", bg="#ffffff").grid(row=4, column=0, sticky="w", pady=5, padx=5)
        self.address_entry = tk.Text(form_frame, width=68, height=3, font=("Arial", 10), bd=1, relief="solid")
        self.address_entry.grid(row=5, column=0, columnspan=2, pady=5, padx=5)
        self.address_entry.insert(tk.END, "Street, City, State, ZIP")
        self.address_entry.bind("<FocusIn>", lambda event: self.clear_text_placeholder(event, self.address_entry, "Street, City, State, ZIP"))
        self.address_entry.bind("<FocusOut>", lambda event: self.add_text_placeholder(event, self.address_entry, "Street, City, State, ZIP"))

        # Fourth row: Location
        tk.Label(form_frame, text="Location", bg="#ffffff").grid(row=6, column=0, sticky="w", pady=5, padx=5)
        entry5 = tk.Entry(form_frame, textvariable=self.location_var, width=33, font=("Arial", 10), bd=1, relief="solid")
        entry5.grid(row=7, column=0, pady=5, padx=5)
        entry5.insert(0, "City / Region")
        entry5.bind("<FocusIn>", lambda event: self.clear_placeholder(event, entry5, "City / Region"))
        entry5.bind("<FocusOut>", lambda event: self.add_placeholder(event, entry5, self.location_var, "City / Region"))


        button_frame = tk.Frame(main_frame, bg="#ffffff")
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Register", command=self.save_donor, bg="#0d6efd", fg="white", font=("Arial", 12, "bold"), padx=15, pady=5).pack(side="left", padx=10)
        tk.Button(button_frame, text="Continue", command=lambda: parent.show_frame(DonationEntryPage), bg="#6c757d", fg="white", font=("Arial", 12, "bold"), padx=15, pady=5).pack(side="left", padx=10)

    def clear_placeholder(self, event, entry_widget, placeholder_text):
        if entry_widget.get() == placeholder_text:
            entry_widget.delete(0, tk.END)

    def add_placeholder(self, event, entry_widget, variable, placeholder_text):
        if not variable.get():
            entry_widget.insert(0, placeholder_text)

    def clear_text_placeholder(self, event, text_widget, placeholder_text):
        if text_widget.get("1.0", tk.END).strip() == placeholder_text:
            text_widget.delete("1.0", tk.END)

    def add_text_placeholder(self, event, text_widget, placeholder_text):
        if not text_widget.get("1.0", tk.END).strip():
            text_widget.insert("1.0", placeholder_text)

    def save_donor(self):
        name = self.name_var.get()
        phone = self.phone_var.get()
        email = self.email_var.get()
        address = self.address_entry.get("1.0", tk.END).strip()
        location = self.location_var.get()

        if name == "Full name" or not name:
            messagebox.showwarning("Input Error", "Donor name is required.")
            return

        conn = connect_db()
        if conn is None:
            return
        cursor = conn.cursor()

        # Check if donor already exists
        cursor.execute("SELECT donar_id FROM donar_details WHERE name=%s", (name,))
        if cursor.fetchone():
            messagebox.showinfo("Duplicate", "This donor already exists.")
            conn.close()
            return

        cursor.execute("""
            INSERT INTO donar_details (name, phone_no, email, address, location)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, phone, email, address, location))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Donor details saved successfully!")
        self.clear_fields()

    def clear_fields(self):
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.address_entry.delete("1.0", tk.END)
        self.location_var.set("")
        
        # Reset placeholders
        self.name_var.set("Full name")
        self.phone_var.set("e.g., +1 555 000 1234")
        self.email_var.set("name@example.com")
        self.address_entry.insert("1.0", "Street, City, State, ZIP")
        self.location_var.set("City / Region")


# ---------------- PAGE 2: DONATION ENTRY ----------------
class DonationEntryPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f8f9fa", padx=30, pady=30, relief="raised", bd=2, highlightbackground="#d3d3d3", highlightthickness=1)
        
        self.parent = parent
        
        # Use a main frame to center the content
        main_frame = tk.Frame(self, bg="#ffffff", padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")

        title_frame = tk.Frame(main_frame, bg="#ffffff")
        title_frame.pack(fill="x", pady=10)
        
        title = tk.Label(title_frame, text="DONATION DETAILS", font=("Arial", 18, "bold"), bg="#ffffff", fg="#0d6efd")
        title.pack(side="left", padx=5)

        tk.Button(title_frame, text="New Donor Registration", command=lambda: parent.show_frame(DonorEntryPage),
                  bg="#d3d3d3", fg="black", font=("Arial", 10)).pack(side="right")


        # Variables
        self.name_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.payment_var = tk.StringVar()
        self.ref_var = tk.StringVar()
        self.date_var = tk.StringVar(value=datetime.now().strftime("%d-%m-%Y"))

        form_frame = tk.Frame(main_frame, bg="#ffffff")
        form_frame.pack(padx=20, pady=10)

        # First row: Donor Name and Amount
        tk.Label(form_frame, text="Donor Name", bg="#ffffff").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        name_entry = tk.Entry(form_frame, textvariable=self.name_var, width=33, font=("Arial", 10), bd=1, relief="solid")
        name_entry.grid(row=1, column=0, pady=5, padx=5)
        name_entry.insert(0, "Enter donor name")
        name_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, name_entry, "Enter donor name"))
        name_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, name_entry, self.name_var, "Enter donor name"))

        tk.Label(form_frame, text="Amount", bg="#ffffff").grid(row=0, column=1, sticky="w", pady=5, padx=5)
        amount_entry = tk.Entry(form_frame, textvariable=self.amount_var, width=33, font=("Arial", 10), bd=1, relief="solid")
        amount_entry.grid(row=1, column=1, pady=5, padx=5)
        amount_entry.insert(0, "0.00")
        amount_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, amount_entry, "0.00"))
        amount_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, amount_entry, self.amount_var, "0.00"))


        # Second row: Payment Category and Date
        tk.Label(form_frame, text="Payment Category", bg="#ffffff").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        category_combobox = ttk.Combobox(form_frame, textvariable=self.category_var,
                                         values=["Education", "Health", "Food", "Other"], width=30, font=("Arial", 10), state="readonly")
        category_combobox.set("Select a category")
        category_combobox.grid(row=3, column=0, pady=5, padx=5)
        
        tk.Label(form_frame, text="Date", bg="#ffffff").grid(row=2, column=1, sticky="w", pady=5, padx=5)
        date_entry = tk.Entry(form_frame, textvariable=self.date_var, width=33, font=("Arial", 10), bd=1, relief="solid")
        date_entry.grid(row=3, column=1, pady=5, padx=5)
        date_entry.insert(0, "dd-mm-yyyy")
        date_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, date_entry, "dd-mm-yyyy"))
        date_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, date_entry, self.date_var, "dd-mm-yyyy"))

        # Third row: Payment Method and Ref Number
        tk.Label(form_frame, text="Payment Method", bg="#ffffff").grid(row=4, column=0, sticky="w", pady=5, padx=5)
        payment_combobox = ttk.Combobox(form_frame, textvariable=self.payment_var,
                                        values=["Cash", "UPI", "Card", "Cheque"], width=30, font=("Arial", 10), state="readonly")
        payment_combobox.set("Select a method")
        payment_combobox.grid(row=5, column=0, pady=5, padx=5)

        tk.Label(form_frame, text="Ref Number", bg="#ffffff").grid(row=4, column=1, sticky="w", pady=5, padx=5)
        ref_entry = tk.Entry(form_frame, textvariable=self.ref_var, width=33, font=("Arial", 10), bd=1, relief="solid")
        ref_entry.grid(row=5, column=1, pady=5, padx=5)
        ref_entry.insert(0, "Reference number")
        ref_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, ref_entry, "Reference number"))
        ref_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, ref_entry, self.ref_var, "Reference number"))

        button_frame = tk.Frame(main_frame, bg="#ffffff")
        button_frame.pack(fill="x", pady=20)
        
        tk.Button(button_frame, text="Reset", command=self.clear_fields, bg="#6c757d", fg="white", font=("Arial", 12, "bold"), padx=15, pady=5).pack(side="right", padx=10)
        tk.Button(button_frame, text="Submit", command=self.submit_donation, bg="#0d6efd", fg="white", font=("Arial", 12, "bold"), padx=15, pady=5).pack(side="right", padx=10)

    def clear_placeholder(self, event, entry_widget, placeholder_text):
        if entry_widget.get() == placeholder_text:
            entry_widget.delete(0, tk.END)

    def add_placeholder(self, event, entry_widget, variable, placeholder_text):
        if not variable.get():
            entry_widget.insert(0, placeholder_text)

    def submit_donation(self):
        name = self.name_var.get()
        amount = self.amount_var.get()
        category = self.category_var.get()
        payment_type = self.payment_var.get()
        reference_no = self.ref_var.get()
        date = self.date_var.get()

        if name == "Enter donor name" or not name or amount == "0.00" or not amount or category == "Select a category" or not category or payment_type == "Select a method" or not payment_type or date == "dd-mm-yyyy" or not date:
            messagebox.showwarning("Input Error", "Please fill all mandatory fields.")
            return

        conn = connect_db()
        if conn is None:
            return
        cursor = conn.cursor()

        # Check donor exists
        cursor.execute("SELECT donar_id FROM donar_details WHERE name=%s", (name,))
        result = cursor.fetchone()
        if not result:
            messagebox.showerror("Donor Not Found", "Donor not found. Please register the donor first.")
            conn.close()
            return

        donar_id = result[0]
        
        # Convert date format for database
        try:
            date_obj = datetime.strptime(date, "%d-%m-%Y").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Date Error", "Please enter date in dd-mm-yyyy format.")
            return

        # Insert donation record
        cursor.execute("""
            INSERT INTO receipt_table (donar_id, amount, date, category, payment_type, reference_no)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (donar_id, amount, date_obj, category, payment_type, reference_no if reference_no != "Reference number" else None))
        conn.commit()

        receipt_id = cursor.lastrowid
        conn.close()

        self.parent.frames[ReceiptPage].set_receipt_data(
            receipt_id, name, amount, category, payment_type, reference_no, date
        )
        self.parent.show_frame(ReceiptPage)

    def clear_fields(self):
        self.name_var.set("Enter donor name")
        self.amount_var.set("0.00")
        self.category_var.set("Select a category")
        self.payment_var.set("Select a method")
        self.ref_var.set("Reference number")
        self.date_var.set(datetime.now().strftime("%d-%m-%Y"))


# ---------------- PAGE 3: RECEIPT PAGE ----------------
class ReceiptPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#fff")

        self.title = tk.Label(self, text="Donation Receipt", font=("Arial", 18, "bold"), bg="#fff")
        self.title.pack(pady=15)

        self.text_box = tk.Text(self, width=70, height=20, font=("Courier", 11))
        self.text_box.pack(padx=20, pady=10)

        tk.Button(self, text="Back to Home", command=lambda: parent.show_frame(DonationEntryPage),
                  bg="#0d6efd", fg="white", font=("Arial", 12, "bold")).pack(pady=10)

    def set_receipt_data(self, rid, name, amount, category, payment, ref, date):
        self.text_box.delete(1.0, tk.END)
        receipt_text = f"""
----------------------------------------------
                DONATION RECEIPT
----------------------------------------------
Receipt ID     : {rid}
Donor Name     : {name}
Category       : {category}
Amount         : ₹{amount}
Payment Type   : {payment}
Reference No   : {ref if ref else 'N/A'}
Date           : {date}
----------------------------------------------
Thank you for your contribution!
----------------------------------------------
"""
        self.text_box.insert(tk.END, receipt_text)


# ---------------- PAGE 4: VIEW DONATIONS ----------------
class ViewDonationsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f8f9fa")

        tk.Label(self, text="View Donations", font=("Arial", 18, "bold"), bg="#f8f9fa").pack(pady=15)

        date_frame = tk.Frame(self, bg="#f8f9fa")
        date_frame.pack(pady=10)

        self.start_date = tk.StringVar()
        self.end_date = tk.StringVar()

        tk.Label(date_frame, text="Start Date (YYYY-MM-DD):", bg="#f8f9fa").grid(row=0, column=0, padx=5)
        tk.Entry(date_frame, textvariable=self.start_date, width=15).grid(row=0, column=1)
        tk.Label(date_frame, text="End Date (YYYY-MM-DD):", bg="#f8f9fa").grid(row=0, column=2, padx=5)
        tk.Entry(date_frame, textvariable=self.end_date, width=15).grid(row=0, column=3)

        tk.Button(date_frame, text="Search", command=self.search_records,
                  bg="#198754", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=4, padx=10)

        columns = ("Receipt ID", "Donor", "Amount", "Date", "Category", "Payment Type")
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(padx=10, pady=10)

        tk.Button(self, text="Back", command=lambda: parent.show_frame(DonationEntryPage),
                  bg="#0d6efd", fg="white", font=("Arial", 10, "bold")).pack(pady=5)

    def search_records(self):
        sdate = self.start_date.get()
        edate = self.end_date.get()

        if not (sdate and edate):
            messagebox.showwarning("Input Error", "Please enter both start and end dates.")
            return

        conn = connect_db()
        if conn is None:
            return
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.receipt_id, d.name, r.amount, r.date, r.category, r.payment_type
            FROM receipt_table r
            JOIN donar_details d ON r.donar_id = d.donar_id
            WHERE r.date BETWEEN %s AND %s
        """, (sdate, edate))
        records = cursor.fetchall()
        conn.close()

        for row in self.tree.get_children():
            self.tree.delete(row)

        for rec in records:
            self.tree.insert("", "end", values=rec)


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app = DonationApp()
    app.mainloop()
