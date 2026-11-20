"""
Restaurant Food Ordering System — NoSQL Mini Project
Built with Flask + MongoDB (PyMongo)
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# ─── MongoDB Connection ───────────────────────────────────────────────
MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.12.0"
)
client = MongoClient(MONGO_URI)
db = client["restaurant_db"]

# Collections
menu_collection = db["menu_items"]
order_collection = db["orders"]
customer_collection = db["customers"]


# ═══════════════════════════════════════════════════════════════════════
#  HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

def seed_menu():
    """Seed the menu with sample data or ensure items are refreshed."""
    # Correct broken Gulab Jamun image if already seeded
    menu_collection.update_many(
        {"name": "Gulab Jamun", "image_url": {"$regex": "photo-1666190050288"}},
        {"$set": {"image_url": "https://images.unsplash.com/photo-1666190092159-3171cf0fbb12?w=600"}}
    )

    sample_items = [
        # --- Starters ---
        {
            "name": "Crispy Paneer Tikka",
            "category": "Starters",
            "price": 249.0,
            "description": "Char-grilled cottage cheese cubes marinated in spiced yogurt and kasuri methi",
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1599488615731-7e5c2823ff28?w=600",
            "created_at": datetime.now()
        },
        {
            "name": "Smoky BBQ Chicken Wings",
            "category": "Starters",
            "price": 289.0,
            "description": "Crispy chicken wings glazed in artisanal hickory BBQ glaze with garlic dip",
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1567620832903-9fc6debc209f?w=600",
            "created_at": datetime.now()
        },
        {
            "name": "Caesar Salad",
            "category": "Starters",
            "price": 199.0,
            "description": "Crisp romaine lettuce with shaved parmesan, herbed croutons, and creamy Caesar dressing",
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1546793665-c74683f339c1?w=600",
            "created_at": datetime.now()
        },
        {
            "name": "Garlic Bread Supreme",
            "category": "Starters",
            "price": 149.0,
            "description": "Artisan toasted baguette topped with herb butter, roasted garlic, and melted mozzarella",
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1619535860434-ba1d8fa12536?w=600",
            "created_at": datetime.now()
        },
        {
            "name": "Crispy Golden Spring Rolls",
            "category": "Starters",
            "price": 189.0,
            "description": "Wok-tossed julienne vegetables encased in crispy pastry with sweet chili dip",
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=600",
            "created_at": datetime.now()
        },
        {
            "name": "Loaded Fiesta Nachos",
            "category": "Starters",
            "price": 229.0,
            "description": "Corn tortilla chips loaded with jalapeños, molten cheddar, salsa, and sour cream",
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1513456852971-30c0b8199d4d?w=600",
            "created_at": datetime.now()
        },

        # --- Pizza ---
        {
            "name": "Classic Margherita Pizza",
            "category": "Pizza",
            "price": 299.0,
            "description": "San Marzano tomato base, fresh buffalo mozzarella, aromatic basil, and olive oil drizzle",
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=600",
            "created_at": datetime.now()
        },
        {
            "name": "Rustic Farmhouse Pizza",
            "category": "Pizza",
            "price": 349.0,
            "description": "Loaded with bell peppers, sweet corn, black olives, red onions, and mozzarella",
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=600",
            "created_at": datetime.now()
        },
        {
            "name": "Spicy Pepperoni Feast",
            "category": "Pizza",
            "price": 399.0,
            "description": "Generous layers of cured spicy pepperoni and melted double mozzarella",
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1628840042765-356cda07504e?w=600",
            "created_at": datetime.now()
        },
        {
            "name": "Smoked BBQ Chicken Pizza",
            "category": "Pizza",
            "price": 379.0,
            "description": "Tender grilled BBQ chicken chunks, caramelized red onions, cilantro, and smoked cheese",
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=600",
            "created_at": datetime.now()
        },

        # --- Main Course ---
        {
            "name": "Hyderabadi Chicken Biryani",
            "category": "Main Course",
            "price": 349.0,
            "description": "Dum-cooked fragrant basmati rice layered with succulent chicken, saffron, and fried onions",
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=600",
            "created_at": datetime.now()
        },
        {
            "name": "Royal Butter Chicken",
            "category": "Main Course",
            "price": 359.0,
            "description": "Tandoori chicken simmered in a velvety buttery tomato gravy enriched with cream",
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=600",
            "created_at": datetime.now()
        },
        {
            "name": "Paneer Butter Masala",
            "category": "Main Course",
            "price": 279.0,
            "description": "Soft malai paneer cubes gently cooked in a rich, mild sweet creamy tomato gravy",
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=600",
            "created_at": datetime.now()
        },
        {
            "name": "Slow-Cooked Dal Makhani",
            "category": "Main Course",
            "price": 249.0,
            "description": "Black lentils slow simmered overnight with fresh butter, ginger, and aromatic spices",
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=600",
            "created_at": datetime.now()
        },
        {
            "name": "Veg Schezwan Fried Rice",
            "category": "Main Course",
            "price": 219.0,
            "description": "Wok-tossed long grain rice with garden fresh vegetables in zesty Schezwan sauce",
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=600",
            "created_at": datetime.now()
        },
        {
            "name": "Truffle Wild Mushroom Risotto",
            "category": "Main Course",
            "price": 369.0,
            "description": "Creamy arborio rice with porcini mushrooms, white truffle oil, and aged parmesan",
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1633964913295-ceb43826e7c9?w=600",
            "created_at": datetime.now()
        },

        # --- Desserts ---
        {
            "name": "Gulab Jamun (2 Pcs)",
            "category": "Desserts",
            "price": 99.0,
            "description": "Soft golden milk-solid dumplings soaked in rose and cardamom infused warm sugar syrup",
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1666190092159-3171cf0fbb12?w=600",
            "created_at": datetime.now()
        },
        {
            "name": "Molten Chocolate Brownie",
            "category": "Desserts",
            "price": 159.0,
            "description": "Warm Belgian chocolate brownie served with Madagascar vanilla gelato and hot fudge",
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1564355808539-22fda35bed7e?w=600",
            "created_at": datetime.now()
        },
        {
            "name": "Classic Venetian Tiramisu",
            "category": "Desserts",
            "price": 189.0,
            "description": "Espresso-soaked savoiardi ladyfingers layered with whipped mascarpone cream and cocoa",
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=600",
            "created_at": datetime.now()
        },
        {
            "name": "Kesar Pista Rasmalai",
            "category": "Desserts",
            "price": 129.0,
            "description": "Delicate cottage cheese patties soaked in thickened saffron cardamom milk with pistachios",
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=600",
            "created_at": datetime.now()
        },

        # --- Beverages ---
        {
            "name": "Alphonso Mango Lassi",
            "category": "Beverages",
            "price": 119.0,
            "description": "Velvety blend of ripe Alphonso mango pulp, churned yogurt, cardamom, and mint",
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1527661591475-527312dd65f5?w=600",
            "created_at": datetime.now()
        },
        {
            "name": "Artisanal Cold Coffee",
            "category": "Beverages",
            "price": 139.0,
            "description": "Bold espresso shot blended with chilled whole milk, ice cream, and chocolate drizzle",
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=600",
            "created_at": datetime.now()
        },
        {
            "name": "Sparkling Mint Lime Soda",
            "category": "Beverages",
            "price": 89.0,
            "description": "Freshly squeezed lime juice with crushed mint leaves, rock salt, and effervescent soda",
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=600",
            "created_at": datetime.now()
        },
        {
            "name": "Kulhad Masala Chai",
            "category": "Beverages",
            "price": 69.0,
            "description": "Authentic street-style brewed tea infused with ginger, cardamom, cinnamon, and whole milk",
            "is_available": True,
            "image_url": "https://images.unsplash.com/photo-1576092768241-dec231879fc3?w=600",
            "created_at": datetime.now()
        },
    ]

    if menu_collection.count_documents({}) == 0:
        menu_collection.insert_many(sample_items)
        print("✅ Menu seeded with 24 sample items.")
    else:
        # Insert any newly added items that don't exist yet
        for item in sample_items:
            existing = menu_collection.find_one({"name": item["name"]})
            if not existing:
                menu_collection.insert_one(item)


# ═══════════════════════════════════════════════════════════════════════
#  ROUTES — MENU (CRUD)
# ═══════════════════════════════════════════════════════════════════════

@app.route("/")
def index():
    """Home page — shows the full menu grouped by category."""
    menu_items = list(menu_collection.find().sort("category", 1))
    # Group by category
    categories = {}
    for item in menu_items:
        cat = item.get("category", "Other")
        categories.setdefault(cat, []).append(item)
    return render_template("index.html", categories=categories)


@app.route("/admin")
def admin_dashboard():
    """Admin dashboard with menu management and order overview."""
    menu_items = list(menu_collection.find().sort("category", 1))
    raw_orders = list(order_collection.find().sort("ordered_at", -1).limit(20))
    
    # Sanitize orders so 'items' is always a list and not the dict.items method
    orders = []
    for ord_doc in raw_orders:
        if "items" not in ord_doc or not isinstance(ord_doc["items"], list):
            ord_doc["items"] = []
        orders.append(ord_doc)
        
    stats = {
        "total_items": menu_collection.count_documents({}),
        "total_orders": order_collection.count_documents({}),
        "total_customers": customer_collection.count_documents({}),
        "pending_orders": order_collection.count_documents({"status": "Pending"}),
    }
    return render_template("admin.html", menu_items=menu_items, orders=orders, stats=stats)


# ── CREATE ────────────────────────────────────────────────────────────
@app.route("/menu/add", methods=["GET", "POST"])
def add_menu_item():
    """Add a new menu item."""
    if request.method == "POST":
        new_item = {
            "name": request.form["name"],
            "category": request.form["category"],
            "price": float(request.form["price"]),
            "description": request.form["description"],
            "is_available": "is_available" in request.form,
            "image_url": request.form.get("image_url", ""),
            "created_at": datetime.now(),
        }
        menu_collection.insert_one(new_item)
        flash("Menu item added successfully!", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("menu_form.html", item=None)


# ── READ ──────────────────────────────────────────────────────────────
@app.route("/menu/<item_id>")
def view_menu_item(item_id):
    """View a single menu item."""
    item = menu_collection.find_one({"_id": ObjectId(item_id)})
    if not item:
        flash("Menu item not found.", "error")
        return redirect(url_for("index"))
    return render_template("menu_detail.html", item=item)


# ── UPDATE ────────────────────────────────────────────────────────────
@app.route("/menu/edit/<item_id>", methods=["GET", "POST"])
def edit_menu_item(item_id):
    """Edit an existing menu item."""
    item = menu_collection.find_one({"_id": ObjectId(item_id)})
    if not item:
        flash("Menu item not found.", "error")
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        updated = {
            "$set": {
                "name": request.form["name"],
                "category": request.form["category"],
                "price": float(request.form["price"]),
                "description": request.form["description"],
                "is_available": "is_available" in request.form,
                "image_url": request.form.get("image_url", ""),
                "updated_at": datetime.now(),
            }
        }
        menu_collection.update_one({"_id": ObjectId(item_id)}, updated)
        flash("Menu item updated successfully!", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("menu_form.html", item=item)


# ── DELETE ────────────────────────────────────────────────────────────
@app.route("/menu/delete/<item_id>", methods=["POST"])
def delete_menu_item(item_id):
    """Delete a menu item."""
    menu_collection.delete_one({"_id": ObjectId(item_id)})
    flash("Menu item deleted.", "warning")
    return redirect(url_for("admin_dashboard"))


# ═══════════════════════════════════════════════════════════════════════
#  ROUTES — ORDERS (CRUD)
# ═══════════════════════════════════════════════════════════════════════

@app.route("/order", methods=["GET", "POST"])
def place_order():
    """Place a new order."""
    menu_items = list(menu_collection.find({"is_available": True}).sort("category", 1))

    if request.method == "POST":
        customer_name = request.form["customer_name"]
        customer_phone = request.form["customer_phone"]
        customer_address = request.form.get("customer_address", "")

        # Upsert customer
        customer_collection.update_one(
            {"phone": customer_phone},
            {"$set": {
                "name": customer_name,
                "phone": customer_phone,
                "address": customer_address,
                "last_order_at": datetime.now()
            }},
            upsert=True
        )

        # Gather selected items
        selected_ids = request.form.getlist("items")
        quantities = request.form.getlist("quantities")

        if not selected_ids:
            flash("Please select at least one item.", "error")
            return render_template("order_form.html", menu_items=menu_items)

        order_items = []
        total = 0.0
        for item_id, qty in zip(selected_ids, quantities):
            qty = int(qty) if qty else 1
            if qty < 1:
                continue
            item = menu_collection.find_one({"_id": ObjectId(item_id)})
            if item:
                subtotal = item["price"] * qty
                order_items.append({
                    "item_id": ObjectId(item_id),
                    "name": item["name"],
                    "price": item["price"],
                    "quantity": qty,
                    "subtotal": subtotal,
                })
                total += subtotal

        if not order_items:
            flash("Please select at least one item with quantity > 0.", "error")
            return render_template("order_form.html", menu_items=menu_items)

        order = {
            "customer_name": customer_name,
            "customer_phone": customer_phone,
            "customer_address": customer_address,
            "items": order_items,
            "total_amount": total,
            "status": "Pending",
            "ordered_at": datetime.now(),
        }
        result = order_collection.insert_one(order)
        flash(f"Order placed successfully! Order ID: {result.inserted_id}", "success")
        return redirect(url_for("order_confirmation", order_id=str(result.inserted_id)))

    return render_template("order_form.html", menu_items=menu_items)


@app.route("/order/<order_id>")
def order_confirmation(order_id):
    """Order confirmation / detail page."""
    order = order_collection.find_one({"_id": ObjectId(order_id)})
    if not order:
        flash("Order not found.", "error")
        return redirect(url_for("index"))
    if "items" not in order or not isinstance(order["items"], list):
        order["items"] = []
    return render_template("order_detail.html", order=order)


@app.route("/order/update/<order_id>", methods=["POST"])
def update_order_status(order_id):
    """Update order status (Admin)."""
    new_status = request.form["status"]
    order_collection.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"status": new_status, "updated_at": datetime.now()}}
    )
    flash(f"Order status updated to '{new_status}'.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/order/delete/<order_id>", methods=["POST"])
def delete_order(order_id):
    """Delete an order (Admin)."""
    order_collection.delete_one({"_id": ObjectId(order_id)})
    flash("Order deleted.", "warning")
    return redirect(url_for("admin_dashboard"))


# ═══════════════════════════════════════════════════════════════════════
#  ROUTES — CUSTOMERS (Read)
# ═══════════════════════════════════════════════════════════════════════

@app.route("/customers")
def list_customers():
    """List all customers."""
    customers = list(customer_collection.find().sort("name", 1))
    return render_template("customers.html", customers=customers)


# ═══════════════════════════════════════════════════════════════════════
#  ROUTES — SEARCH & AGGREGATION
# ═══════════════════════════════════════════════════════════════════════

@app.route("/search")
def search_menu():
    """Search menu items by name or category."""
    query = request.args.get("q", "")
    if query:
        # MongoDB text-like search using $regex
        results = list(menu_collection.find({
            "$or": [
                {"name": {"$regex": query, "$options": "i"}},
                {"category": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}},
            ]
        }))
    else:
        results = []
    return render_template("search_results.html", results=results, query=query)


@app.route("/api/stats")
def api_stats():
    """API endpoint — Aggregation pipeline for order statistics."""
    pipeline = [
        {"$unwind": "$items"},
        {"$group": {
            "_id": "$items.name",
            "times_ordered": {"$sum": "$items.quantity"},
            "total_revenue": {"$sum": "$items.subtotal"},
        }},
        {"$sort": {"times_ordered": -1}},
        {"$limit": 10},
    ]
    popular_items = list(order_collection.aggregate(pipeline))

    # Revenue by status
    status_pipeline = [
        {"$group": {
            "_id": "$status",
            "count": {"$sum": 1},
            "revenue": {"$sum": "$total_amount"},
        }}
    ]
    status_stats = list(order_collection.aggregate(status_pipeline))

    return jsonify({
        "popular_items": popular_items,
        "order_status_stats": status_stats,
    })


# ═══════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    seed_menu()
    print("🍽️  Restaurant Food Ordering System is running!")
    print("   → Customer Portal : http://localhost:5000/")
    print("   → Admin Dashboard : http://localhost:5000/admin")
    app.run(debug=True, port=5000)
