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
            password='',  # change if needed
            database='new_db'
        )
        return conn
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database:\n{e}")
        return None

# ---------------- PAGE 1: DONOR ENTRY ----------------
class DonorEntryPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f8f9fa", padx=30, pady=30)
        self.parent = parent

        main_frame = tk.Frame(self, bg="#ffffff", padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")

        tk.Label(main_frame, text="Donor Registration", font=("Arial", 18, "bold"), bg="#ffffff", fg="#0d6efd").pack(pady=10)

        # Variables
        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.location_var = tk.StringVar()

        form_frame = tk.Frame(main_frame, bg="#ffffff")
        form_frame.pack(padx=20, pady=10)

        # Name
        tk.Label(form_frame, text="Name *", bg="#ffffff").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.name_entry = tk.Entry(form_frame, textvariable=self.name_var, width=33, font=("Arial", 10), bd=1, relief="solid")
        self.name_entry.grid(row=1, column=0, pady=5, padx=5)

        # Phone
        tk.Label(form_frame, text="Phone Number *", bg="#ffffff").grid(row=0, column=1, sticky="w", pady=5, padx=5)
        self.phone_entry = tk.Entry(form_frame, textvariable=self.phone_var, width=33, font=("Arial", 10), bd=1, relief="solid")
        self.phone_entry.grid(row=1, column=1, pady=5, padx=5)

        # Email
        tk.Label(form_frame, text="Email", bg="#ffffff").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        self.email_entry = tk.Entry(form_frame, textvariable=self.email_var, width=33, font=("Arial", 10), bd=1, relief="solid")
        self.email_entry.grid(row=3, column=0, pady=5, padx=5)

        # Address
        tk.Label(form_frame, text="Address", bg="#ffffff").grid(row=2, column=1, sticky="w", pady=5, padx=5)
        self.address_entry = tk.Entry(form_frame, textvariable=self.address_var, width=33, font=("Arial", 10), bd=1, relief="solid")
        self.address_entry.grid(row=3, column=1, pady=5, padx=5)

        # Location
        tk.Label(form_frame, text="Location", bg="#ffffff").grid(row=4, column=0, sticky="w", pady=5, padx=5)
        self.location_entry = tk.Entry(form_frame, textvariable=self.location_var, width=33, font=("Arial", 10), bd=1, relief="solid")
        self.location_entry.grid(row=5, column=0, pady=5, padx=5)

        # Buttons
        button_frame = tk.Frame(main_frame, bg="#ffffff")
        button_frame.pack(pady=20)
        tk.Button(button_frame, text="Register", command=self.save_donor, bg="#0d6efd", fg="white", font=("Arial", 12, "bold"), padx=15, pady=5).pack(side="left", padx=10)
        tk.Button(button_frame, text="Cancel", command=lambda: parent.show_frame(DonationEntryPage), bg="#6c757d", fg="white", font=("Arial", 12, "bold"), padx=15, pady=5).pack(side="left", padx=10)

    def save_donor(self):
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()
        address = self.address_var.get().strip()
        location = self.location_var.get().strip()

        if not name or not phone:
            messagebox.showwarning("Input Error", "Name and Phone Number are required.")
            return

        conn = connect_db()
        if conn is None:
            return
        cursor = conn.cursor()

        cursor.execute("SELECT donar_id FROM donar_details WHERE name=%s AND phone_no=%s", (name, phone))
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

        # Auto-return to donation page with name filled
        self.parent.show_frame(DonationEntryPage)
        self.parent.frames[DonationEntryPage].name_var.set(name)

    def clear_fields(self):
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.address_var.set("")
        self.location_var.set("")

# ---------------- PAGE 2: DONATION ENTRY ----------------
class DonationEntryPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f8f9fa", padx=30, pady=30)
        self.parent = parent

        main_frame = tk.Frame(self, bg="#ffffff", padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")

        tk.Label(main_frame, text="DONATION DETAILS", font=("Arial", 18, "bold"), bg="#ffffff", fg="#0d6efd").pack(pady=10)

        # Variables
        self.name_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.payment_var = tk.StringVar()
        self.ref_var = tk.StringVar()
        self.date_var = tk.StringVar(value=datetime.now().strftime("%d-%m-%Y"))

        self.active_categories = self.get_active_categories()
        vcmd = self.register(self.only_positive_numbers)

        form_frame = tk.Frame(main_frame, bg="#ffffff")
        form_frame.pack(padx=20, pady=10)

        # Donor Name Autocomplete
        tk.Label(form_frame, text="Donor Name *", bg="#ffffff").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.name_combobox = ttk.Combobox(form_frame, textvariable=self.name_var, width=33, font=("Arial", 10))
        self.name_combobox.grid(row=1, column=0, pady=5, padx=5)
        self.name_combobox.set("Enter donor name")
        self.name_combobox.bind("<KeyRelease>", self.fetch_donor_matches)

        # Amount
        tk.Label(form_frame, text="Amount *", bg="#ffffff").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        amount_entry = tk.Entry(form_frame, textvariable=self.amount_var, width=33, font=("Arial", 10), bd=1, relief="solid",
                        validate="key", validatecommand=(vcmd, "%P"))
        amount_entry.grid(row=3, column=0, pady=5, padx=5)
        amount_entry.insert(0, "0.00")
        amount_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, amount_entry, "0.00"))
        amount_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, amount_entry, self.amount_var, "0.00"))

        # Category
        tk.Label(form_frame, text="Payment Category *", bg="#ffffff").grid(row=2, column=1, sticky="w", pady=5, padx=5)
        self.category_combobox = ttk.Combobox(form_frame, textvariable=self.category_var, values=self.active_categories, width=30, font=("Arial", 10), state="readonly")
        self.category_combobox.set("Select a category")
        self.category_combobox.grid(row=3, column=1, pady=5, padx=5)

        # Payment Method
        tk.Label(form_frame, text="Payment Method *", bg="#ffffff").grid(row=4, column=0, sticky="w", pady=5, padx=5)
        self.payment_combobox = ttk.Combobox(form_frame, textvariable=self.payment_var, values=["Cash", "UPI", "Card", "Cheque"], width=30, font=("Arial", 10), state="readonly")
        self.payment_combobox.set("Select a method")
        self.payment_combobox.grid(row=5, column=0, pady=5, padx=5)

        # Date
        tk.Label(form_frame, text="Date *", bg="#ffffff").grid(row=4, column=1, sticky="w", pady=5, padx=5)
        self.date_entry = tk.Entry(form_frame, textvariable=self.date_var, width=33, font=("Arial", 10))
        self.date_entry.grid(row=5, column=1, pady=5, padx=5)

        # Reference
        tk.Label(form_frame, text="Ref Number", bg="#ffffff").grid(row=6, column=0, sticky="w", pady=5, padx=5)
        self.ref_entry = tk.Entry(form_frame, textvariable=self.ref_var, width=33, font=("Arial", 10))
        self.ref_entry.grid(row=7, column=0, pady=5, padx=5)

        # Buttons
        button_frame = tk.Frame(main_frame, bg="#ffffff")
        button_frame.pack(fill="x", pady=20)
        tk.Button(button_frame, text="Reset", command=self.clear_fields, bg="#6c757d", fg="white", font=("Arial", 12, "bold")).pack(side="right", padx=10)
        tk.Button(button_frame, text="Submit", command=self.submit_donation, bg="#0d6efd", fg="white", font=("Arial", 12, "bold")).pack(side="right", padx=10)
        tk.Button(button_frame, text="Manage Donors", command=lambda: parent.show_frame(ManageDonorsPage), bg="#d3d3d3").pack(side="left")
        tk.Button(button_frame, text="View All Donations", command=lambda: parent.show_frame(ViewDonationsPage), bg="#198754", fg="white").pack(side="left", padx=5)

    def only_positive_numbers(self, P):
        """
        Allow only positive numbers (integers or decimals) and empty string.
        """
        if P == "":
            return True
        try:
            value = float(P)
            return value >= 0  # only positive numbers
        except ValueError:
            return False

    def get_active_categories(self):
        conn = connect_db()
        categories = []
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT category_name FROM category WHERE active = 1")
            categories = [row[0] for row in cursor.fetchall()]
            conn.close()
        return categories

    def fetch_donor_matches(self, event):
        name = self.name_var.get().strip()
        if len(name) < 3:
            return
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM donar_details WHERE name LIKE %s", (f"%{name}%",))
            results = [row[0] for row in cursor.fetchall()]
            conn.close()
            if results:
                self.name_combobox['values'] = results
            else:
                response = messagebox.askyesno("Donor Not Found", "No matching donor found. Register new donor?")
                if response:
                    self.parent.show_frame(DonorEntryPage)

    def submit_donation(self):
        name = self.name_var.get().strip()
        amount = self.amount_var.get().strip()
        category = self.category_var.get()
        payment_type = self.payment_var.get()
        reference_no = self.ref_var.get().strip()
        date = self.date_var.get().strip()

        if not name or not amount or not category or not payment_type or not date:
            messagebox.showwarning("Input Error", "Please fill all mandatory fields.")
            return

        # Reference required only if not cash
        if payment_type != "Cash" and not reference_no:
            messagebox.showwarning("Input Error", "Reference number is required for non-cash payments.")
            return

        conn = connect_db()
        if conn is None:
            return
        cursor = conn.cursor()

        # Get donor ID
        cursor.execute("SELECT donar_id FROM donar_details WHERE name=%s", (name,))
        result = cursor.fetchone()
        if not result:
            messagebox.showerror("Donor Error", "Donor not found. Please register first.")
            conn.close()
            return
        donor_id = result[0]

        try:
            date_obj = datetime.strptime(date, "%d-%m-%Y").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Date Error", "Enter date in dd-mm-yyyy format.")
            return

        cursor.execute("""
            INSERT INTO receipt_table (donar_id, amount, date, category, payment_type, reference_no)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (donor_id, amount, date_obj, category, payment_type, reference_no if reference_no else None))
        conn.commit()
        receipt_id = cursor.lastrowid
        conn.close()

        self.parent.frames[ReceiptPage].set_receipt_data(receipt_id, name, amount, category, payment_type, reference_no, date)
        self.parent.show_frame(ReceiptPage)

    def clear_fields(self):
        self.name_var.set("Enter donor name")
        self.amount_var.set("0.00")
        self.category_var.set("Select a category")
        self.payment_var.set("Select a method")
        self.ref_var.set("")
        self.date_var.set(datetime.now().strftime("%d-%m-%Y"))

# ---------------- PAGE 3: RECEIPT PAGE ----------------
class ReceiptPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#fff")
        self.parent = parent

        self.title = tk.Label(self, text="Donation Receipt", font=("Arial", 18, "bold"), bg="#fff")
        self.title.pack(pady=15)

        self.text_box = tk.Text(self, width=70, height=20, font=("Courier", 11))
        self.text_box.pack(padx=20, pady=10)

        self.button_frame = tk.Frame(self, bg="#fff")
        self.button_frame.pack(pady=10)

        tk.Button(self.button_frame, text="Back to Home", command=lambda: parent.show_frame(DonationEntryPage),
                  bg="#0d6efd", fg="white", font=("Arial", 12, "bold")).pack(side="left", padx=10)

        self.back_button = tk.Button(self.button_frame, text="Back to Donations", command=lambda: parent.show_frame(ViewDonationsPage),
                                     bg="#6c757d", fg="white", font=("Arial", 12, "bold"))
        self.back_button.pack(side="left", padx=10)
        self.back_button.pack_forget()

    def set_receipt_data(self, rid, name, amount, category, payment, ref, date):
        self.text_box.delete(1.0, tk.END)
        receipt_text = f"""
----------------------------------------------
              DONATION RECEIPT
----------------------------------------------
Receipt ID      : {rid}
Donor Name      : {name}
Category        : {category}
Amount          : ₹{amount}
Payment Type    : {payment}
Reference No    : {ref if ref else 'N/A'}
Date            : {date}
----------------------------------------------
Thank you for your contribution!
----------------------------------------------
"""
        self.text_box.insert(tk.END, receipt_text)

    def show_back_button(self, visible):
        if visible:
            self.back_button.pack(side="left", padx=10)
        else:
            self.back_button.pack_forget()

# ---------------- PAGE 4: VIEW DONATIONS ----------------
class ViewDonationsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f8f9fa")
        self.parent = parent

        tk.Label(self, text="View Donations", font=("Arial", 18, "bold"), bg="#f8f9fa").pack(pady=15)

        date_frame = tk.Frame(self, bg="#f8f9fa")
        date_frame.pack(pady=10)

        self.start_date = tk.StringVar()
        self.end_date = tk.StringVar()

        tk.Label(date_frame, text="Start Date (YYYY-MM-DD):", bg="#f8f9fa").grid(row=0, column=0, padx=5)
        tk.Entry(date_frame, textvariable=self.start_date, width=15).grid(row=0, column=1)
        tk.Label(date_frame, text="End Date (YYYY-MM-DD):", bg="#f8f9fa").grid(row=0, column=2, padx=5)
        tk.Entry(date_frame, textvariable=self.end_date, width=15).grid(row=0, column=3)
        tk.Button(date_frame, text="Search", command=self.search_records, bg="#198754", fg="white").grid(row=0, column=4, padx=10)

        columns = ("Receipt ID", "Donor", "Amount", "Date", "Category", "Payment Type")
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(padx=10, pady=10)

        # Button container frame
        button_frame = tk.Frame(self, bg="#f8f9fa")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Manage Donors", 
                command=lambda: parent.show_frame(ManageDonorsPage), 
                bg="#d3d3d3").pack(side="left", padx=5)

        tk.Button(button_frame, text="View Receipt", 
                command=self.view_selected_receipt, 
                bg="#0d6efd", fg="white").pack(side="left", padx=5)

        tk.Button(button_frame, text="Back to Home", 
                command=lambda: parent.show_frame(DonationEntryPage), 
                bg="#6c757d", fg="white").pack(side="left", padx=5)

    def search_records(self):
        sdate = self.start_date.get()
        edate = self.end_date.get()
        if not sdate or not edate:
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

    def view_selected_receipt(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a donation record to view the receipt.")
            return

        item_data = self.tree.item(selected_item, 'values')
        receipt_id = item_data[0]

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.receipt_id, d.name, r.amount, r.category, r.payment_type, r.reference_no, r.date
                FROM receipt_table r
                JOIN donar_details d ON r.donar_id = d.donar_id
                WHERE r.receipt_id = %s
            """, (receipt_id,))
            record = cursor.fetchone()
            conn.close()

            if record:
                formatted_date = record[6].strftime("%d-%m-%Y") if isinstance(record[6], datetime) else record[6]
                self.parent.frames[ReceiptPage].set_receipt_data(record[0], record[1], record[2], record[3], record[4], record[5], formatted_date)
                self.parent.frames[ReceiptPage].show_back_button(True)
                self.parent.show_frame(ReceiptPage)
            else:
                messagebox.showerror("Error", "Could not retrieve receipt details.")

# ---------------- MAIN APPLICATION ----------------
class DonationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Donation Management System")
        self.geometry("750x600")
        self.configure(bg="#f8f9fa")

        self.frames = {}
        for F in (DonorEntryPage, DonationEntryPage, ReceiptPage, ViewDonationsPage, ManageDonorsPage):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(DonationEntryPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class ManageDonorsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f8f9fa")
        self.parent = parent

        tk.Label(self, text="Manage Donors", font=("Arial", 18, "bold"), bg="#f8f9fa").pack(pady=15)

        # ----------- Form for Add/Update -----------
        form_frame = tk.Frame(self, bg="#ffffff", padx=20, pady=20, relief="raised", bd=2)
        form_frame.pack(padx=10, pady=10, fill="x")

        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.location_var = tk.StringVar()
        self.selected_donor_id = None  # Keep track of donor being edited

        tk.Label(form_frame, text="Name *", bg="#ffffff").grid(row=0, column=0, sticky="w", pady=5)
        tk.Entry(form_frame, textvariable=self.name_var, width=30).grid(row=1, column=0, pady=5)

        tk.Label(form_frame, text="Phone *", bg="#ffffff").grid(row=0, column=1, sticky="w", pady=5)
        tk.Entry(form_frame, textvariable=self.phone_var, width=30).grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Email", bg="#ffffff").grid(row=2, column=0, sticky="w", pady=5)
        tk.Entry(form_frame, textvariable=self.email_var, width=30).grid(row=3, column=0, pady=5)

        tk.Label(form_frame, text="Address", bg="#ffffff").grid(row=2, column=1, sticky="w", pady=5)
        tk.Entry(form_frame, textvariable=self.address_var, width=30).grid(row=3, column=1, pady=5)

        tk.Label(form_frame, text="Location", bg="#ffffff").grid(row=4, column=0, sticky="w", pady=5)
        tk.Entry(form_frame, textvariable=self.location_var, width=30).grid(row=5, column=0, pady=5)

        button_frame = tk.Frame(form_frame, bg="#ffffff")
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)

        tk.Button(button_frame, text="Add / Update", command=self.add_or_update_donor, bg="#0d6efd", fg="white").pack(side="left", padx=5)
        tk.Button(button_frame, text="Clear", command=self.clear_form, bg="#6c757d", fg="white").pack(side="left", padx=5)
        tk.Button(button_frame, text="Back to Donations", command=lambda: parent.show_frame(DonationEntryPage), bg="#198754", fg="white").pack(side="right", padx=5)

        # ----------- Donor Table -----------
        table_frame = tk.Frame(self, bg="#f8f9fa")
        table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        columns = ("Donor ID", "Name", "Phone", "Email", "Address", "Location")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<<TreeviewSelect>>", self.on_row_selected)

        # Delete button
        tk.Button(self, text="Delete Selected Donor", command=self.delete_donor, bg="#dc3545", fg="white").pack(pady=5)

        self.load_donors()

    # ----------- DB Operations -----------

    def load_donors(self):
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT donar_id, name, phone_no, email, address, location FROM donar_details")
            records = cursor.fetchall()
            conn.close()

            for row in self.tree.get_children():
                self.tree.delete(row)
            for rec in records:
                self.tree.insert("", "end", values=rec)

    def on_row_selected(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], 'values')
            self.selected_donor_id = values[0]
            self.name_var.set(values[1])
            self.phone_var.set(values[2])
            self.email_var.set(values[3])
            self.address_var.set(values[4])
            self.location_var.set(values[5])

    def add_or_update_donor(self):
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()
        address = self.address_var.get().strip()
        location = self.location_var.get().strip()

        if not name or not phone:
            messagebox.showwarning("Input Error", "Name and Phone are required.")
            return

        conn = connect_db()
        if conn is None:
            return
        cursor = conn.cursor()

        if self.selected_donor_id:  # Update existing donor
            cursor.execute("""
                UPDATE donar_details SET name=%s, phone_no=%s, email=%s, address=%s, location=%s
                WHERE donar_id=%s
            """, (name, phone, email, address, location, self.selected_donor_id))
            messagebox.showinfo("Success", "Donor updated successfully!")
        else:  # Add new donor
            cursor.execute("""
                INSERT INTO donar_details (name, phone_no, email, address, location)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, phone, email, address, location))
            messagebox.showinfo("Success", "Donor added successfully!")

        conn.commit()
        conn.close()
        self.clear_form()
        self.load_donors()

    def delete_donor(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Select a donor to delete.")
            return
        donor_id = self.tree.item(selected[0], 'values')[0]

        # Check if donor has existing donations
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM receipt_table WHERE donar_id=%s", (donor_id,))
            count = cursor.fetchone()[0]
            if count > 0:
                messagebox.showwarning("Cannot Delete", "This donor has existing donations and cannot be deleted.")
                conn.close()
                return

            response = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this donor?")
            if not response:
                conn.close()
                return

            try:
                cursor.execute("DELETE FROM donar_details WHERE donar_id=%s", (donor_id,))
                conn.commit()
                messagebox.showinfo("Deleted", "Donor deleted successfully!")
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Cannot delete donor: {e}")
            finally:
                conn.close()

        self.clear_form()
        self.load_donors()


    def clear_form(self):
        self.selected_donor_id = None
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.address_var.set("")
        self.location_var.set("")

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app = DonationApp()
    app.mainloop()
