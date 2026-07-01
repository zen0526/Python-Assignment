
def save_unavailable_to_txt(unavailable_items, filename="unavailable_items.txt"):
    with open(filename, "w") as f:
        for item in unavailable_items:
            f.write(f"{item}\n")


def save_menu_pretty_txt(recipes_dic, filename="menu.txt"):
    with open(filename, 'w') as f:
        for category, items in recipes_dic.items():
            f.write(f"[{category}]\n")
            for item_id, item_data in items.items():
                name = item_data['name']
                price = item_data['price']
                f.write(f"{item_id} | {name:<25} | {price:>5.2f}\n")
            f.write("\n")


def save_all_data_txt(recipes_dic, inventory, equipment_reports, ingredients_required, filename="chef_data.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n# ingredients_required\n")
        for recipe, ingredients in ingredients_required.items():
            parts = [f"{ing}:{qty}" for ing, qty in ingredients.items()]
            joined = ", ".join(parts)
            f.write(f"{recipe} | {joined}\n")

        f.write("\n# inventory\n")
        for item, info in inventory.items():
            quantity = info["quantity"]
            price = info["price"]
            f.write(f"{item}: {quantity}, {price}\n")

        f.write("\n# equipment_reports\n")
        for report in equipment_reports:
            f.write(f"{report['equipment']} | {report['issue']}\n")


def load_menu_from_txt(filename):
    menu = {}
    category = None

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            if line.startswith('[') and line.endswith(']'):
                category = line[1:-1]
                menu[category] = {}
            elif '|' in line and category:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) == 3:
                    item_id, item_name, price = parts
                    try:
                        menu[category][item_id] = {
                            'id': item_id,
                            'name': item_name,
                            'price': float(price)
                        }
                    except ValueError:
                        print(f"❌ Invalid price in line: {line}")
    return menu


def load_all_data_txt(filename="chef_data.txt"):
    inventory = {}
    equipment_reports = []
    ingredients_required = {}
    current_section = ""

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                if "inventory" in line:
                    current_section = "inventory"
                elif "equipment_reports" in line:
                    current_section = "equipment"
                elif "ingredients_required" in line:
                    current_section = "ingredients"
            else:
                if current_section == "inventory":
                    item, rest = line.split(":")
                    qty_str, price_str = rest.split(",")
                    inventory[item.strip()] = {
                        "quantity": float(qty_str.strip()),
                        "price": float(price_str.strip())
                    }

                elif current_section == "equipment":
                    equipment, issue = line.split(" | ")
                    equipment_reports.append({
                        "equipment": equipment.strip(),
                        "issue": issue.strip()
                    })

                elif current_section == "ingredients":
                    if " | " not in line:
                        print(f"⚠️ Skipped invalid line in ingredients section: {line}")
                        continue
                    recipe, ing_list = line.split(" | ")
                    ing_parts = ing_list.split(",")
                    ingredients = {}
                    for part in ing_parts:
                        name, qty = part.strip().split(":")
                        ingredients[name.strip()] = float(qty.strip())
                    ingredients_required[recipe.strip()] = ingredients

    return inventory, equipment_reports, ingredients_required


def manage_recipes(recipes_dic, inventory, equipment_reports, ingredients_required, return_to_manager=False):
    while True:
        print("\n📋 Recipes:")
        for category, items in recipes_dic.items():
            print(f"\n[{category}]")
            for item_id, item_data in items.items():
                print(f"  {item_id} | {item_data['name']} | RM{item_data['price']:.2f}")

        choice = input("\nEnter 'add', 'delete', or 'exit': ").strip().lower()

        if choice == 'add':
            category = input("Enter the category: ").strip()
            if category in recipes_dic:
                item_id = input("Enter item ID (e.g., B004): ").strip()
                if item_id in recipes_dic[category]:
                    print(f"❌ ID '{item_id}' already exists in {category}.")
                    continue

                name = input("Enter recipe name: ").strip()
                try:
                    price = float(input("Enter price: ").strip())
                    recipes_dic[category][item_id] = {'name': name, 'price': price}

                    print("Enter ingredients (format: name:quantity,name:quantity separate by commas)")
                    ing_input = input("Ingredients: ").strip()
                    ingredient_dict = {}
                    for pair in ing_input.split(","):
                        try:
                            ing_name, qty = pair.strip().split(":")
                            ing_name = ing_name.strip()
                            qty = float(qty.strip())
                            ingredient_dict[ing_name] = qty

                            if ing_name not in inventory:
                                inventory[ing_name] = {"quantity": 0, "price": 0.0}
                        except ValueError:
                            print(f"❌ Invalid input: '{pair}'. Skipped.")
                        except Exception as e:
                            print(f"❌ Unexpected error with input '{pair}': {e}")

                    ingredients_required[name] = ingredient_dict

                    print(f"✅ Added '{name}' ({item_id}) with price RM{price:.2f} to {category}.")
                    save_menu_pretty_txt(recipes_dic)
                    save_all_data_txt(recipes_dic, inventory, equipment_reports, ingredients_required)

                except ValueError:
                    print("❌ Invalid price. Please enter a number.")
            else:
                print(f"❌ Category '{category}' does not exist.")

        elif choice == 'delete':
            category = input("Enter the category: ").strip()
            if category in recipes_dic:
                item_id = input("Enter item ID to delete: ").strip()
                if item_id in recipes_dic[category]:
                    deleted_name = recipes_dic[category][item_id]['name']
                    del recipes_dic[category][item_id]
                    if deleted_name in ingredients_required:
                        del ingredients_required[deleted_name]
                        print(f"🧹 Also removed ingredients required for '{deleted_name}'.")

                    print(f"🗑️ Deleted '{deleted_name}' ({item_id}) from {category}.")
                    save_menu_pretty_txt(recipes_dic)
                    save_all_data_txt(recipes_dic, inventory, equipment_reports, ingredients_required)
                else:
                    print(f"❌ Item ID '{item_id}' not found in {category}.")
            else:
                print(f"❌ Category '{category}' does not exist.")

        # elif choice == 'show':
        #     print("\n📋 Recipes:")
        #     for category, items in recipes_dic.items():
        #         print(f"\n[{category}]")
        #         for item_id, item_data in items.items():
        #             print(f"  {item_id} | {item_data['name']} | RM{item_data['price']:.2f}")

        elif choice == 'exit':
            print("👋 Goodbye from recipe management!")
            if return_to_manager:
                from Manager import Manager
                Manager()
            return

        else:
            print("❌ Invalid option. Try again.")


def check_inventory_for_recipe(recipes_dic, inventory, equipment_reports, ingredients_required):
    print("\n📋 Available Recipes:")
    for category, items in recipes_dic.items():
        print(f"\n[{category}]")
        for item_id, item_data in items.items():
            print(f"  {item_id} - {item_data['name']}")

    recipe_id = input("\n🔎 Enter recipe ID to check inventory: ").strip().upper()

    recipe_name = None
    for items in recipes_dic.values():
        if recipe_id in items:
            recipe_name = items[recipe_id]["name"]
            break

    if not recipe_name:
        print("❌ Recipe ID not found.")
        return

    required_ingredients = ingredients_required.get(recipe_name, {})
    missing_items = []

    for ingredient, required_qty in required_ingredients.items():
        available = inventory.get(ingredient, 0)
        if isinstance(available, dict):
            available_qty = available.get("quantity", 0)
        else:
            available_qty = available

        if available_qty < required_qty:
            missing_items.append(
                f"{ingredient} (required: {required_qty}, in stock: {available_qty})"
            )

    if missing_items:
        print(f"\n🚫 Missing or insufficient ingredients for '{recipe_name}':")
        for item in missing_items:
            print(f"- {item}")
    else:
        print(f"\n✅ All ingredients are in stock for '{recipe_name}'. You can cook this recipe!")


def main_menu():
    recipes_dic = load_menu_from_txt("menu.txt")
    inventory, equipment_reports, ingredients_required = load_all_data_txt()
    while True:
        print("\n=== Chef Main Management ===")
        print("1. Manage Recipes")
        print("2. Check Inventory")
        print("3. Report equipment issue")
        print("4. View Reported Equipment Issues")
        print("5. Generate Unavailable Dish List")
        print("0. Log Out")
        choice = input("Select an option: ").strip()
        if choice == '1':
            manage_recipes(recipes_dic, inventory, equipment_reports, ingredients_required)
        elif choice == '2':
            check_inventory_for_recipe(recipes_dic, inventory, equipment_reports, ingredients_required)
        elif choice == '3':
            report_equipment_issue(equipment_reports, recipes_dic, inventory, ingredients_required)
        elif choice == '4':
            show_equipment_issues(recipes_dic, inventory, equipment_reports, ingredients_required)
        elif choice == '5':
            unavailable = get_unavailable_items(ingredients_required, inventory, recipes_dic)
            save_unavailable_to_txt(unavailable)
            print("✅ Updated unavailable_items.txt for cashier.")
        elif choice == '0':
            print("Logged out.")
            break

        else:
            print("Invalid option. Try again.")


def get_unavailable_items(ingredients_required, inventory, recipes_dic):
    unavailable_ids = []

    for category in recipes_dic.values():
        for item_id, item in category.items():
            recipe_name = item["name"]
            required_ingredients = ingredients_required.get(recipe_name, {})
            for ingredient, required_qty in required_ingredients.items():
                available_qty = inventory.get(ingredient, {}).get("quantity", 0)
                if available_qty < required_qty:
                    unavailable_ids.append(item_id)
                    break

    return unavailable_ids


def report_equipment_issue(equipment_reports, recipes_dic, inventory, ingredients_required):
    equipment_name = input("Enter the equipment name: ")
    issue = input("Enter malfunctions or maintenance needs: ").strip()

    equipment_reports.append({
        "equipment": equipment_name,
        "issue": issue
    })

    save_all_data_txt(
        recipes_dic,
        inventory,
        equipment_reports,
        ingredients_required
    )

    print(f"✅ Issue reported for '{equipment_name}': {issue}")

    return equipment_reports


def show_equipment_issues(recipes_dic, inventory, equipment_reports, ingredients_required):
    print("\n=== Reported Equipment Issues ===")
    if not equipment_reports:
        print("No equipment issues reported.")
    else:
        for idx, report in enumerate(equipment_reports, 1):
            print(f"{idx}. Equipment: {report['equipment']}, Issue: {report['issue']}")


if __name__ == "__main__":
    main_menu()

