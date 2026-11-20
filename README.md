# FoodieSpot — Restaurant Food Ordering System
## NoSQL Mini Project (MongoDB + Python Flask)
MCA Programme | 25MCAG301 - NoSQL Databases | Activity-2

---

## 📌 Project Overview
FoodieSpot is a full-featured web application demonstrating real-world NoSQL database architecture using **MongoDB** and **Python (Flask)**. It showcases:
- **Flexible Schema Design:** Nested documents & arrays for multi-item orders.
- **Complete CRUD Operations:** Create, Read, Update, Delete across collections.
- **Upsert Patterns:** Dynamic customer record management using `update_one(..., upsert=True)`.
- **Text & Regex Search:** Multi-field pattern searching across categories, dish names, and descriptions.
- **Aggregation Pipeline:** Real-time analytics on sales volume, top-selling dishes, and revenue status.

---

## 📂 Project Directory Structure

```
nosql-mini-project/
├── app.py                  # Main Flask application with PyMongo routes
├── mongo_queries.py        # Standalone script demonstrating all MongoDB queries
├── requirements.txt        # Python package dependencies
├── README.md               # Quick start & documentation
├── PROJECT_REPORT.md       # Complete Jain University format project report
└── templates/              # Jinja2 HTML templates (Bootstrap 5)
    ├── base.html           # Common layout & navigation
    ├── index.html          # Menu catalog (Categorized view)
    ├── admin.html          # Admin dashboard & management
    ├── menu_form.html      # Add & Edit menu items
    ├── menu_detail.html    # Single item view
    ├── order_form.html     # Customer ordering page with live total calculation
    ├── order_detail.html   # Order invoice & tracking confirmation
    ├── search_results.html # Search results view
    └── customers.html      # Customer registry
```

---

## 🚀 Quick Setup & Execution Guide

### 1. Prerequisites
- Python 3.9+ installed
- MongoDB installed locally on port `27017` (or use a free [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) URI)

### 2. Install Dependencies
```bash
pip install flask pymongo
```

### 3. Run the Application
```bash
cd C:\Users\harsh\.gemini\antigravity\scratch\nosql-mini-project
python app.py
```

*Note:* On initial startup, `app.py` automatically populates the `menu_items` collection with 10 sample dishes across starters, main courses, pizzas, beverages, and desserts!

### 4. Open in Browser
- **Customer Menu Portal:** [http://localhost:5000/](http://localhost:5000/)
- **Place an Order:** [http://localhost:5000/order](http://localhost:5000/order)
- **Admin Dashboard:** [http://localhost:5000/admin](http://localhost:5000/admin)
- **Menu Search:** [http://localhost:5000/search](http://localhost:5000/search)
- **Analytics API (Aggregation):** [http://localhost:5000/api/stats](http://localhost:5000/api/stats)

---

## 🛠️ MongoDB Collections & Schema Reference

### 1. `menu_items`
```json
{
  "_id": ObjectId("..."),
  "name": "Chicken Biryani",
  "category": "Main Course",
  "price": 349.0,
  "description": "Fragrant basmati rice layered with spiced chicken and aromatic herbs",
  "is_available": true,
  "image_url": "https://...",
  "created_at": ISODate("...")
}
```

### 2. `orders`
```json
{
  "_id": ObjectId("..."),
  "customer_name": "Aarav Sharma",
  "customer_phone": "9876543210",
  "customer_address": "42 MG Road, Bengaluru",
  "items": [
    {
      "item_id": ObjectId("..."),
      "name": "Chicken Biryani",
      "price": 349.0,
      "quantity": 2,
      "subtotal": 698.0
    }
  ],
  "total_amount": 698.0,
  "status": "Pending",
  "ordered_at": ISODate("...")
}
```

### 3. `customers`
```json
{
  "_id": ObjectId("..."),
  "phone": "9876543210",
  "name": "Aarav Sharma",
  "address": "42 MG Road, Bengaluru",
  "last_order_at": ISODate("...")
}
```

---

## 📊 Summary of MongoDB Concepts Implemented

| Concept | Implementation in Project |
| :--- | :--- |
| **Document Embedding** | Ordered items are embedded directly in the `orders` document |
| **CRUD: Create** | `insert_one()` for menu items and customer orders |
| **CRUD: Read** | `find()`, `find_one()` with category filtering and sorting |
| **CRUD: Update** | `update_one()` with `$set` for status and prices |
| **Upsert Pattern** | Customer records created or updated using `upsert=True` |
| **CRUD: Delete** | `delete_one()` for menu items and canceled orders |
| **Pattern Search** | `$regex` case-insensitive queries across 3 fields |
| **Aggregation Pipeline** | `$unwind` $\rightarrow$ `$group` $\rightarrow$ `$sort` $\rightarrow$ `$limit` |
