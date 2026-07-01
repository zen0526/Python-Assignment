import datetime
from collections import Counter


# === FILE HELPERS ===
def get_food_names():
    food_names = set()
    try:
        with open("menu.txt", "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("[") or not line or "|" not in line:
                    continue
                parts = line.split("|")
                if len(parts) >= 3:
                    food_names.add(parts[1].strip().upper())
    except FileNotFoundError:
        pass
    return food_names


def get_unavailable_names():
    try:
        with open("unavailable_items.txt", "r") as f:
            return {line.strip().upper() for line in f}
    except FileNotFoundError:
        return set()


def get_discounts_dict():
    try:
        with open("discounts.txt", "r") as f:
            return {
                line.strip().split(",")[0].upper(): line.strip().split(",")[1]
                for line in f if "," in line
            }
    except FileNotFoundError:
        return {}


# === MENU DISPLAY ===
def render_product_list():
    print("=" * 89)
    print(" " * 38 + "Restaurant Menu")
    print("=" * 89)
    print(" " * 89)

    try:
        with open("unavailable_items.txt", "r") as f:
            unavailable_ids = {line.strip().upper() for line in f}
    except FileNotFoundError:
        unavailable_ids = set()

    try:
        with open("discounts.txt", "r") as f:
            discounts = {
                line.strip().split(",")[0].upper(): line.strip().split(",")[1]
                for line in f if "," in line
            }
    except FileNotFoundError:
        discounts = {}

    try:
        with open("menu.txt", "r") as file:
            lines = file.readlines()

        category_active = False
        for idx, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            elif line.startswith("[") and line.endswith("]"):
                if category_active:
                    print("-" * 89)
                    print()
                print("-" * 89)
                print(f"{line.center(89)}")
                print("-" * 89)
                print("  ID   |             Name               |   Price   |       Status       |    Discount")
                print("-------|--------------------------------|-----------|--------------------|---------------")
                category_active = True
            elif "|" in line:
                parts = [part.strip() for part in line.split("|")]
                if len(parts) >= 3:
                    food_id = parts[0]
                    name = parts[1]
                    try:
                        price = float(parts[2])
                    except ValueError:
                        price = 0.00
                    status = "Out of Stock" if food_id.upper() in unavailable_ids else "Available"
                    discount = discounts.get(name.upper())
                    discount_display = f"{discount}% Discount" if discount else "-"
                    print(f"{food_id:<7}| {name:<31}| RM{price:<8.2f}| {status:<19}| {discount_display}")
                if idx + 1 >= len(lines) or lines[idx + 1].strip().startswith("["):
                    print("-" * 89)
    except FileNotFoundError:
        print("menu.txt not found.")

    print(" " * 89)
    print("=" * 89)


def display_menu():
    render_product_list()


def manage_discount_action(action_type):
    food_names = get_food_names()
    unavailable = get_unavailable_names()
    discounts = get_discounts_dict()

    action_title = {
        "add": "Add Discount",
        "edit": "Edit Discount",
        "delete": "Delete Discount"
    }.get(action_type, "Manage Discount")

    while True:
        render_product_list()
        print(f"\n--- {action_title} ---")
        print("1. Select a Food Name")
        print("0. Back")
        print("-" * 20)
        choice = input("Selecting: ").strip()

        if choice == "1":
            food_name = input("Entering Food Name: ").strip().upper()

            if food_name not in food_names:
                print("Invalid: Food Name does not exist.")
            elif food_name in unavailable:
                print("Invalid: Item is Out of Stock.")
            elif action_type == "add" and food_name in discounts:
                print("Invalid: Discount already exists for this item.")
            elif action_type in ["edit", "delete"] and food_name not in discounts:
                print("Invalid: No existing discount for this item.")
            else:
                if action_type == "add":
                    percent = input("Entering Discount Amount: ").strip()
                    if not percent.isdigit():
                        print("Invalid input. Must be a number.")
                        continue
                    with open("discounts.txt", "a") as f:
                        f.write(f"{food_name},{percent}\n")
                    print(f"Discount of {percent}% applied to {food_name}.")
                elif action_type == "edit":
                    new_percent = input("Enter new discount percentage: ").strip()
                    if not new_percent.isdigit():
                        print("Invalid input. Must be a number.")
                        continue
                    with open("discounts.txt", "w") as f:
                        for name, disc in discounts.items():
                            if name == food_name:
                                f.write(f"{name},{new_percent}\n")
                            else:
                                f.write(f"{name},{disc}\n")
                    print(f"Discount updated for {food_name} to {new_percent}%.")
                elif action_type == "delete":
                    with open("discounts.txt", "w") as f:
                        for name, disc in discounts.items():
                            if name != food_name:
                                f.write(f"{name},{disc}\n")
                    print(f"Discount removed for {food_name}.")
                break

        elif choice == "0":
            break
        else:
            print("Invalid input.")


def manage_discounts():
    while True:
        render_product_list()
        print("\n===== MANAGE DISCOUNTS =====")
        print("1. Add Discount")
        print("2. Edit Discount")
        print("3. Delete Discount")
        print("0. Back to Menu")
        print("=" * 28)
        choice = input("Select an option: ").strip()

        if choice == "1":
            manage_discount_action("add")
        elif choice == "2":
            manage_discount_action("edit")
        elif choice == "3":
            manage_discount_action("delete")
        elif choice == "0":
            break
        else:
            print("Invalid option.")


def generate_receipt_menu():
    while True:
        print("\n========== RECEIPT MENU ==========")
        print("1. Generate Receipt")
        print("2. View Receipt History")
        print("3. Archive Receipted Orders")
        print("0. Back to Cashier Menu")
        print("=" * 34)
        choice = input("Selecting: ")

        if choice == "1":
            generate_receipt()
        elif choice == "2":
            view_receipt_history()
        elif choice == "3":
            archive_receipted_orders()
        elif choice == "0":
            break
        else:
            print("Invalid option.")


def generate_receipt():
    try:
        with open("Customer_Orders.txt", "r") as f:
            orders = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Customer_Orders.txt not found.")
        return

    if not orders:
        print("No orders found.")
        return

    print("\n" + "=" * 66)
    print(" " * 25 + "ORDER STATUS")
    print("=" * 66)
    print(" Customer  |              Item              |    Status")
    print("-" * 66)
    for line in orders:
        parts = [p.strip() for p in line.split(",")]
        if len(parts) == 4:
            name, food, price, status = parts
            item_detail = f"{food} - RM{price}"
        elif len(parts) == 3:
            name, item_detail, status = parts
        else:
            continue  # skip invalid lines
        print(f"{name:<10} | {item_detail:<30} | {status}")
    print("-" * 66)

    customer = input("\nEnter Customer Name to generate receipt: ").strip()
    item_counter = Counter()
    order_lines, updated_lines = [], []
    total = 0.0
    discounts = get_discounts_dict()

    for line in orders:
        parts = line.strip().split(",")
        if len(parts) == 4:
            name, food, price, status = [p.strip() for p in parts]
            item_detail = f"{food},{price}"
        elif len(parts) == 3:
            name, item_detail, status = [p.strip() for p in parts]
        else:
            print(f"Skipping malformed line: {line}")
            continue

        if name.lower() == customer.lower() and status.lower() == "new":
            order_lines.append(item_detail)
            updated_lines.append(f"{name},{item_detail},Receipted\n")
        else:
            updated_lines.append(f"{name},{item_detail},{status}\n")

    if not order_lines:
        print("No new orders found for this customer.")
        return

    receipt_id = f"RCP{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    receipt_content = []
    receipt_content.append("-------------------------- Full Receipt --------------------------")
    receipt_content.append(f"Receipt ID: {receipt_id}")
    receipt_content.append(f"Customer: {customer}")
    receipt_content.append(f"Date/Time: {timestamp}")
    receipt_content.append("-" * 66)
    receipt_content.append("Item                           | Price     | Discount")
    receipt_content.append("-" * 66)

    for item in order_lines:
        name_part, price_part = item.split(",")
        food_name = name_part.strip()
        try:
            price = float(price_part.strip())
        except ValueError:
            continue
        discount = float(discounts.get(food_name.upper(), 0))
        if discount > 0:
            discounted_price = price - (price * discount / 100)
            receipt_content.append(f"{food_name:<30} | RM{price:<7.2f} | ({int(discount)}% Discount)")
            total += discounted_price
        else:
            receipt_content.append(f"{food_name:<30} | RM{price:<7.2f} | -")
            total += price
        item_counter[food_name] += 1

    receipt_content.append("-" * 66)
    receipt_content.append(f"{'Total':<30} | RM{total:.2f}")
    receipt_content.append("=" * 66)

    with open("Customer_Orders.txt", "w") as file:
        file.writelines(updated_lines)

    with open("receipt_history.txt", "a") as history:
        history.write("\n".join(receipt_content) + "\n\n")

    print("Receipt generated and saved in receipt_history.txt")


def view_receipt_history():
    try:
        with open("receipt_history.txt", "r") as file:
            content = file.read()
            if content.strip():
                print(content)
            else:
                print("No receipts have been generated yet.")
    except FileNotFoundError:
        print("receipt_history.txt not found.")


def archive_receipted_orders():
    try:
        with open("Customer_Orders.txt", "r") as file:
            lines = file.readlines()

        remaining_orders = []
        receipted_orders = []

        for line in lines:
            parts = [p.strip() for p in line.strip().split(",")]
            if len(parts) == 4:
                name, item, price, status = parts
                if status.lower() == "receipted":
                    receipted_orders.append(name + "," + item + " - RM" + price + "," + status + "\n")
                else:
                    remaining_orders.append(line)

        with open("Customer_Orders.txt", "w") as file:
            file.writelines(remaining_orders)

        if receipted_orders:
            with open("orderstatus_archive.txt", "a") as archive:
                archive.writelines(receipted_orders)

        print(f"\nArchived {len(receipted_orders)} receipted orders.")
        print(f"Remaining orders in Customer_Orders.txt: {len(remaining_orders)}")

        while True:
            print("\n============ Selection ================")
            print("1. View Archived Orders")
            print("0. Back")
            print("=" * 39)
            sub_choice = input("Selecting: ")

            if sub_choice == "1":
                try:
                    with open("orderstatus_archive.txt", "r") as archive:
                        archived_lines = archive.readlines()
                        if not archived_lines:
                            print("No archived orders found.")
                        else:
                            print("\n===================== ARCHIVED ORDERS ===========================")
                            print(f"{'Customer':<10} | {'Item':<30} | {'Status'}")
                            print("-" * 65)
                            for line in archived_lines:
                                name, item_detail, status = [p.strip() for p in line.strip().split(",")]
                                print(f"{name:<10} | {item_detail:<30} | {status}")
                            print("-" * 65)
                except FileNotFoundError:
                    print("No archive file found.")
            elif sub_choice == "0":
                break
            else:
                print("Invalid option.")

    except FileNotFoundError:
        print("Customer_Orders.txt not found.")


def generate_report():
    try:
        with open("receipt_history.txt", "r") as file:
            lines = [line.strip() for line in file if line.strip()]
        if not lines:
            print("No sales data available.")
            return

        total_receipts = 0
        total_revenue = 0.0
        item_counter = Counter()
        latest_date = ""

        for line in lines:
            if line.startswith("Receipt ID:"):
                total_receipts += 1
            elif line.startswith("Date/Time:"):
                latest_date = line.split(":", 1)[1].strip()
            elif "|" in line and "RM" in line and not line.startswith("-"):
                if line.strip().startswith("Total"):
                    continue
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 2:
                    item_name = parts[0]
                    try:
                        price = float(parts[1].replace("RM", "").strip())
                        total_revenue += price
                        item_counter[item_name] += 1
                    except ValueError:
                        continue

        # === EXPENSES CALCULATION ===
        from collections import defaultdict
        ingredient_cost = {}  # name -> price per unit
        recipes = defaultdict(dict)  # item_name -> {ingredient: amount}

        try:
            with open("chef_data.txt", "r") as f:
                section = None
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        if "inventory" in line.lower():
                            section = "inventory"
                        elif "ingredients_required" in line.lower():
                            section = "recipes"
                        continue

                    if section == "inventory" and ":" in line and "," in line:
                        try:
                            ing_part, values_part = line.split(":")
                            _, price_str = values_part.strip().split(",", 1)
                            ingredient = ing_part.strip().upper()
                            price = float(price_str.strip())
                            ingredient_cost[ingredient] = price
                        except ValueError:
                            continue

                    elif section == "recipes" and "|" in line:
                        try:
                            item_part, ingredients_str = line.split("|", 1)
                            item_name = item_part.strip().upper()
                            ingredient_pairs = ingredients_str.split(",")
                            for pair in ingredient_pairs:
                                if ":" in pair:
                                    ing, amt = pair.strip().split(":")
                                    ing = ing.strip().upper()
                                    amt = float(amt.strip())
                                    recipes[item_name][ing] = amt
                        except ValueError:
                            continue
        except FileNotFoundError:
            print("chef_data.txt not found. Cannot calculate expenses.")
            return

        total_expenses = 0.0
        for item_name, count in item_counter.items():
            item_recipes = recipes.get(item_name.upper(), {})
            for ingredient, amount in item_recipes.items():
                unit_price = ingredient_cost.get(ingredient, 0)
                total_expenses += amount * unit_price * count

        profit = total_revenue - total_expenses
        profitability = (profit / total_revenue * 100) if total_revenue else 0.0
        avg_revenue = total_revenue / total_receipts if total_receipts else 0
        top_items = item_counter.most_common()

        border = "=" * 60
        line = "-" * 60

        print("\n" + border)
        print(f"{'CASHIER SALES REPORT':^60}")
        print(border)
        print(f"{'Total Receipts Issued':<35} : {total_receipts}")
        print(f"{'Total Revenue':<35} : RM{total_revenue:>9.2f}")
        print(f"{'Total Expenses':<35} : RM{total_expenses:>9.2f}")
        print(f"{'Profit':<35} : RM{profit:>9.2f}")
        print(f"{'Profitability':<35} : {profitability:>8.2f}%")
        print(f"{'Average Revenue/Receipt':<35} : RM{avg_revenue:>9.2f}")
        print(f"{'Most Recent Transaction':<35} : {latest_date}")
        print(line)
        print(f"{'Top Selling Products':^60}")
        print(line)
        for i, (item, count) in enumerate(top_items, 1):
            print(f"{i:>2}. {item:<45} x{count}")
        print(border)

        with open("report_history.txt", "a") as log:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            log.write(border + "\n")
            log.write(f"{'CASHIER SALES REPORT':^60}\n")
            log.write(border + "\n")
            log.write(f"[{now}]\n")
            log.write(f"{'Total Receipts Issued':<35} : {total_receipts}\n")
            log.write(f"{'Total Revenue':<35} : RM{total_revenue:>9.2f}\n")
            log.write(f"{'Total Expenses':<35} : RM{total_expenses:>9.2f}\n")
            log.write(f"{'Profit':<35} : RM{profit:>9.2f}\n")
            log.write(f"{'Profitability':<35} : {profitability:>8.2f}%\n")
            log.write(f"{'Average Revenue/Receipt':<35} : RM{avg_revenue:>9.2f}\n")
            log.write(f"{'Most Recent Transaction':<35} : {latest_date}\n")
            log.write(line + "\n")
            log.write(f"{'Top Selling Products':^60}\n")
            log.write(line + "\n")
            for i, (item, count) in enumerate(top_items, 1):
                log.write(f"{i:>2}. {item:<45} x{count}\n")
            log.write(border + "\n\n")

    except FileNotFoundError:
        print("receipt_history.txt not found.")


def view_report_history():
    try:
        with open("report_history.txt", "r") as file:
            content = file.read()
            if content.strip():
                print(content)
            else:
                print("No reports saved yet.")
    except FileNotFoundError:
        print("report_history.txt not found.")


def report_menu():
    while True:
        print("\n==== SALES REPORT MENU ====")
        print("1. Generate Sales Report")
        print("2. View Report History")
        print("0. Back to Cashier Menu")
        print("===========================")
        choice = input("Selecting: ")
        if choice == "1":
            generate_report()
        elif choice == "2":
            view_report_history()
        elif choice == "0":
            break
        else:
            print("Invalid option.")


# === MAIN MENU ===
def cashier_menu():
    while True:
        print("\n========== CASHIER MENU ==========")
        print("1. Restaurant Menu")
        print("2. Manage Discounts")
        print("3. Manage Receipt")
        print("4. Manage Sales Report")
        print("0. Exit")
        print("=" * 34)
        choice = input("Selecting: ")
        if choice == "1":
            render_product_list()
        elif choice == "2":
            manage_discounts()
        elif choice == "3":
            generate_receipt_menu()
        elif choice == "4":
            report_menu()
        elif choice == "0":
            print("Logged out.")
            break
        else:
            print("Invalid input.")


# Run program
if __name__ == "__main__":
    cashier_menu()
