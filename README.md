# FoodieSpot — Restaurant Food Ordering System
## NoSQL Mini Project (MongoDB + Python Flask)
**JAIN (Deemed-to-be University)**  
*School of Computer Science and IT* | **MCA Programme**  
Course: **25MCAG301 - NoSQL Databases** | Activity-2: Mini Project

---

## 📌 Project Overview
**FoodieSpot** is a complete, full-stack food ordering and restaurant management platform developed to demonstrate core **NoSQL** database principles using **MongoDB** and **Python (Flask)**. 

Unlike traditional relational schemas (RDBMS) that require expensive joins and rigid migration penalties, FoodieSpot leverages MongoDB's BSON document model:
- **Embedded Document Architecture:** Orders store item arrays atomically, guaranteeing lightning-fast reads and historical snapshot preservation.
- **Dynamic Schema Flexibility:** Add ingredients, custom dietary labels, or image metadata without running database migrations.
- **Robust CRUD Implementation:** Complete document lifecycle handling (Create, Read, Update, Delete) across collections.
- **Atomic Upsert Logic:** Automatically register or update customer profiles during order placement via `update_one(..., upsert=True)`.
- **Text & Regex Search:** Multi-attribute pattern matching over dish names, categories, and culinary descriptions using `$regex` and `$or`.
- **Analytical Aggregation Pipelines:** Real-time metrics reporting (top dishes by volume, sales revenue by fulfillment state) with multi-stage `$unwind`, `$group`, `$sort`, and `$limit`.

---

## 📂 Project Structure

```
nosql-mini-project/
├── app.py                  # Core Flask backend with PyMongo routes & MongoDB connection
├── mongo_queries.py        # Standalone script demonstrating isolated MongoDB queries
├── requirements.txt        # Python package dependencies
├── README.md               # Complete project documentation & setup guide
├── PROJECT_REPORT.md       # Full JAIN University formatted project report
└── templates/              # Jinja2 HTML5 / Bootstrap 5 responsive templates
    ├── base.html           # Base layout, navbar, search bar & footer
    ├── index.html          # Interactive customer menu catalog (categorized view)
    ├── admin.html          # Admin metrics dashboard & order status management
    ├── menu_form.html      # Create & Edit menu item interface
    ├── menu_detail.html    # Single dish showcase view
    ├── order_form.html     # Real-time cart calculation & customer checkout
    ├── order_detail.html   # Invoice receipt & live fulfillment status
    ├── search_results.html # Dynamic search results display
    └── customers.html      # Registered customer directory
```

---

## ⚙️ MongoDB Connection Details

By default, the application connects to your local MongoDB instance with direct connection parameters enabled:

```python
MONGO_URI = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.12.0"
```

- **Target Database:** `restaurant_db`
- **Collections:**
  - `menu_items` — Food catalog, pricing, category, availability flags.
  - `orders` — Customer orders with embedded item subdocument arrays.
  - `customers` — Customer contact directory with last active timestamps.

*(Optional)* You can override the connection URI anytime by exporting the `MONGO_URI` environment variable:
```bash
set MONGO_URI="mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority"
```

---

## 🚀 Quick Setup & Execution Guide

### 1. Prerequisites
- **Python 3.10+**
- **MongoDB Community Server (v6.0+)** running locally on port `27017` (or a MongoDB Atlas connection string)
- **MongoDB Compass / `mongosh`** (recommended for visually verifying documents)

### 2. Set Up Virtual Environment (Recommended)
```bash
cd C:\Users\harsh\.gemini\antigravity\scratch\nosql-mini-project
python -m venv .venv

# Activate Virtual Environment:
# On Windows (Command Prompt / PowerShell):
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
*(Dependencies: `flask>=3.0`, `pymongo>=4.6`)*

### 4. Run the Web Application
```bash
python app.py
```
> **Automatic Data Seeding:** Upon first execution, `app.py` automatically initializes `menu_items` with a diverse culinary catalog (Starters, Main Course, Pizza, Desserts, Beverages) if the collection is empty.

### 5. Access the Web Application
Open your web browser and navigate to:
| Portal | URL | Description |
| :--- | :--- | :--- |
| **Customer Menu** | [http://localhost:5000/](http://localhost:5000/) | Browse dishes grouped by category with live availability badges |
| **Place an Order** | [http://localhost:5000/order](http://localhost:5000/order) | Interactive ordering interface with real-time bill calculation |
| **Admin Dashboard** | [http://localhost:5000/admin](http://localhost:5000/admin) | Real-time statistics counters, order management & menu controls |
| **Catalog Search** | [http://localhost:5000/search](http://localhost:5000/search) | Regex-powered search across dish names, categories & descriptions |
| **Customer Directory** | [http://localhost:5000/customers](http://localhost:5000/customers) | View registered customer profiles and order histories |
| **Aggregation Analytics API** | [http://localhost:5000/api/stats](http://localhost:5000/api/stats) | JSON output of multi-stage analytics pipeline |

---

## 💻 Standalone MongoDB Queries Test Script

To verify all MongoDB query constructs outside of the Flask browser interface, execute:

```bash
python mongo_queries.py
```

This runs a CLI suite demonstrating:
1. `insert_one` document creation.
2. `find()` with projection and sorting.
3. `$regex` pattern matching.
4. `update_one` with `$set` and customer `upsert=True`.
5. Embedded document insertion for multi-item orders.
6. Multi-stage Aggregation Pipeline (`$unwind` $\rightarrow$ `$group` $\rightarrow$ `$sort` $\rightarrow$ `$limit`).
7. `delete_one` document cleanup.

---

## 🛠️ Data Modeling & Collections Architecture

### 1. `menu_items` Collection
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

### 2. `orders` Collection (Embedded Document Pattern)
```json
{
  "_id": ObjectId("67389c22c45ef2018a101aa3"),
  "customer_name": "Aarav Sharma",
  "customer_phone": "9876543210",
  "customer_address": "42 MG Road, Bengaluru",
  "items": [
    {
      "item_id": ObjectId("67389a0bc45ef2018a101aa1"),
      "name": "Chicken Biryani",
      "price": 349.0,
      "quantity": 2,
      "subtotal": 698.0
    },
    {
      "item_id": ObjectId("67389a0bc45ef2018a101aa5"),
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

### 3. `customers` Collection
```json
{
  "_id": ObjectId("67389b14c45ef2018a101aa2"),
  "phone": "9876543210",
  "name": "Aarav Sharma",
  "address": "42 MG Road, Bengaluru",
  "last_order_at": ISODate("2026-11-20T18:05:00.000Z")
}
```

---

## 📊 Summary of NoSQL Concepts Implemented

| Core NoSQL Concept | MongoDB Operator / Method | Project Implementation |
| :--- | :--- | :--- |
| **Document Embedding** | Nested Arrays of Subdocuments | Line items stored inside `orders.items` snapshotting price & quantity |
| **CRUD: Create** | `insert_one()`, `insert_many()` | Adding menu items, seeding initial catalog, creating customer orders |
| **CRUD: Read** | `find()`, `find_one()` | Categorized menu queries, single item detail pages, customer lookups |
| **CRUD: Update** | `update_one()` with `$set` | Modifying dish details, updating order fulfillment status |
| **Atomic Upsert** | `update_one(..., upsert=True)` | Automatic customer registration without duplicate phone records |
| **CRUD: Delete** | `delete_one()` | Admin deletion of outdated dishes and cancelled orders |
| **Pattern Search** | `$regex`, `$options: 'i'`, `$or` | Case-insensitive multi-field search across catalog |
| **Aggregation Pipeline** | `$unwind` $\rightarrow$ `$group` $\rightarrow$ `$sort` | Calculating top-selling dishes by volume and order revenue by status |

---

## 🛡️ Recent Bug Fixes & Reliability Improvements
- **Template Attribute Collision (`dict.items` vs `order.items`):** Fixed `TypeError: object of type 'builtin_function_or_method' has no len()` in `admin.html` and `order_detail.html` by enforcing safe type checks and pre-sanitizing order documents in backend view handlers.
- **Robust Local Connection String:** Updated connection defaults with `directConnection=true` and explicit client metadata for complete compatibility with modern MongoDB 6.0/7.0 and `mongosh` environments.

---

## 📜 Academic Attribution
- **Institution:** JAIN (Deemed-to-be University)
- **Programme:** Master of Computer Applications (MCA)
- **Subject:** 25MCAG301 - NoSQL Databases (Activity-2 Mini Project)
- **Comprehensive Project Report:** Refer to [`PROJECT_REPORT.md`](PROJECT_REPORT.md) for full academic submission documentation (format-compliant with all university guidelines).
