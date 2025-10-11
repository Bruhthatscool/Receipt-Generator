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
        super().__init__(parent, bg="#f8f9fa")

        title = tk.Label(self, text="New Donor Registration", font=("Arial", 18, "bold"), bg="#f8f9fa")
        title.pack(pady=15)

        self.parent = parent

        # Variables
        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.location_var = tk.StringVar()

        form_frame = tk.Frame(self, bg="#f8f9fa")
        form_frame.pack(padx=20, pady=10)

        labels = ["Donor Name *", "Phone No", "Email", "Address", "Location"]
        variables = [self.name_var, self.phone_var, self.email_var, self.address_var, self.location_var]

        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label, bg="#f8f9fa").grid(row=i, column=0, sticky="w", pady=5)
            tk.Entry(form_frame, textvariable=variables[i], width=33).grid(row=i, column=1, pady=5)

        tk.Button(self, text="Save Donor", command=self.save_donor, bg="#198754", fg="white",
                  font=("Arial", 12, "bold")).pack(pady=20)

        tk.Button(self, text="Back to Donation Entry", command=lambda: parent.show_frame(DonationEntryPage),
                  bg="#0d6efd", fg="white", font=("Arial", 10, "bold")).pack(pady=5)

    def save_donor(self):
        name = self.name_var.get()
        phone = self.phone_var.get()
        email = self.email_var.get()
        address = self.address_var.get()
        location = self.location_var.get()

        if not name:
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
        for var in [self.name_var, self.phone_var, self.email_var, self.address_var, self.location_var]:
            var.set("")


# ---------------- PAGE 2: DONATION ENTRY ----------------
class DonationEntryPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f8f9fa")

        title = tk.Label(self, text="Donation Entry Form", font=("Arial", 18, "bold"), bg="#f8f9fa")
        title.pack(pady=15)

        self.parent = parent

        # Variables
        self.name_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.payment_var = tk.StringVar()
        self.ref_var = tk.StringVar()
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))

        form_frame = tk.Frame(self, bg="#f8f9fa")
        form_frame.pack(padx=20, pady=10)

        # Fields only for mandatory info
        labels = ["Donor Name *", "Amount *", "Category *", "Payment Type *", "Reference No", "Date *"]
        variables = [self.name_var, self.amount_var, self.category_var,
                     self.payment_var, self.ref_var, self.date_var]

        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label, bg="#f8f9fa").grid(row=i, column=0, sticky="w", pady=5)
            if label == "Category *":
                entry = ttk.Combobox(form_frame, textvariable=self.category_var,
                                     values=["Education", "Health", "Food", "Other"], width=30)
            elif label == "Payment Type *":
                entry = ttk.Combobox(form_frame, textvariable=self.payment_var,
                                     values=["Cash", "UPI", "Card", "Cheque"], width=30)
            else:
                entry = tk.Entry(form_frame, textvariable=variables[i], width=33)
            entry.grid(row=i, column=1)

        # Buttons
        tk.Button(self, text="Submit Donation", command=self.submit_donation,
                  bg="#198754", fg="white", font=("Arial", 12, "bold")).pack(pady=20)
        tk.Button(self, text="New Donor Registration", command=lambda: parent.show_frame(DonorEntryPage),
                  bg="#6c757d", fg="white", font=("Arial", 10, "bold")).pack(pady=5)
        tk.Button(self, text="View Donations", command=lambda: parent.show_frame(ViewDonationsPage),
                  bg="#0d6efd", fg="white", font=("Arial", 10, "bold")).pack(pady=5)

    def submit_donation(self):
        name = self.name_var.get()
        amount = self.amount_var.get()
        category = self.category_var.get()
        payment_type = self.payment_var.get()
        reference_no = self.ref_var.get()
        date = self.date_var.get()

        if not (name and amount and category and payment_type and date):
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

        # Insert donation record
        cursor.execute("""
            INSERT INTO receipt_table (donar_id, amount, date, category, payment_type, reference_no)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (donar_id, amount, date, category, payment_type, reference_no))
        conn.commit()

        receipt_id = cursor.lastrowid
        conn.close()

        self.parent.frames[ReceiptPage].set_receipt_data(
            receipt_id, name, amount, category, payment_type, reference_no, date
        )
        self.parent.show_frame(ReceiptPage)


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

