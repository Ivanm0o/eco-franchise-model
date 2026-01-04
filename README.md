ECO-FRANCHISE-MODEL FUNCTIONALITIES

1. Menu Class
   - Parameters: name, items, start_time, end_time
   - __repr__: Displays menu name and availability
   - calculate_bill(purchased_items): Returns total cost of selected items

2. Franchise Class
   - Parameters: address, menus, is_mall (optional)
   - __repr__: Displays franchise address
   - available_menus(time): Returns menus available at given time
   - If is_mall=True: Prices increase by 10% automatically

3. Business Class
   - Parameters: name, list of franchises
   - Represents the EcoMarket brand grouping multiple franchises

4. Product Catalog
   - Contains 20 eco-friendly products with base prices
   - Examples: organic apples, quinoa, almond milk, vegan burger, kombucha, eco nuggets, etc.

5. Menus
   - Morning Market: fruits, drinks, breakfast items
   - Afternoon Specials: vegan meals, salads, soups
   - Evening Dinners: sustainable dishes, wine, pasta
   - Kids EcoMenu: healthy snacks and juices

6. Franchises
   - Flagship Store: full menu access
   - Mall Branch: limited menus, prices increased by 10%
   - Suburb Branch: selected menus, standard pricing

7. Business
   - EcoMarket: umbrella brand for all franchises

8. Usage Examples
   - Print menu availability by time
   - Calculate bills for customer purchases
   - Compare pricing between mall and non-mall franchises
   - Simulate real-world business logic with Python OOP
