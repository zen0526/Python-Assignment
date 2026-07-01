def customer_logged_in_menu(username):
    cart = []
    while True:
        print(f"\n--- Welcome, {username}! (Customer Menu) ---")
        print("1. View Menu")
        print("2. Add Item to Cart")
        print("3. View Cart")
        print("4. Place Order")
        print("5. View Order Status")
        print("6. Leave a Review")
        print("0. Log Out")
        choice = input("Please enter your selection: ")

        if choice == "1":
            view_menu()
        elif choice == "2":
            add_to_cart(cart)
        elif choice == "3":
            view_cart(cart)
        elif choice == "4":
            place_order(username, cart)
        elif choice == "5":
            view_order_status(username)
        elif choice == "6":
            leave_review(username)
        elif choice == "0":
            print("Logged out.")
            break
        else:
            print("Invalid choice.")


def load_menu_from_txt(filename):
    menu_items = {}
    try:
        with open(filename, "r") as file:
            current_category = None
            for line in file:
                line = line.strip()
                if not line:
                    continue
                if line.startswith("[") and line.endswith("]"):
                    current_category = line[1:-1]
                    menu_items[current_category] = {}
                else:
                    try:
                        code, name, price = line.split("|")
                        menu_items[current_category][code.strip()] = {
                            "name": name.strip(),
                            "price": float(price.strip())
                        }
                    except ValueError:
                        print(f"Invalid line format: {line}")
    except FileNotFoundError:
        print(f"Menu file '{filename}' not found.")
    return menu_items


def get_discounted_price(item_name, original_price):
    try:
        with open("discounts.txt", "r") as f:
            discounts = {
                line.strip().split(",")[0].upper(): float(line.strip().split(",")[1])
                for line in f if "," in line
            }
    except FileNotFoundError:
        discounts = {}

    discount = discounts.get(item_name.upper(), 0)
    return original_price * (1 - discount / 100)


def view_menu():
    menu_items = load_menu_from_txt("menu.txt")

    try:
        with open("unavailable_items.txt", "r") as f:
            unavailable_ids = {line.strip().upper() for line in f}
    except FileNotFoundError:
        unavailable_ids = set()

    try:
        with open("discounts.txt", "r") as f:
            discounts = {
                line.strip().split(",")[0].upper(): float(line.strip().split(",")[1])
                for line in f if "," in line
            }
    except FileNotFoundError:
        discounts = {}

    print("\n========== Menu ==========")
    for category, items in menu_items.items():
        has_available = any(code not in unavailable_ids for code in items)
        if not has_available:
            continue

        print(f"\n{category}")
        print(f"{'Code':<6} {'Item':<30} {'Price':>8}")
        print("-" * 50)

        for code, info in items.items():
            if code.upper() in unavailable_ids:
                continue
            name = info["name"]
            price = info["price"]
            discount_percent = discounts.get(name.upper(), 0)
            final_price = price * (1 - discount_percent / 100)
            if discount_percent > 0:
                print(f"{code:<6} {name:<30} RM{final_price:>6.2f}  ({discount_percent}% off)")
            else:
                print(f"{code:<6} {name:<30} RM{price:>6.2f}")
    print("=" * 50)


def add_to_cart(cart):
    menu_items = load_menu_from_txt("menu.txt")

    try:
        with open("unavailable_items.txt", "r") as f:
            unavailable_ids = {line.strip().upper() for line in f}
    except FileNotFoundError:
        unavailable_ids = set()

    view_menu()
    print("Enter item code to add, or type 'done' to finish.")

    while True:
        item_code = input("Enter item code: ").upper()
        if item_code == "DONE":
            print("Finished adding items to cart.")
            break

        found = False
        for category in menu_items.values():
            if item_code in category:
                if item_code in unavailable_ids:
                    print("Sorry, this item is out of stock.")
                    found = True
                    break
                item = category[item_code]
                discounted_price = get_discounted_price(item["name"], item["price"])
                cart.append((item["name"], discounted_price))
                print(f"Added {item['name']} to cart at RM{discounted_price:.2f}.")
                found = True
                break

        if not found:
            print("The corresponding code was not found. Please try again.")


def view_cart(cart):
    if not cart:
        print("Your cart is currently empty.")
        return

    while True:
        print("\n--- Your Cart ---")
        total = 0
        for i, (item, price) in enumerate(cart, start=1):
            print(f"{i}. {item:<25} RM{price:>5.2f}")
            total += price
        print(f"\n Total: RM{total:.2f}")

        print("\nOptions:")
        print("Enter the item number to remove it from cart")
        print("Type 'done' to exit cart view")

        choice = input("Your choice: ").lower()
        if choice == "done":
            break
        elif choice.isdigit():
            index = int(choice)
            if 1 <= index <= len(cart):
                removed_item = cart.pop(index - 1)
                print(f"Removed {removed_item[0]} from cart.")
            else:
                print("Invalid item number.")
        else:
            print("Invalid input. Please try again.")


def place_order(username, cart):
    if not cart:
        print("Cart is empty. Please add items before placing an order.")
        return

    print("\n--- Your Order Summary ---")
    total = 0
    for item, price in cart:
        print(f"{item:<25} RM{price:>5.2f}")
        total += price
    print(f"\nTotal: RM{total:.2f}")

    confirm = input("Confirm order? (yes/no): ").lower()
    if confirm != "yes":
        print("Order cancelled. You can continue editing your cart.")
        return

    try:
        with open("Customer_Orders.txt", "a") as file:
            for item, price in cart:
                file.write(f"{username},{item},{price:.2f},New\n")
        cart.clear()
        print("Your order has been placed successfully!")
    except Exception as e:
        print(f"Error writing order: {e}")


def view_order_status(username):
    print("\n--- Your Orders ---")
    try:
        with open("Customer_Orders.txt", "r") as file:
            user_orders = []
            for line in file:
                parts = line.strip().split(",")
                if len(parts) != 4:
                    continue
                order_username, item, price_str, status = parts
                if order_username == username:
                    try:
                        price = float(price_str)
                    except ValueError:
                        price = 0.0
                    user_orders.append((item, price, status))

            if not user_orders:
                print("No orders found.")
                return

            total = 0
            for i, (item, price, status) in enumerate(user_orders, start=1):
                total += price
                print(f"{i}. {item:<25} RM{price:>6.2f}   Status: {status}")

            print(f"\nTotal value of orders: RM{total:.2f}")

    except FileNotFoundError:
        print("No orders found.")


def leave_review(username):
    review = input("Enter your review: ")
    with open("Customer_Reviews.txt", "a") as file:
        file.write(f"{username},{review}\n")
    print("Thank you for your feedback!")