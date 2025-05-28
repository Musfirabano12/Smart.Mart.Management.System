# Smart.Mart.Management.System
Smart Mart is a GUI-based retail management system built with Python and Tkinter. It includes separate roles for Admin and Cashier, enabling product management, cashier management, and a checkout system with payment options.

🚀 Features
✅ Admin Features:
Login with fixed credentials (admin, 1234)

Add new products (Category, Name, Stock)

Add new cashiers (Name, ID, Password)

View all registered cashiers

✅ Cashier Features:
Login using credentials set by admin

View product list with stock levels

Add products to a cart (only if stock is available)

Select payment method: Cash or Card (10% Discount)

Generate bill and store it in bills.txt

🗃 File Structure
bash
Copy
Edit
SmartMart/
│
├── main.py               # Main application file
├── admin.txt             # Stores admin credentials
├── products.txt          # Stores product details (as list of dicts)
├── cashiers.txt          # Stores cashier credentials (as list of dicts)
├── bills.txt             # Stores bill amounts
💾 How to Run
Install Python 3.x (if not already installed)

Open terminal or command prompt in the SmartMart project directory

Run the app:

bash
Copy
Edit
python main.py
🧑‍💼 Admin Login
ID: admin

Password: 1234

Once logged in, the Admin can:

Add/view/edit product inventory

Register new cashiers

👨‍🔧 Cashier Login
Cashiers must be added by Admin first. Once added, a cashier can:

View available products

Add items to cart

Select payment method

Generate bill

💵 Payment Methods
Cash: Full amount

Card: 10% discount on total

Each product is assumed to cost Rs. 100 for demo purposes.

📁 Data Files Format
All records are stored in .txt files using str() and ast.literal_eval() for easy parsing.

products.txt: List of dictionaries like {'category': 'Snacks', 'name': 'Chips', 'stock': 10}

cashiers.txt: List of dictionaries like {'name': 'Ali', 'id': 'ali123', 'password': 'pass'}

bills.txt: Each line records a generated bill like Bill 1: 270

🎨 GUI Design
Built using tkinter

Clean and colorful interface with radio buttons, entries, buttons, and tables

Includes Treeview for displaying products

🔧 Dependencies
Python standard libraries only

tkinter

os

ast

No external installations required.

📌 Future Improvements
Add price field for each product

Allow update/delete of products and cashiers

Save receipts with product details

Login/signup GUI improvement

🧑‍💻 Author
Musfiira Bano
BSSE - 6th Semester
COCIS Department
University Project (SCD Lab)
