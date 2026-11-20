# JAIN (Deemed-to-be University)
## School of Computer Science and IT
### MCA Programme | 25MCAG301 - NoSQL Databases
### Activity-2: Mini Project Report

---

# RESTAURANT FOOD ORDERING SYSTEM (FOODIESPOT) USING MONGODB

**Prepared and Submitted by:**

| USN | NAME |
| :--- | :--- |
| 25MCAR0225 | HARSHIL SHETH |


---

## TABLE OF CONTENTS

| Sl. No. | Content |
| :--- | :--- |
| **1** | **Introduction** |
| | 1.1 Purpose of the Project |
| | 1.2 Target Audience |
| **2** | **Concept and Objectives** |
| | 2.1 Problem Statement |
| | 2.2 Objectives |
| **3** | **System Requirements** |
| | 3.1 Software Requirements |
| | 3.2 Hardware Requirements |
| | 3.3 Dependencies and Tools |
| **4** | **Implementation Details** |
| | 4.1 Schema |
| | 4.2 MongoDB Queries |
| | 4.3 Screenshots | |
| **5** | **Challenges and Solutions** |
| | 5.1 Technical Challenges |
| | 5.2 Design Challenges |
| | 5.3 How Issues Were Resolved |
| **6** | **Conclusion** |
| **7** | **References** |
| | 7.1 Book References |
| | 7.2 Web References |

---

# 1.0 Introduction

### 1.1 Purpose of the Project
The rapid digitization of the culinary and hospitality industry requires high-throughput, agile, and resilient database architectures to handle dynamic menu configurations and real-time order processing. Traditional Relational Database Management Systems (RDBMS) enforce rigid tabular schemas, necessitating expensive join operations and schema migration penalties whenever complex, nested order data or seasonal menu variations are introduced.

The primary purpose of the Restaurant Food Ordering System (*FoodieSpot*) is to build a robust, document-oriented NoSQL solution using MongoDB and Python (Flask). By leveraging document modeling, multi-item customer orders containing diverse nested arrays can be stored atomically within a single document. The application demonstrates real-world enterprise NoSQL principles: flexible schema management, dynamic indexing, subdocument embedding, high-performance CRUD operations, and multi-stage analytical aggregation pipelines.

### 1.2 Target Audience
The system serves distinct primary stakeholders across restaurant business operations:
*(a) Restaurant Customers:* End-users browsing dynamic categorized digital menus, searching dishes in real time, configuring cart quantities, and tracking instantaneous order status updates.  
*(b) Restaurant Administrators & Kitchen Staff:* Operational personnel managing real-time inventory availability, adding seasonal menu items, updating pricing, and orchestrating order life-cycle transitions (Pending, Preparing, Ready, Delivered, Cancelled).  
*(c) Business Analysts & Store Managers:* Stakeholders relying on aggregate metrics to uncover top-selling food items, demand trends, and operational revenue performance without incurring costly analytical workload penalties.

---

# 2.0 Concept and Objectives

### 2.1 Problem Statement
Conventional food ordering platforms developed on relational backends face significant operational bottlenecks when handling variable menu structures and nested order lines:
1. *Impedance Mismatch and Joins:* Storing an order with multiple items requires partitioning across separate normalized tables (`orders`, `order_items`, `menu_items`, `customers`), requiring multiple foreign key constraints and multi-table SQL joins that degrade database throughput under peak ordering traffic.
2. *Rigid Schemas:* Modifying menu properties (such as nutritional values, spice levels, allergen tags, or combo offerings) necessitates ALTER TABLE migrations, incurring downtime risk.
3. *Real-Time Operational Analytics:* Calculating real-time sales revenue and volume statistics across normalized tables introduces high computational overhead.

Hence, there is a distinct requirement for a modern, document-oriented NoSQL database that can store composite order hierarchies naturally in JSON/BSON format while maintaining rapid read and write capability.

### 2.2 Objectives
The key technical and academic objectives of this mini project are:
*(a) Schema Design & Data Modeling:* To design denormalized and referenced MongoDB data collections (`menu_items`, `orders`, `customers`) that capitalize on BSON flexibility.  
*(b) End-to-End CRUD Implementation:* To implement complete document operations: Insertion (`insert_one`, `insert_many`), Retrieval (`find`, `find_one`, projections), Updating (`update_one` with `$set` and `upsert=True`), and Deletion (`delete_one`).  
*(c) Text-Like Search Pattern:* To implement sub-string pattern matching and case-insensitive menu filtering using MongoDB `$regex` and `$or` query operators.  
*(d) Multi-Stage Aggregation Pipeline:* To design analytical queries using `$unwind`, `$group`, `$sort`, and `$limit` to compute top-selling items, volume distribution, and revenue breakdown.  
*(e) Modular Web Application:* To build an intuitive, responsive user interface utilizing Python Flask and Bootstrap 5 connected seamlessly via PyMongo.

---

# 3.0 System Requirements

### 3.1 Software Requirements
- **Operating System:** Microsoft Windows 10/11, Ubuntu Linux 20.04+, or macOS Sonoma
- **Database Engine:** MongoDB Community Server (v6.0 or higher) / MongoDB Atlas
- **Database Connection URI:** `mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.12.0`
- **Database GUI Client:** MongoDB Compass (v1.40 or higher) / MongoDB Shell (`mongosh` v2.12+)
- **Backend Framework:** Python 3.10+ / Flask 3.0+
- **Driver / ODM:** PyMongo 4.6+
- **Frontend Technologies:** HTML5, CSS3, JavaScript (ES6), Bootstrap 5.3, Bootstrap Icons
- **Development Environment:** Visual Studio Code / PyCharm / Antigravity

### 3.2 Hardware Requirements
- **Processor:** Intel Core i3 / AMD Ryzen 3 (or higher) Dual-Core / Quad-Core CPU
- **RAM:** Minimum 4 GB RAM (8 GB recommended for concurrent MongoDB daemon and web server)
- **Disk Storage:** Minimum 1 GB available storage space for MongoDB binaries and application data
- **Display Resolution:** 1280 x 720 minimum (1920 x 1080 recommended)

### 3.3 Dependencies and Tools
- **Flask:** Lightweight WSGI web application framework in Python for routing and templating.
- **PyMongo:** The official MongoDB client library for Python handling connection pooling and BSON serialization.
- **BSON ObjectId:** Built-in module to manage unique 12-byte hexadecimal identifiers across documents.
- **Bootstrap 5:** Mobile-first CSS framework providing responsive layouts and UI components.

---

# 4.0 Implementation Details

### 4.1 Schema
MongoDB stores unstructured or semi-structured data as flexible BSON documents. The application maintains three primary collections in the `restaurant_db` database:

#### *(a) Collection: `menu_items`*
Stores food items, categories, pricing, and availability flags.

```json
{
  "_id": ObjectId("67389a0bc45ef2018a101aa1"),
  "name": "Chicken Biryani",
  "category": "Main Course",
  "price": 349.0,
  "description": "Fragrant basmati rice layered with spiced chicken and aromatic herbs",
  "is_available": true,
  "image_url": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=600",
  "created_at": ISODate("2026-11-20T18:00:00.000Z")
}
```

#### *(b) Collection: `customers`*
Maintains customer profile records updated dynamically during checkout using upsert semantics.

```json
{
  "_id": ObjectId("67389b14c45ef2018a101aa2"),
  "phone": "9876543210",
  "name": "Rahul Verma",
  "address": "Flat 304, Green Heights, Bengaluru",
  "last_order_at": ISODate("2026-11-20T18:05:00.000Z")
}
```

#### *(c) Collection: `orders`*
Demonstrates document embedding. Each order contains an embedded array of subdocuments representing individual line items.

```json
{
  "_id": ObjectId("67389c22c45ef2018a101aa3"),
  "customer_name": "Rahul Verma",
  "customer_phone": "9876543210",
  "customer_address": "Flat 304, Green Heights, Bengaluru",
  "items": [
    {
      "item_id": ObjectId("67389a0bc45ef2018a101aa1"),
      "name": "Chicken Biryani",
      "price": 349.0,
      "quantity": 2,
      "subtotal": 698.0
    },
    {
      "item_id": ObjectId("67389a0bc45ef2018a101aa4"),
      "name": "Mango Lassi",
      "price": 99.0,
      "quantity": 1,
      "subtotal": 99.0
    }
  ],
  "total_amount": 797.0,
  "status": "Pending",
  "ordered_at": ISODate("2026-11-20T18:05:00.000Z")
}
```

---

### 4.2 MongoDB Queries

*Figure 1. Code Snippet for Menu Item Creation (Insert Operation)*
```python
# Code 1: Insert new menu item into MongoDB
new_item = {
    "name": request.form["name"],
    "category": request.form["category"],
    "price": float(request.form["price"]),
    "description": request.form["description"],
    "is_available": "is_available" in request.form,
    "image_url": request.form.get("image_url", ""),
    "created_at": datetime.now()
}
result = db.menu_items.insert_one(new_item)
```

*Figure 2. Code Snippet for Menu Retrieval and Category Grouping (Read Operation)*
```python
# Code 2: Query all menu items sorted by category
menu_items = list(db.menu_items.find().sort("category", 1))
categories = {}
for item in menu_items:
    cat = item.get("category", "Other")
    categories.setdefault(cat, []).append(item)
```

*Figure 3. Code Snippet for Case-Insensitive Pattern Search (Search Operation)*
```python
# Code 3: Multi-field search using $regex and $or
query = request.args.get("q", "")
results = list(db.menu_items.find({
    "$or": [
        {"name": {"$regex": query, "$options": "i"}},
        {"category": {"$regex": query, "$options": "i"}},
        {"description": {"$regex": query, "$options": "i"}}
    ]
}))
```

*Figure 4. Code Snippet for Atomic Order Insertion with Embedded Documents*
```python
# Code 4: Atomic insertion of customer order with nested item documents
order_document = {
    "customer_name": customer_name,
    "customer_phone": customer_phone,
    "customer_address": customer_address,
    "items": order_items, # Embedded array of subdocuments
    "total_amount": total_amount,
    "status": "Pending",
    "ordered_at": datetime.now()
}
order_result = db.orders.insert_one(order_document)
```

*Figure 5. Code Snippet for Customer Profile Upsert (Update with Upsert)*
```python
# Code 5: Upsert customer profile based on unique phone number
db.customers.update_one(
    {"phone": customer_phone},
    {"$set": {
        "name": customer_name,
        "phone": customer_phone,
        "address": customer_address,
        "last_order_at": datetime.now()
    }},
    upsert=True
)
```

*Figure 6. Code Snippet for Order Status Update and Item Deletion (Update & Delete)*
```python
# Code 6a: Update order status
db.orders.update_one(
    {"_id": ObjectId(order_id)},
    {"$set": {"status": new_status, "updated_at": datetime.now()}}
)

# Code 6b: Delete menu item
db.menu_items.delete_one({"_id": ObjectId(item_id)})
```

*Figure 7. Code Snippet for Analytics Aggregation Pipeline (Analytical Query)*
```python
# Code 7: Multi-stage aggregation pipeline calculating top selling items
pipeline = [
    {"$unwind": "$items"},
    {"$group": {
        "_id": "$items.name",
        "times_ordered": {"$sum": "$items.quantity"},
        "total_revenue": {"$sum": "$items.subtotal"}
    }},
    {"$sort": {"times_ordered": -1}},
    {"$limit": 10}
]
popular_items = list(db.orders.aggregate(pipeline))
```

*Figure 8. Code Snippet for Backend Order List Sanitization*
```python
# Code 8: Guard against missing or malformed items attributes
raw_orders = list(db.orders.find().sort("ordered_at", -1).limit(20))
orders = []
for ord_doc in raw_orders:
    if "items" not in ord_doc or not isinstance(ord_doc["items"], list):
        ord_doc["items"] = []
    orders.append(ord_doc)
```

---

### 4.3 Screenshots
Below are descriptions and layout placements for the system interface and verification screenshots:

*Fig 1. Customer Menu Interface Layout (Code 2)*  
Displays the categorized food catalog, dynamic badges, item descriptions, and pricing cards rendered through responsive HTML5 templates.

*Fig 2. Order Placement and Dynamic Bill Calculation (Code 4)*  
Illustrates client-side item selection, dynamic subtotal calculations, and address submission form.

*Fig 3. Order Confirmation and Receipt Generation (Code 4)*  
Shows the generated unique BSON `_id` order invoice along with detailed itemized breakdown and timestamp.

*Fig 4. Admin Management Dashboard and Statistics (Code 6a, Code 7, Code 8)*  
Displays real-time metric counters (Total Menu Items, Total Orders, Customer Count, Pending Orders) and table listings for menu item modifications and order status updates.

*Fig 5. MongoDB Compass Document Viewer (Code 1, Code 4)*  
Visualizes the native JSON documents stored in `restaurant_db` across collections, highlighting nested BSON types and embedded arrays.

---

# 5.0 Challenges and Solutions

### 5.1 Technical Challenges
*(a) BSON ObjectId Handling in Web Views:* MongoDB produces non-string `ObjectId` types for document identifiers (`_id`). Direct serialization into HTML templates or JSON APIs produced `TypeError: Object of type ObjectId is not JSON serializable`.  
*(b) Embedded Document Calculation vs. Redundancy:* Balancing whether line items inside orders should reference menu items by ID or embed name and price snapshots to safeguard historical billing integrity against future menu price updates.  
*(c) Analytical Computation Over Nested Arrays:* Extracting metrics (e.g., top selling dishes) across orders where items are embedded inside variable-length arrays.  
*(d) Jinja2 Attribute Collision with Python Dictionary Methods:* When rendering orders in the admin dashboard, accessing `order.items` caused Jinja2 to bind to Python's built-in `dict.items()` method whenever a document lacked an `"items"` array or was incomplete, throwing `TypeError: object of type 'builtin_function_or_method' has no len()`.  
*(e) Local MongoDB Connection Resolution:* Connecting with standard `mongodb://localhost:27017/` occasionally encountered DNS / IPv6 timeout latency issues (`127.0.0.1` vs `::1`) in modern local runtime environments and standalone `mongosh` shells.

### 5.2 Design Challenges
*(a) Schema Normalization vs. Denormalization Tradeoff:* Designing collections to minimize read latency for customer-facing views while maintaining clean customer and menu catalogs.  
*(b) Responsive UI Without Complex Frameworks:* Providing interactive order quantity controls and real-time total computation without loading heavy single-page application (SPA) client libraries.

### 5.3 How Issues Were Resolved
*(a) Explicit ObjectId Casting & Jinja Conversions:* Applied explicit Python `str(ObjectId)` and `ObjectId(id_str)` sanitization across all routing parameters and aggregation steps.  
*(b) Snapshot Embedding Pattern:* Adopted the snapshot schema design pattern. Historical orders embed the exact price and name at time-of-purchase, while retaining the referenced `item_id` for traceability.  
*(c) MongoDB Aggregation Framework:* Solved nested array querying using the `$unwind` operator, which deconstructs the `items` array from each order document to generate individual documents for each element, allowing seamless `$group` and `$sum` operations.  
*(d) Defensive Backend Data Sanitization & Template Type Guards:* Resolved the Jinja2 collision by: (1) sanitizing all order documents in `app.py` before template rendering to ensure `"items"` is always guaranteed to be a Python list, and (2) updating Jinja2 templates (`admin.html` and `order_detail.html`) to access `order['items']` using dictionary bracket notation along with type checking (`is iterable and is not mapping`).  
*(e) Direct Connection String Configuration:* Updated the MongoDB connection string to explicitly target `127.0.0.1` with `directConnection=true` and `serverSelectionTimeoutMS=2000`, matching `mongosh 2.12.0` client parameters for instantaneous connection establishment without topology discovery overhead.

---

# 6.0 Conclusion
The Restaurant Food Ordering System (*FoodieSpot*) demonstrates the architectural advantages and pragmatic implementation of MongoDB as a document-oriented NoSQL database. Through its document model, the application handles complex, hierarchical order data with embedded line items without requiring relational joins. 

Key outcomes accomplished during this project include:
1. Designing scalable BSON schemas that naturally represent real-world restaurant operations.
2. Delivering comprehensive CRUD functionality coupled with upsert semantics and regex search capabilities.
3. Exploiting MongoDB’s Aggregation Pipeline to generate instant operational and sales insights.
4. Implementing resilient backend validation and defensive template guards to avoid runtime dictionary-method collisions.
5. Integrating a clean, production-ready Python Flask web interface that interacts seamlessly with MongoDB via PyMongo.

The project demonstrates how NoSQL databases reduce developmental complexity, eliminate schema migration friction, and support modern, data-intensive web applications.

---

# 7.0 References

### 7.1 Book References
1. Chodorow, Kristina. *MongoDB: The Definitive Guide: Powerful and Scalable Data Storage*. 3rd ed., O'Reilly Media, 2020.
2. Banker, Kyle, et al. *MongoDB in Action: Covers MongoDB 3.0*. 2nd ed., Manning Publications, 2016.
3. Sadalage, Pramod J., and Martin Fowler. *NoSQL Distilled: A Brief Guide to the Emerging World of Polyglot Persistence*. Addison-Wesley Professional, 2012.

### 7.2 Web References
1. MongoDB Official Documentation: *CRUD Operations and Aggregation Pipeline*. https://www.mongodb.com/docs/manual/
2. PyMongo Documentation: *Python Driver for MongoDB*. https://pymongo.readthedocs.io/
3. Flask Documentation (v3.0.x): *Pallets Projects*. https://flask.palletsprojects.com/
4. Bootstrap 5.3 Framework Reference. https://getbootstrap.com/docs/5.3/
