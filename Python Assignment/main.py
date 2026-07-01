from customer import customer_logged_in_menu
from Manager import Manager
from Chef import main_menu as chef_menu
from Cashier import cashier_menu


def main_menu():
    while True:
        print("\n=== Welcome to APU Hamburger Restaurant ===")
        print("1. Login")
        print("2. Register as Customer")
        print("0. Exit")
        choice = input("Please enter your selection: ")

        if choice == "1":
            login_menu()
        elif choice == "2":
            register_customer()
        elif choice == "0":
            print("Thank you! See you next time.")
            break
        else:
            print("Invalid input. Please try again.")


def login_menu():
    print("\n--- Login ---")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    role = validate_login_and_get_role("Account_Storage.txt", username, password)
    if role:
        print(f"\nWelcome, {username} ({role})!")
        if role == "Customer":
            customer_logged_in_menu(username)
        elif role == "Manager":
            Manager()
        elif role == "Cashier":
            cashier_menu()
        elif role == "Chef":
            chef_menu()
        else:
            print("Unknown role. Please contact admin.")
    else:
        print("Invalid username or password.")


def validate_login_and_get_role(filename, username, password):
    try:
        with open(filename, "r") as file:
            for line in file:
                saved_username, saved_password, role = line.strip().split(",")
                if username == saved_username and password == saved_password:
                    return role
    except FileNotFoundError:
        print(f"{filename} not found.")
    return None


def register_customer():
    print("\n--- Customer Registration ---")
    username = input("Enter a username: ")

    try:
        with open("Account_Storage.txt", "r") as file:
            for line in file:
                saved_username = line.strip().split(",")[0]
                if username == saved_username:
                    print("Username already exists. Please rewrite again.")
                    return
    except FileNotFoundError:
        print("Account_Storage.txt not found.")

    while True:
        password = input("Enter a password (min 6 words): ")
        if len(password) >= 6:
            break
        else:
            print("Password must be at least 6 words. Please try again.")

    with open("Account_Storage.txt", "a") as file:
        file.write(f"{username},{password},Customer\n")
    print("Registration successful! You can now login.")


main_menu()
