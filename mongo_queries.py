"""
MongoDB Shell & Driver Queries Demonstration Script
Restaurant Food Ordering System (FoodieSpot)
Covers all CRUD, Regex Search, Upsert, and Aggregation Pipeline queries.
"""

from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

MONGO_URI = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.12.0"
client = MongoClient(MONGO_URI)
db = client["restaurant_db"]

menu_col = db["menu_items"]
orders_col = db["orders"]
customers_col = db["customers"]

def demonstrate_queries():
    print("=== 1. CREATE (Insert Documents) ===")
    sample_item = {
        "name": "Paneer Tikka Roll",
        "category": "Starters",
        "price": 180.0,
        "description": "Grilled marinated paneer wrapped in flaky flatbread with mint chutney",
        "is_available": True,
        "image_url": "https://images.unsplash.com/photo-1626777552726-4a6b54c97e46?w=400",
        "created_at": datetime.now()
    }
    insert_res = menu_col.insert_one(sample_item)
    print(f"Inserted Menu Item ID: {insert_res.inserted_id}")

    print("\n=== 2. READ (Find, Filter & Projection) ===")
    starters = list(menu_col.find({"category": "Starters", "is_available": True}, {"name": 1, "price": 1, "category": 1}))
    print(f"Available Starters Count: {len(starters)}")
    for item in starters[:3]:
        print(f" - {item.get('name')}: Rs. {item.get('price')}")

    print("\n=== 3. SEARCH (Regex query) ===")
    search_term = "pizza"
    search_res = list(menu_col.find({
        "$or": [
            {"name": {"$regex": search_term, "$options": "i"}},
            {"category": {"$regex": search_term, "$options": "i"}},
            {"description": {"$regex": search_term, "$options": "i"}}
        ]
    }))
    print(f"Search results for '{search_term}': {len(search_res)} items")

    print("\n=== 4. UPDATE (Single Document & Upsert) ===")
    # Update Menu Item
    menu_col.update_one(
        {"_id": insert_res.inserted_id},
        {"$set": {"price": 199.0, "updated_at": datetime.now()}}
    )
    print("Updated price for inserted item.")

    # Customer Upsert
    cust_res = customers_col.update_one(
        {"phone": "9876543210"},
        {"$set": {
            "name": "Aarav Sharma",
            "phone": "9876543210",
            "address": "42 MG Road, Bangalore, Karnataka",
            "last_order_at": datetime.now()
        }},
        upsert=True
    )
    print(f"Customer Upserted (Matched: {cust_res.matched_count}, Modified: {cust_res.modified_count})")

    print("\n=== 5. CREATE ORDER ===")
    sample_order = {
        "customer_name": "Aarav Sharma",
        "customer_phone": "9876543210",
        "customer_address": "42 MG Road, Bangalore, Karnataka",
        "items": [
            {
                "item_id": insert_res.inserted_id,
                "name": "Paneer Tikka Roll",
                "price": 199.0,
                "quantity": 2,
                "subtotal": 398.0
            }
        ],
        "total_amount": 398.0,
        "status": "Pending",
        "ordered_at": datetime.now()
    }
    order_res = orders_col.insert_one(sample_order)
    print(f"Created Sample Order ID: {order_res.inserted_id}")

    print("\n=== 6. AGGREGATION PIPELINES ===")
    # Aggregation 1: Popular items by sales volume and revenue
    pop_pipeline = [
        {"$unwind": "$items"},
        {"$group": {
            "_id": "$items.name",
            "times_ordered": {"$sum": "$items.quantity"},
            "total_revenue": {"$sum": "$items.subtotal"}
        }},
        {"$sort": {"times_ordered": -1}},
        {"$limit": 5}
    ]
    popular = list(orders_col.aggregate(pop_pipeline))
    print("Popular Items Aggregation:", popular)

    # Aggregation 2: Revenue and count breakdown by status
    status_pipeline = [
        {"$group": {
            "_id": "$status",
            "order_count": {"$sum": 1},
            "total_revenue": {"$sum": "$total_amount"}
        }}
    ]
    status_stats = list(orders_col.aggregate(status_pipeline))
    print("Order Status Stats Aggregation:", status_stats)

    print("\n=== 7. DELETE ===")
    del_res = menu_col.delete_one({"_id": insert_res.inserted_id})
    print(f"Cleaned up inserted item, deleted count: {del_res.deleted_count}")

if __name__ == "__main__":
    print("To run this against local MongoDB:")
    print("python mongo_queries.py")
