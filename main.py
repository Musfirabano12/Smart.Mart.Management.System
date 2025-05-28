# Enhanced Smart Mart System with working Add-to-Cart, Payment Modes, and Colorful GUI
import tkinter as tk
from tkinter import messagebox, ttk
import os
import ast

# File paths
ADMIN_FILE = "admin.txt"
PRODUCTS_FILE = "products.txt"
CASHIERS_FILE = "cashiers.txt"
BILLS_FILE = "bills.txt"

ADMIN_ID = "admin"
ADMIN_PASS = "1234"

def init_files():
    for file in [PRODUCTS_FILE, CASHIERS_FILE, BILLS_FILE]:
        if not os.path.exists(file):
            open(file, 'w').close()
    with open(ADMIN_FILE, 'w') as f:
        f.write(f"{ADMIN_ID},{ADMIN_PASS}")

def read_data(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    if file == BILLS_FILE:
        return lines
    return [ast.literal_eval(line.strip()) for line in lines if line.strip()]

def write_data(file, data):
    with open(file, 'w') as f:
        for record in data:
            f.write(str(record) + "\n")

def append_data(file, record):
    with open(file, 'a') as f:
        f.write(str(record) + "\n")

class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Mart Login")
        self.root.geometry("400x300")
        self.root.configure(bg="#f0f8ff")

        tk.Label(root, text="Smart Mart Login", font=("Helvetica", 18, "bold"), bg="#f0f8ff").pack(pady=20)
        tk.Label(root, text="Login ID:", bg="#f0f8ff").pack()
        self.id_entry = tk.Entry(root)
        self.id_entry.pack()
        tk.Label(root, text="Password:", bg="#f0f8ff").pack()
        self.pass_entry = tk.Entry(root, show='*')
        self.pass_entry.pack()
        tk.Button(root, text="Login", bg="#008080", fg="white", command=self.login).pack(pady=15)

    def login(self):
        uid = self.id_entry.get()
        pwd = self.pass_entry.get()
        with open(ADMIN_FILE, 'r') as f:
            stored_id, stored_pwd = f.read().split(',')
        if uid == stored_id and pwd == stored_pwd:
            self.root.destroy()
            AdminPanel()
        else:
            cashiers = read_data(CASHIERS_FILE)
            for c in cashiers:
                if c['id'] == uid and c['password'] == pwd:
                    self.root.destroy()
                    CashierPanel(c['name'])
                    return
            messagebox.showerror("Error", "Invalid credentials")

class AdminPanel:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Admin Panel")
        self.root.geometry("400x400")
        self.root.configure(bg="#e6f2ff")

        tk.Label(self.root, text="Admin Dashboard", font=("Arial", 20, "bold"), bg="#e6f2ff").pack(pady=10)
        tk.Button(self.root, text="Manage Products", command=self.manage_products, bg="#4682B4", fg="white").pack(pady=10)
        tk.Button(self.root, text="Manage Cashiers", command=self.manage_cashiers, bg="#4682B4", fg="white").pack(pady=10)

        self.root.mainloop()

    def manage_products(self):
        Manager(PRODUCTS_FILE, ["category", "name", "stock", "price"])

    def manage_cashiers(self):
        Manager(CASHIERS_FILE, ["name", "id", "password"])

class Manager:
    def __init__(self, file, fields):
        self.file = file
        self.fields = fields
        self.data = read_data(file)

        self.win = tk.Toplevel()
        self.win.title("Manage Records")
        self.entries = {}

        for field in fields:
            tk.Label(self.win, text=field.capitalize()).pack()
            entry = tk.Entry(self.win)
            entry.pack()
            self.entries[field] = entry

        tk.Button(self.win, text="Add", command=self.add).pack()
        tk.Button(self.win, text="Update", command=self.update).pack()
        tk.Button(self.win, text="Delete", command=self.delete).pack()
        tk.Button(self.win, text="View All", command=self.view_all).pack()

    def add(self):
        try:
            record = {f: (int(self.entries[f].get()) if f in ["stock", "price"] else self.entries[f].get()) for f in self.fields}
            self.data.append(record)
            write_data(self.file, self.data)
            messagebox.showinfo("Success", "Record added")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update(self):
        id_field = self.fields[1]
        target_id = self.entries[id_field].get()
        for record in self.data:
            if str(record[id_field]) == target_id:
                for f in self.fields:
                    value = self.entries[f].get()
                    record[f] = int(value) if f in ["stock", "price"] else value
                write_data(self.file, self.data)
                messagebox.showinfo("Updated", "Record updated")
                return
        messagebox.showerror("Not Found", f"{id_field} not found")

    def delete(self):
        id_field = self.fields[1]
        target_id = self.entries[id_field].get()
        self.data = [r for r in self.data if str(r[id_field]) != target_id]
        write_data(self.file, self.data)
        messagebox.showinfo("Deleted", "Record deleted")

    def view_all(self):
        messagebox.showinfo("Records", "\n".join(str(r) for r in self.data))

class CashierPanel:
    def __init__(self, name):
        self.root = tk.Tk()
        self.root.title("Cashier Panel")
        self.root.geometry("500x500")
        self.root.configure(bg="#f5fff5")

        self.cart = []
        self.products = read_data(PRODUCTS_FILE)

        tk.Label(self.root, text=f"Welcome {name}", font=("Arial", 16), bg="#f5fff5").pack(pady=10)

        tk.Label(self.root, text="Select Category", bg="#f5fff5").pack()
        self.category_var = tk.StringVar()
        self.category_menu = ttk.Combobox(self.root, textvariable=self.category_var, state="readonly")
        self.category_menu['values'] = list(set(p['category'] for p in self.products))
        self.category_menu.pack()
        self.category_menu.bind("<<ComboboxSelected>>", self.update_products)

        tk.Label(self.root, text="Select Product", bg="#f5fff5").pack()
        self.product_var = tk.StringVar()
        self.product_menu = ttk.Combobox(self.root, textvariable=self.product_var, state="readonly")
        self.product_menu.pack()

        tk.Label(self.root, text="Enter Quantity", bg="#f5fff5").pack()
        self.qty_entry = tk.Entry(self.root)
        self.qty_entry.pack()

        tk.Button(self.root, text="Add to Cart", bg="#32CD32", fg="white", command=self.add_to_cart).pack(pady=10)

        tk.Label(self.root, text="Select Payment Method", bg="#f5fff5").pack()
        self.payment_var = tk.StringVar(value="Cash")
        tk.Radiobutton(self.root, text="Cash", variable=self.payment_var, value="Cash", bg="#f5fff5").pack()
        tk.Radiobutton(self.root, text="Card (10% off)", variable=self.payment_var, value="Card", bg="#f5fff5").pack()

        tk.Button(self.root, text="Generate Bill", bg="#FFA500", fg="white", command=self.generate_bill).pack(pady=10)

        self.root.mainloop()

    def update_products(self, event):
        category = self.category_var.get()
        products = [p['name'] for p in self.products if p['category'] == category]
        self.product_menu['values'] = products
        self.product_menu.set("")

    def add_to_cart(self):
        prod_name = self.product_var.get()
        if not prod_name:
            messagebox.showerror("Error", "Please select a product")
            return
        try:
            qty = int(self.qty_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity")
            return

        for product in self.products:
            if product['name'] == prod_name:
                if product['stock'] >= qty:
                    product['stock'] -= qty
                    self.cart.append({'name': product['name'], 'price': product['price'], 'qty': qty})
                    write_data(PRODUCTS_FILE, self.products)
                    messagebox.showinfo("Added", f"{prod_name} x{qty} added to cart")
                    return
                else:
                    messagebox.showerror("Error", "Insufficient stock")
                    return
        messagebox.showerror("Error", "Product not found")

    def generate_bill(self):
        if not self.cart:
            messagebox.showerror("Error", "Cart is empty")
            return
        total = sum(item['price'] * item['qty'] for item in self.cart)
        if self.payment_var.get() == "Card":
            total *= 0.9
        total = round(total, 2)
        bill_number = len(read_data(BILLS_FILE)) + 1
        receipt = f"Bill {bill_number}:\n"
        for item in self.cart:
            receipt += f"{item['name']} x{item['qty']} @ Rs.{item['price']} = Rs.{item['price']*item['qty']}\n"
        receipt += f"Total: Rs.{total}\nPayment Mode: {self.payment_var.get()}"
        append_data(BILLS_FILE, receipt)
        messagebox.showinfo("Receipt", receipt)
        self.cart.clear()

if __name__ == "__main__":
    init_files()
    root = tk.Tk()
    LoginScreen(root)
    root.mainloop()
