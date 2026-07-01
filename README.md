# Restaurant Ordering and Management System 🍔

A modular, menu-driven CLI application developed in Python for efficient restaurant operations management. The system implements a secure, role-based architecture operating entirely without global variables, utilizing advanced Python collections and structured flat text files for persistent data storage.

---

## 🛠️ System Architecture & File Structure

The project repository is broken down into modular functional engines and text-file storage layers:

### 🎮 Core Logic & Role Engines
* `main.py` - The application entry point managing execution loops and the master role-selection gateway.
* `Manager.py` - System administration, account controls, financial metrics tracking, and product/ingredient master inventory tracking.
* `Customer.py` - Core user interface for profile updates, digital menu parsing, shopping cart staging, live order placement, and feedback capturing.
* `Cashier.py` - Point-of-Sale (POS) controls managing discount overrides, transactional billing engines, and sales analytics tracking.
* `Chef.py` - Operational panel monitoring active kitchen statuses, checking ingredient logic matrices, and managing recipe updates.

### 📂 Flat-File Data Persistence Layer
* `Account_Storage.txt` - Encapsulates credentials verification strings mapped dynamically across active sessions.
* `menu.txt` / `chef_data.txt` - Serves as the central product and digital recipe catalog.
* `Customer_Orders.txt` / `orderstatus_archive.txt` - Tracks live orders, historical archives, and status modifications.
* `receipt_history.txt` / `report_history.txt` - Logs generated financial receipts and localized sales popularity analytical reports.
* `discounts.txt` / `Customer_Reviews.txt` - Manages promotion keys and store rating inputs.
* `unavailable_items.txt` - Monitors low inventory levels and item shortages.

---

## 🚀 Key Functional Features

* **Multi-Tenant Permissions Matrix:** Implements strict authorization boundaries for four explicit roles (Manager, Customer, Cashier, Chef) via structured menu interfaces.
* **Advanced Data Mapping:** Processes memory and queries using native Python collection structures (nested dictionaries, lists, and tuples) to handle state changes.
* **Defensive Input Validation:** Enforces data cleaning checkpoints across user entry gateways, eliminating type errors and illegal state arguments without runtime performance degradation.
* **Isolated State Modularity:** Adheres strictly to functional programming parameters with zero global variables, handling variables via local scopes and direct parameters.

---

## 💻 How to Run the Application

1. Ensure Python 3.x is installed on your local environment.
2. Clone or extract this project folder.
3. Execute the entry script from your terminal console:
   ```bash
   python main.py
