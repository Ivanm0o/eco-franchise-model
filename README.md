# Eco-Franchise POS System

A Python-based Point of Sale (POS) desktop application built with Tkinter. This system manages sales for a sustainable business ("EcoMarket") operating multiple franchises with distinct pricing strategies and time-based menus.

## 📋 Overview

The application separates business logic (Backend classes) from the user interface (Frontend Tkinter). It allows cashiers to select store locations, view specific menus tailored to the time of day, build a shopping cart, and process transactions, generating persistent logs.

## ✨ Key Functionalities

### 1. Dynamic Business Logic
* **Franchise Management:** Handles different store locations.
* **Smart Pricing Engine:** Implements specific pricing rules. For example, the "Central Mall" branch automatically applies a **10% markup** to all base catalog prices upon initialization.
* **Time-Based Menus:** Products are organized into distinct menus (e.g., "Morning Market", "Evening Dinners") available only during specific time slots.

### 2. Interactive User Interface (GUI)
* **Store Configuration:** Dropdown selectors (Combobox) to switch between franchises and menus dynamically. Changing the franchise automatically clears the cart to ensure correct pricing.
* **Product Browser:** Displays available items and their specific prices in a professional table view (Treeview) based on the active menu.
* **Shopping Cart Management:**
    * **Add to Cart:** Move items from the product browser to the cart.
    * **Remove Selected:** Remove individual items from the cart.
    * **Clear Cart:** Empty the entire cart instantly.
* **Real-Time Totals:** The total cost is recalculated and displayed immediately after any cart modification.

### 3. Transaction Processing
* **Cart Validation:** Prevents checkout if the cart is empty.
* **Receipt Generation:** Generates a detailed, formatted text receipt including timestamp, store location, itemized list, and final total.
* **Persistent Logging:** Saves receipts automatically to a local text file (`transactions_log.txt`), appending new sales without overwriting previous data.

## 🔧 Technical Structure

* **Backend (Model):**
    * `Menu Class`: Defines lists of items and their prices within specific time windows. Handles bill calculation.
    * `Franchise Class`: Represents a store. Creates deep copies of menus to apply location-specific price adjustments (like mall taxes) independent of other stores.
    * `Business Class`: Aggregates franchises.
* **Frontend (View/Controller):**
    * `EcoApp Class (tk.Tk)`: The main window managing widgets, user events, and connection to the backend logic. Uses `ttk.Treeview` for tabular data display.

## 🚀 How to Run

1.  Ensure Python 3.x is installed.
2.  No external libraries are required (uses standard `tkinter`, `copy`, `datetime`).
3.  Run the script:
    ```bash
    eco-franchise-model.py
    ```
