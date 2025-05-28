import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import os
import ast

# File paths
ADMIN_FILE = "admin.txt"
PRODUCTS_FILE = "products.txt"
CASHIERS_FILE = "cashiers.txt"
BILLS_FILE = "bills.txt"

# Admin credentials (hardcoded)
ADMIN_ID = "admin"
ADMIN_PASS = "1234"

# Ensure data files exist
def init_files():
    for file in [PRODUCTS_FILE, CASHIERS_FILE, BILLS_FILE]:
        if not os.path.exists(file):
            open(file, 'w').close()
    with open(ADMIN_FILE, 'w') as f:
        f.write(f"{ADMIN_ID},{ADMIN_PASS}")

# Helper functions to manage .txt data
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

# GUI Classes
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

        tk.Button(root, text="Login", font=("Arial", 12), bg="#00ced1", fg="white", command=self.login).pack(pady=15)

    def login(self):
        uid = self.id_entry.get()
        pwd = self.pass_entry.get()
        try:
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
        except Exception as e:
            messagebox.showerror("Error", str(e))

class AdminPanel:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Admin Panel")
        self.root.geometry("600x500")
        self.root.configure(bg="#faf0e6")

        tk.Label(self.root, text="Admin Dashboard", font=("Arial", 20, "bold"), bg="#faf0e6").pack(pady=10)

        tk.Button(self.root, text="Manage Products", font=("Arial", 12), bg="#4682b4", fg="white", command=self.manage_products).pack(pady=5)
        tk.Button(self.root, text="Manage Cashiers", font=("Arial", 12), bg="#4682b4", fg="white", command=self.manage_cashiers).pack(pady=5)
        tk.Button(self.root, text="View Cashiers", font=("Arial", 12), bg="#4682b4", fg="white", command=self.view_cashiers).pack(pady=5)

        self.root.mainloop()

    def manage_products(self):
        ProductsWindow()

    def manage_cashiers(self):
        CashierManager()

    def view_cashiers(self):
        cashiers = read_data(CASHIERS_FILE)
        messagebox.showinfo("Cashiers", "\n".join([f"{c['name']} ({c['id']})" for c in cashiers]))

class ProductsWindow:
    def __init__(self):
        self.win = tk.Toplevel()
        self.win.title("Manage Products")
        self.win.geometry("500x400")
        self.win.configure(bg="#fffaf0")

        self.products = read_data(PRODUCTS_FILE)

        tk.Label(self.win, text="Category:").pack()
        self.category = tk.Entry(self.win)
        self.category.pack()
        tk.Label(self.win, text="Product Name:").pack()
        self.name = tk.Entry(self.win)
        self.name.pack()
        tk.Label(self.win, text="Stock:").pack()
        self.stock = tk.Entry(self.win)
        self.stock.pack()

        tk.Button(self.win, text="Add Product", bg="#32cd32", fg="white", command=self.add_product).pack(pady=5)

    def add_product(self):
        try:
            cat = self.category.get()
            name = self.name.get()
            stock = int(self.stock.get())
            self.products.append({'category': cat, 'name': name, 'stock': stock})
            write_data(PRODUCTS_FILE, self.products)
            messagebox.showinfo("Success", "Product added")
        except Exception as e:
            messagebox.showerror("Error", str(e))

class CashierManager:
    def __init__(self):
        self.win = tk.Toplevel()
        self.win.title("Manage Cashiers")
        self.win.geometry("500x400")
        self.win.configure(bg="#f5fffa")

        self.cashiers = read_data(CASHIERS_FILE)

        tk.Label(self.win, text="Cashier Name:").pack()
        self.name = tk.Entry(self.win)
        self.name.pack()
        tk.Label(self.win, text="Cashier ID:").pack()
        self.uid = tk.Entry(self.win)
        self.uid.pack()
        tk.Label(self.win, text="Password:").pack()
        self.pwd = tk.Entry(self.win)
        self.pwd.pack()

        tk.Button(self.win, text="Add Cashier", bg="#8a2be2", fg="white", command=self.add_cashier).pack(pady=5)

    def add_cashier(self):
        try:
            name = self.name.get()
            uid = self.uid.get()
            pwd = self.pwd.get()
            self.cashiers.append({'name': name, 'id': uid, 'password': pwd})
            write_data(CASHIERS_FILE, self.cashiers)
            messagebox.showinfo("Success", "Cashier added")
        except Exception as e:
            messagebox.showerror("Error", str(e))

class CashierPanel:
    def __init__(self, name):
        self.root = tk.Tk()
        self.root.title("Cashier Panel")
        self.root.geometry("700x600")
        self.root.configure(bg="#e6e6fa")
        self.cart = []

        tk.Label(self.root, text=f"Welcome {name}", font=("Arial", 16), bg="#e6e6fa").pack(pady=10)

        self.products = read_data(PRODUCTS_FILE)
        self.tree = ttk.Treeview(self.root, columns=('Category', 'Name', 'Stock'), show='headings')
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
        self.tree.pack()

        self.load_products()

        tk.Button(self.root, text="Add Selected Product to Cart", bg="#00bfff", fg="white", command=self.add_to_cart).pack(pady=10)

        self.payment_var = tk.StringVar()
        tk.Label(self.root, text="Select Payment Method:", bg="#e6e6fa").pack()
        tk.Radiobutton(self.root, text="Cash", variable=self.payment_var, value="Cash", bg="#e6e6fa").pack()
        tk.Radiobutton(self.root, text="Card (10% off)", variable=self.payment_var, value="Card", bg="#e6e6fa").pack()

        tk.Button(self.root, text="Generate Bill", bg="#3cb371", fg="white", command=self.generate_bill).pack(pady=10)
        self.root.mainloop()

    def load_products(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for item in self.products:
            self.tree.insert('', tk.END, values=(item['category'], item['name'], item['stock']))

    def add_to_cart(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "No product selected")
            return
        item_values = self.tree.item(selected[0])['values']
        for item in self.products:
            if item['name'] == item_values[1] and item['stock'] > 0:
                self.cart.append(item)
                item['stock'] -= 1
                write_data(PRODUCTS_FILE, self.products)
                self.load_products()
                messagebox.showinfo("Added", f"{item['name']} added to cart")
                return
        messagebox.showerror("Error", "Product out of stock")

    def generate_bill(self):
        if not self.cart:
            messagebox.showerror("Error", "Cart is empty")
            return
        total = 100 * len(self.cart)
        payment_method = self.payment_var.get()
        if payment_method == "Card":
            total *= 0.9
        total = int(total)
        bill_lines = read_data(BILLS_FILE)
        bill_number = len(bill_lines) + 1
        append_data(BILLS_FILE, f"Bill {bill_number}: {total}")
        messagebox.showinfo("Bill", f"Payment Received. Total = Rs. {total}")
        self.cart.clear()
        self.load_products()

if __name__ == "__main__":
    init_files()
    root = tk.Tk()
    app = LoginScreen(root)
    root.mainloop()
