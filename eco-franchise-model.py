import tkinter as tk
from tkinter import ttk, messagebox
import copy
import datetime

# ---------------------------------------------------------
# 1. BUSINESS LOGIC (BACKEND)
# ---------------------------------------------------------

class Menu:
    def __init__(self, name, items, start_time, end_time):
        self.name = name
        self.items = items
        self.start_time = start_time
        self.end_time = end_time

    def calculate_bill(self, purchased_items):
        total = 0
        for item_name in purchased_items:
            # Look up price in the items dictionary
            if item_name in self.items:
                total += self.items[item_name]
        return total

class Franchise:
    def __init__(self, address, menus, is_mall=False):
        self.address = address
        # Deepcopy is vital here to avoid reference issues
        self.menus = [copy.deepcopy(m) for m in menus]
        self.is_mall = is_mall

        # Mall pricing logic (+10%)
        if self.is_mall:
            for menu in self.menus:
                menu.items = {k: round(v * 1.1, 2) for k, v in menu.items.items()}

    def __repr__(self):
        return self.address

class Business:
    def __init__(self, name, franchises):
        self.name = name
        self.franchises = franchises

# --- DATA CATALOG (ENGLISH) ---
catalog = {
    'organic apples': 2.50, 'bananas': 1.80, 'avocados': 3.00, 'quinoa': 5.50,
    'almond milk': 4.20, 'soy milk': 3.80, 'eco bread': 2.80, 'vegan burger': 7.50,
    'eco salad': 6.00, 'organic soup': 5.50, 'kombucha': 3.50, 'fair-trade coffee': 2.50,
    'green tea': 2.00, 'organic wine': 15.00, 'sustainable pasta': 8.50,
    'vegan pizza': 10.00, 'eco nuggets': 5.00, 'fruit juice': 2.50,
    'mini veggie wrap': 4.50, 'granola bar': 1.50
}

# Menu Definitions
morning_market = Menu("Morning Market", 
    {k: catalog[k] for k in ['organic apples','bananas','almond milk','eco bread','fair-trade coffee','green tea','granola bar']}, 
    "8am","12pm")

afternoon_specials = Menu("Afternoon Specials", 
    {k: catalog[k] for k in ['vegan burger','eco salad','quinoa','organic soup','kombucha','fruit juice']}, 
    "12pm","5pm")

evening_dinners = Menu("Evening Dinners", 
    {k: catalog[k] for k in ['sustainable pasta','vegan pizza','organic wine','eco salad','organic soup']}, 
    "5pm","10pm")

kids_menu = Menu("Kids EcoMenu", 
    {k: catalog[k] for k in ['eco nuggets','fruit juice','mini veggie wrap','granola bar']}, 
    "11am","8pm")

# Franchise Definitions
flagship_store = Franchise("45 Green Street (Flagship)", [morning_market, afternoon_specials, evening_dinners, kids_menu])
mall_branch = Franchise("Central Mall (Mall Pricing)", [morning_market, afternoon_specials, kids_menu], is_mall=True)
suburb_branch = Franchise("Suburb Eco Plaza", [morning_market, evening_dinners, kids_menu])

# Business Setup
eco_business = Business("EcoMarket", [flagship_store, mall_branch, suburb_branch])


# ---------------------------------------------------------
# 2. GRAPHICAL USER INTERFACE (FRONTEND)
# ---------------------------------------------------------

class EcoApp(tk.Tk):
    def __init__(self, business):
        super().__init__()
        self.business = business
        self.title(f"POS System v2.0 - {self.business.name}")
        self.geometry("950x600")

        # State Variables
        self.current_franchise = None
        self.current_menu = None
        self.cart = [] # List of item names

        self.create_widgets()

    def create_widgets(self):
        # --- Styles ---
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        style.configure("TButton", padding=5)

        # --- Top Frame (Configuration) ---
        top_frame = ttk.LabelFrame(self, text="Store Configuration", padding=15)
        top_frame.pack(fill="x", padx=10, pady=5)

        top_frame.columnconfigure(1, weight=1)
        top_frame.columnconfigure(3, weight=1)

        ttk.Label(top_frame, text="Franchise Location:").grid(row=0, column=0, sticky="w")
        self.combo_franchise = ttk.Combobox(top_frame, values=self.business.franchises, state="readonly")
        self.combo_franchise.grid(row=0, column=1, sticky="ew", padx=5)
        self.combo_franchise.bind("<<ComboboxSelected>>", self.update_menu_options)

        ttk.Label(top_frame, text="Active Menu:").grid(row=0, column=2, sticky="w")
        self.combo_menu = ttk.Combobox(top_frame, state="readonly")
        self.combo_menu.grid(row=0, column=3, sticky="ew", padx=5)
        self.combo_menu.bind("<<ComboboxSelected>>", self.update_items_display)

        # --- Middle Frame (Tables) ---
        middle_frame = tk.Frame(self)
        middle_frame.pack(expand=True, fill="both", padx=10, pady=5)

        # LEFT PANEL: Available Products
        left_panel = ttk.LabelFrame(middle_frame, text="Available Products", padding=5)
        left_panel.pack(side="left", expand=True, fill="both", padx=5)

        columns_products = ('item', 'price')
        self.tree_products = ttk.Treeview(left_panel, columns=columns_products, show='headings')
        self.tree_products.heading('item', text='Item Name')
        self.tree_products.heading('price', text='Price ($)')
        self.tree_products.column('price', width=80, anchor='center')
        
        scrollbar_prod = ttk.Scrollbar(left_panel, orient=tk.VERTICAL, command=self.tree_products.yview)
        self.tree_products.configure(yscroll=scrollbar_prod.set)
        scrollbar_prod.pack(side="right", fill="y")
        self.tree_products.pack(side="left", expand=True, fill="both")

        btn_frame_left = tk.Frame(left_panel)
        btn_frame_left.pack(side="bottom", fill="x", pady=5)
        ttk.Button(btn_frame_left, text="Add to Cart ➜", command=self.add_to_cart).pack(fill="x")


        # RIGHT PANEL: Shopping Cart
        right_panel = ttk.LabelFrame(middle_frame, text="Shopping Cart", padding=5)
        right_panel.pack(side="right", expand=True, fill="both", padx=5)

        columns_cart = ('item', 'price')
        self.tree_cart = ttk.Treeview(right_panel, columns=columns_cart, show='headings')
        self.tree_cart.heading('item', text='Item Name')
        self.tree_cart.heading('price', text='Price ($)')
        self.tree_cart.column('price', width=80, anchor='center')

        scrollbar_cart = ttk.Scrollbar(right_panel, orient=tk.VERTICAL, command=self.tree_cart.yview)
        self.tree_cart.configure(yscroll=scrollbar_cart.set)
        scrollbar_cart.pack(side="right", fill="y")
        self.tree_cart.pack(side="left", expand=True, fill="both")

        btn_frame_right = tk.Frame(right_panel)
        btn_frame_right.pack(side="bottom", fill="x", pady=5)
        ttk.Button(btn_frame_right, text="Remove Selected", command=self.remove_selected).pack(fill="x", pady=2)
        ttk.Button(btn_frame_right, text="Clear Cart", command=self.clear_cart).pack(fill="x", pady=2)


        # --- Bottom Frame (Totals & Checkout) ---
        bottom_frame = tk.Frame(self, bg="#e1e1e1", height=60)
        bottom_frame.pack(fill="x", padx=10, pady=10)

        self.lbl_total = tk.Label(bottom_frame, text="TOTAL: $0.00", font=("Consolas", 20, "bold"), bg="#e1e1e1", fg="#2e7d32")
        self.lbl_total.pack(side="right", padx=20, pady=10)

        checkout_btn = tk.Button(bottom_frame, text="✅ CHECKOUT / PAY", font=("Arial", 12, "bold"), bg="#4caf50", fg="white", command=self.checkout)
        checkout_btn.pack(side="left", padx=20, pady=10)


    # --- Logic ---

    def update_menu_options(self, event):
        idx = self.combo_franchise.current()
        self.current_franchise = self.business.franchises[idx]
        self.combo_menu['values'] = self.current_franchise.menus
        self.combo_menu.current(0)
        self.update_items_display(None)
        self.clear_cart() 

    def update_items_display(self, event):
        idx = self.combo_menu.current()
        if idx >= 0:
            self.current_menu = self.current_franchise.menus[idx]
            
            # Clear Treeview
            for i in self.tree_products.get_children():
                self.tree_products.delete(i)
            
            # Insert Data
            for item, price in self.current_menu.items.items():
                self.tree_products.insert('', tk.END, values=(item, f"{price:.2f}"))

    def add_to_cart(self):
        selected_item = self.tree_products.selection()
        if not selected_item:
            return

        item_values = self.tree_products.item(selected_item)['values']
        name = item_values[0]
        price = float(item_values[1])

        self.cart.append(name) 
        self.tree_cart.insert('', tk.END, values=(name, f"{price:.2f}"))
        
        self.update_total()

    def remove_selected(self):
        selected_item = self.tree_cart.selection()
        if not selected_item:
            return
        
        for item in selected_item:
            self.tree_cart.delete(item)
        
        # Rebuild cart list from visual table to keep sync
        self.cart = []
        for child in self.tree_cart.get_children():
            val = self.tree_cart.item(child)['values']
            self.cart.append(val[0])
            
        self.update_total()

    def clear_cart(self):
        self.cart = []
        for i in self.tree_cart.get_children():
            self.tree_cart.delete(i)
        self.update_total()

    def update_total(self):
        if self.current_menu:
            total = self.current_menu.calculate_bill(self.cart)
            self.lbl_total.config(text=f"TOTAL: ${total:.2f}")
            return total
        return 0

    def checkout(self):
        if not self.cart:
            messagebox.showwarning("Error", "The cart is empty.")
            return
        
        total = self.update_total()
        
        # Generate Receipt text
        receipt_text = f"--- RECEIPT ---\n"
        receipt_text += f"Date:  {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        receipt_text += f"Store: {self.current_franchise.address}\n"
        receipt_text += "-"*25 + "\n"
        for item in self.cart:
            price = self.current_menu.items.get(item, 0)
            receipt_text += f"{item:<25} ${price:.2f}\n"
        receipt_text += "-"*25 + "\n"
        receipt_text += f"TOTAL:                    ${total:.2f}\n"
        receipt_text += "=========================\n"

        self.save_receipt(receipt_text)
        
        messagebox.showinfo("Payment Successful", f"Purchase recorded.\nTotal: ${total:.2f}")
        self.clear_cart()

    def save_receipt(self, text):
        with open("transactions_log.txt", "a", encoding='utf-8') as f:
            f.write(text + "\n\n")

if __name__ == "__main__":
    app = EcoApp(eco_business)
    app.mainloop()
