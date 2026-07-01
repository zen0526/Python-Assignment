from Chef import manage_recipes, load_menu_from_txt, load_all_data_txt
from Cashier import view_report_history


# Function used by manager after choosing to add user accounts
def Add_Account():
    while True:
        option = input("""\n===== Please select an option =====
    1. Enter Username
    0. Go back
===================================
select an option:""")
        if option == '1':
            # create a list to store all the names retrieved from the text file
            Exist_Names = []
            Valid_Roles = ['Customer', 'Chef', 'Manager', 'Cashier']
            try:
                with open("Account_Storage.txt", "r") as Accounts:
                    for Account in Accounts:
                        Exist_Names.append(Account.strip().split(",")[0])
            except FileNotFoundError:
                print("Account_Storage.txt not found.")

            # Get and validate username
            while True:
                Username = input("Please enter a username for the account (Enter '0' to go back): ")
                # Check if username exists
                if Username in Exist_Names:
                    print("Username exists, please choose another one.")
                # Check if username is all alphabets
                elif not Username.isalpha() and Username != '0':
                    print("Username should only contain alphabets.")
                # Check if Username entered is empty
                elif not Username:
                    print("Username cannot be empty.")
                # If everything above was not encountered, username is valid
                elif Username.strip().lower() == '0':
                    return
                else:
                    break

            # Get and validate password
            while True:
                # Repeatedly ask for password if password is empty or less than 8 characters
                Password = input("Please enter a password for the account: ")
                if not Password:
                    print("Password cannot be empty.")
                elif len(Password) < 6:
                    print("Password cannot be less than 6 characters")
                else:
                    break

            # Get and a validate role
            while True:
                # Repeatedly ask for role if the input is not in the valid roles given earlier
                role = input("Please give the account a role: ").strip().lower().capitalize()
                if role not in Valid_Roles:
                    print("Role invalid.")
                else:
                    break

            Data = Username + ',' + Password + ',' + role + '\n'
            # Store the Account to be added into the text file
            with open("Account_Storage.txt", "a") as Storage:
                Storage.write(Data)
                print("Account successfully added.")
                return

        elif option == '0':
            return
        else:
            print("Invalid option.")


def Delete_Account():
    while True:
        option = input("""\n===== Please select an option =====
    1. Enter Username
    0. Go back
===================================
select an option:""")
        if option == '1':
            Username = input("Please enter the username of the account you want to delete: ")

            # Add validation to validate username exists before proceeding
            try:
                with open("Account_Storage.txt", "r") as Storage:
                    Accounts = Storage.readlines()
            except FileNotFoundError:
                print("Account_Storage.txt not found.")

            Target_Line = None
            for Account in Accounts:
                if Username == Account.split(",")[0]:
                    Target_Line = Account
                    break

            if Target_Line:
                with open("Account_Storage.txt", "w") as Storage:
                    for Account in Accounts:
                        if Account != Target_Line:
                            # Rewrite everything except the Line to delete
                            Storage.write(Account)
                    print("Account successfully deleted.")
                    return
            else:
                print("Account not found.")
                return
        elif option == '0':
            return
        else:
            print("Invalid option.")


def Modify_Account_Details():
    while True:
        option = input("""\n===== Please select an option =====
    1. Enter Username
    0. Exit
==================================
select an option:""")
        if option == '1':
            Name = None
            Password = None
            Role = None
            valid_roles = ['Customer', 'Chef', 'Cashier', 'Manager']
            Exist_Names = []

            try:
                with open("Account_Storage.txt", "r") as Accounts:
                    for Account in Accounts:
                        Exist_Names.append(Account.strip().split(",")[0])
            except FileNotFoundError:
                print("Account_Storage.txt not found.")
                return

            while True:
                Username = input("Please enter the username of the account you want to modify: ")
                if Username not in Exist_Names:
                    print("Username not found.")
                else:
                    break

            Modification = input("""Please choose what you want to modify
    1. Name
    2. Password
    3. Role
    4. Go back
select an option:""")

            if Modification == "1":
                Name = input("Please enter a new name: ")
            elif Modification == "2":
                while True:
                    Password = input("Please enter a new password: ")
                    if len(Password) < 6:
                        print("Password should not be less than 6 characters.")
                    else:
                        break
            elif Modification == "3":
                # Validate new role input
                while True:
                    Role = input("Please enter a new role: ").lower().capitalize()
                    if Role not in valid_roles:
                        print("Please enter a valid role (Customer/Chef/Cashier/Manager).")
                    else:
                        break
            else:
                print("Please enter a valid option")
                return

            # Get every account details from the account storage file
            try:
                with open("Account_Storage.txt", "r") as Storage:
                    Accounts = Storage.readlines()
            except FileNotFoundError:
                print("Account_Storage.txt not found.")
                return

            # Looping over every accounts in 'Accounts', through the number of accounts in it
            for Account_Number in range(len(Accounts)):
                # Splitting accounts into three parts for easier modifying
                Account_Parts = Accounts[Account_Number].strip("\n").split(",")

                # Assign the username of the current account being looped to the variable 'Current_Username'
                Current_username = Account_Parts[0]

                # When the assigned username matches the name given by the manager, it means that the username is found
                # Hence, 'found' turns into True
                if Username == Current_username:
                    # Every if loop below checks whether name, password or role is not empty first.
                    # When the one that is not empty is found, assign it to respective part.
                    if Name:
                        Account_Parts[0] = Name
                    elif Password:
                        Account_Parts[1] = Password
                    elif Role:
                        Account_Parts[2] = Role

                    # join back all parts after modifying, otherwise only the data in 'Account_Parts' was changed
                    Accounts[Account_Number] = ','.join(Account_Parts) + "\n"
                    break

            # Overwrite everything in the file with what is in 'Accounts'
            with open("Account_Storage.txt", "w") as Storage:
                Storage.writelines(Accounts)
                print("Account details modified successfully.")
                return

        elif option == '0':
            return
        else:
            print("Invalid option.")


def Manager():
    while True:
        option = input("""\n========== Manager Menu ==========
    1. Manage user accounts
    2. Manage customer orders
    3. Manage financial 
    4. Manage inventory
    5. Manage Products
    6. Check customer feedback
    0. Log Out
==================================
Select an option: """)

        if option == '1':
            ManageUserAccounts()
        elif option == '2':
            ManageCustomerOrders()
        elif option == '3':
            ManageFinancial()
        elif option == '4':
            ManageInventory()
        elif option == '5':
            ManageProducts()
        elif option == '6':
            CheckCustomerFeedback()
        elif option == '0':
            print("Logged out.")
            break
        else:
            print("Please enter a valid option.")


def Exit():
    print("Goodbye!")
    exit()


def ManageUserAccounts():
    # validation (Maybe display user accounts before asking for options)
    # Provide several options that they can do when choosing to manage accounts
    while True:
        try:
            with open("Account_Storage.txt", "r") as Accounts:
                print(f"\n=============== Existing accounts ================")
                print("+--------------------+----------------+----------+")
                print("| Username           | Password       | Role     |")
                print("+--------------------+----------------+----------+")

                for Account in Accounts:
                    Account_Parts = Account.strip().split(",")
                    Username, Password, Role = Account_Parts
                    print(f"| {Username:<18} | {Password:<14} | {Role:<8} |")
                print("+--------------------+----------------+----------+")
        except FileNotFoundError:
            print("Account_Storage.txt not found.")
            return

        Option = input("""\n===== Please select an option =====
    1. Add Account
    2. Delete Account
    3. Modify Account Details
    0. Go Back
===================================
select an option:""")

        if Option == '0':
            return
        if Option == '1':
            Add_Account()
        elif Option == '2':
            Delete_Account()
        elif Option == '3':
            Modify_Account_Details()
        else:
            print("Please enter a valid option")


def ManageCustomerOrders():
    # Display all customer orders  and allow updating of order status
    while True:
        try:
            with open("Customer_Orders.txt", "r") as Customer_Orders:
                Orders = Customer_Orders.readlines()
                print("+----------+--------------------+----------------------+-----------+--------------+")
                print("| Order ID | Customer Name      | Dish Name            | Price     | Order Status |")
                print("+----------+--------------------+----------------------+-----------+--------------+")
                for Order_Number, Order in enumerate(Orders):
                    Order_parts = Order.strip().split(",")
                    Customer, Dish, Price, Status = Order_parts
                    OrderID = f"OD{Order_Number}"
                    print(f"| {OrderID:<8} | {Customer:<18} | {Dish:<20} | RM {Price:<6} | {Status:<12} |")
                print("+----------+--------------------+----------------------+-----------+--------------+")
        except FileNotFoundError:
            print("Customer_Orders.txt not found.")
            return

        option = input("""\n========= Please select an option ==========
    1. Enter Order ID to modify order status
    0. Exit
============================================
select an option:""")
        if option == '1':
            # Ask for the order ID to update and the new order status
            Order_ID = input("Please enter the order ID of the order you want to modify: ").strip()
            if not Order_ID.startswith("OD") and not Order_ID[2:].isdigit():
                print("Invalid Order ID format, please use format like OD1, OD2....")
                continue

            order_index = int(Order_ID[2:])

            if order_index < 0 or order_index > len(Orders)-1:
                print("Order ID does not exist.")
                continue

            Order_Status = input("Please enter the new status (New/Receipted/Cancelled): ").lower().capitalize()
            if Order_Status not in ("New", "Receipted", "Cancelled"):
                print("Invalid order status (New/Receipted/Cancelled).")
                continue

            updated_orders = []
            for Order_Number, Order in enumerate(Orders):
                if Order_Number == order_index:
                    Order_parts = Order.strip().split(",")
                    # Update status
                    Order_parts[-1] = Order_Status
                    updated_orders.append(','.join(Order_parts) + "\n")
                else:
                    updated_orders.append(Order)

            with open("Customer_Orders.txt", "w") as Update:
                Update.writelines(updated_orders)
                print("Order status updated!")

        elif option == '0':
            return
        else:
            print("Invalid option.")


def ManageFinancial():
    view_report_history()


# For manager to add, remove and update ingredients
def AddIngredients():
    # Ask for ingredient name and amount
    Ingredient_Name = input("Please enter new ingredient name: ")
    while True:
        try:
            Amount = float(input("Please enter amount for the new ingredient: "))
            Price = float(input("Please enter the price per unit of the ingredient"))
            break
        except ValueError:
            print("Amount and Price should only contain numbers.")

    # Get everything form the text file
    try:
        with open("chef_data.txt", "r") as Ingredients:
            Data = Ingredients.readlines()
    except FileNotFoundError:
        print("chef_data.txt not found.")
        return

    # The variable is to indicate whether the current section is inventory
    in_inventory_section = False
    # Create a list to store updated data with new ingredient added
    Updated_Data = []

    for ingredients in Data:
        # Check if inventory section is reached, if so, make the variable 'True'
        if ingredients.strip() == '# inventory':
            in_inventory_section = True

        if in_inventory_section:
            # If currently in inventory section, look for empty line at the end
            if ingredients.strip() == '':
                # If found, add the new ingredient
                Updated_Data.append(f"{Ingredient_Name}: {Amount}, {Price}\n")
                # The variable is set to False after this to indicate inventory section ended
                in_inventory_section = False
            else:
                Updated_Data.append(ingredients)
                continue

        # Add back every line to the new list
        Updated_Data.append(ingredients)

    # Write the new list back to the text file
    with open("chef_data.txt", "w") as Ingredients:
        Ingredients.writelines(Updated_Data)
        print("New ingredient successfully added.")

    return


def RemoveIngredients():
    Ingredient_Name = input("Please enter the ingredient you want to remove: ")

    # Get all data from the text file
    try:
        with open("chef_data.txt", "r") as Ingredients:
            Data = Ingredients.readlines()
    # Handle file not found error
    except FileNotFoundError:
        print("chef_data.txt not found.")
        return

    in_inventory_section = False
    Updated_Data = []
    found = False

    for ingredient in Data:
        if ingredient.strip() == '# inventory':
            # when this line is detected, set the variable to true to indicate current section in inventory
            in_inventory_section = True

        if in_inventory_section:
            # If in inventory section, look for the name that matches the input
            if ingredient.split(":")[0].lower() == Ingredient_Name.lower():
                # If found, skip the iteration to not add it back to the updated list
                found = True
                continue

        # Add everything back to the list, except for the one that wants to be deleted
        Updated_Data.append(ingredient)

    if not found:
        print("Ingredient not found")
        return
    else:
        with open("chef_data.txt", "w") as Ingredients:
            # Overwrite all data and write back everything without the removed ingredient to the file
            Ingredients.writelines(Updated_Data)
            print("Ingredient successfully deleted")

    return


def UpdateIngredients():
    Ingredient_Name = input("Please enter the name of the ingredient you want to update: ").strip().lower()
    while True:
        Update_Option = input("Please enter what you want to update (name/amount/price): ").strip().lower()
        if Update_Option in ("name", "amount", "price"):
            break
        else:
            print("Please enter a valid option (name/amount/price).")

    New_Name = None
    New_Amount = None
    New_Price = None

    if Update_Option == 'name':
        New_Name = input("Please enter new name for the ingredient: ")
    elif Update_Option == 'amount':
        while True:
            try:
                New_Amount = float(input("Please enter new amount for the ingredient: "))
                break
            except ValueError:
                print("Amount should only contain numbers.")
    elif Update_Option == 'price':
        while True:
            try:
                New_Price = float(input("Please enter new price for the ingredient: "))
                break
            except ValueError:
                print("Price should only contain numbers.")

    try:
        with open("chef_data.txt", "r") as Ingredients:
            Data = Ingredients.readlines()
    except FileNotFoundError:
        print("chef_data.txt not found.")
        return

    in_inventory_section = False
    Updated_Data = []
    found = False

    for ingredient in Data:
        if ingredient.strip() == '# inventory':
            in_inventory_section = True

        if in_inventory_section:
            if ingredient.split(":")[0].lower().strip() == Ingredient_Name:
                found = True
                if New_Name:
                    Updated_Data.append(New_Name + ":" + ingredient.split(":")[1] + "\n")
                    # Set to false after the target ingredient is updated and remaining lines are just appended
                    in_inventory_section = False
                    continue
                elif New_Amount:
                    Updated_Data.append(ingredient.split(":")[0] + ": " + str(New_Amount) + "," + ingredient.split(":")[1].split(",")[1] + "\n")
                    in_inventory_section = False
                    continue
                elif New_Price:
                    Updated_Data.append(ingredient.split(",")[0] + ", " + str(New_Price) + "\n")
                    in_inventory_section = False
                    continue

        Updated_Data.append(ingredient)

    if found:
        with open("chef_data.txt", "w") as Ingredients:
            Ingredients.writelines(Updated_Data)
            print("Ingredient details updated")
    else:
        print("Ingredient not found.")
        return

    return


def ManageInventory():
    # Display all ingredients and allow manager to add, remove or update them
    try:
        with open("chef_data.txt", "r") as Display_ingredients:
            in_inventory_section = False
            for ingredient in Display_ingredients:
                # When inventory section is reached, these titles to make them into a readable format
                if ingredient.strip() == "# inventory":
                    in_inventory_section = True
                    print("\n+----------------------------+-----------+--------+")
                    print("| Ingredient Name            | Amount    | Price  |")
                    print("+----------------------------+-----------+--------+")
                    continue

                if in_inventory_section:
                    # If currently in inventory section and the current line is not empty
                    if ingredient.strip() != "":
                        # Split the data into several parts and assign them to a variable with meaningful name
                        IngredientName = ingredient.split(":")[0]
                        IngredientAmount = ingredient.split(":")[1].split(",")[0]
                        PricePerUnit = ingredient.split(":")[1].split(",")[1]
                        # Print them in a readable format
                        print(f"| {IngredientName:<26} | {IngredientAmount.strip():<9} | {PricePerUnit.strip():<6} |")
                    else:
                        # If in inventory section but the current line is empty, it indicates that the section ended
                        in_inventory_section = False
            print("+----------------------------+-----------+--------+")
    # Handle file not found errors
    except FileNotFoundError:
        print("chef_data.txt not found.")
        # Return back to Manager menu
        return

    # ask for input repeatedly
    while True:
        option = input(f"""\n===== Please select an option =====
    1. Add new ingredient
    2. Remove an ingredient
    3. Update an ingredient
    0. Go Back
===================================
select an option:""")

        if option == '1':
            AddIngredients()
        elif option == '2':
            RemoveIngredients()
        elif option == '3':
            UpdateIngredients()
        elif option == '0':
            # Return back to manager menu
            return
        else:
            print("Please enter a valid option")


def ManageProducts():
    recipes_dic = load_menu_from_txt("menu.txt")
    inventory, equipment_reports, ingredients_required = load_all_data_txt()
    manage_recipes(recipes_dic, inventory, equipment_reports, ingredients_required, return_to_manager=True)


# Monitor and review customer feedback
def CheckCustomerFeedback():
    # Display customer feedback
    try:
        with open("Customer_Reviews.txt", "r") as Feedback:
            Customer_Feedback = Feedback.readlines()
            if Customer_Feedback:
                print("------- Customer Feedback -------")
                for feedback in Customer_Feedback:
                    print(feedback.split(",")[0] + ": " + feedback.split(",")[1].strip())

                print("---------------------------------")
                print("All customer feedbacks displayed.")
                print("---------------------------------")
                while True:
                    Back = input("Enter 'back' to exit?: ")
                    if Back.lower().strip() == 'back':
                        return
            else:
                print("No feedback yet.")
                return
    except FileNotFoundError:
        print("Customer_Reviews.txt not found.")
        return


if __name__ == "__main__":
    Manager()
