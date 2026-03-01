from flask import Blueprint, request, jsonify
from src.models.mysql_models import db, Order, OrderItem, Product, Inventory
from src.models.mongo_models import ActivityLog

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/', methods=['POST'])
def create_order():
    """
    Accept JSON order request. Parse nested product data.
    JSON structure:
    {
      "user_id": 1,
      "items": [
        {"product_id": 1, "quantity": 2}
      ]
    }
    """
@orders_bp.route('/', methods=['GET'])
def list_orders():
    orders = Order.query.all()
    return jsonify([o.to_dict() for o in orders]), 200
    data = request.json
    user_id = data.get('user_id')
    items = data.get('items', [])

    if not user_id or not items:
        return jsonify({"error": "Invalid request. user_id and items are required"}), 400

    try:
        # 1. Create Order barebones
        new_order = Order(user_id=user_id, status='PAID')
        db.session.add(new_order)
        db.session.flush() # Get order.id Before committing
        
        total_amount = 0.0

        # 2. Process Nested items
        for item in items:
            product_id = item.get('product_id')
            quantity = item.get('quantity')
            
            # Find product to check price and inventory
            product = Product.query.get(product_id)
            if not product:
                raise Exception(f"Product ID {product_id} not found")
                
            inventory = Inventory.query.filter_by(product_id=product_id).first()
            if not inventory or inventory.quantity < quantity:
                raise Exception(f"Insufficient stock for Product ID {product_id}")
            
            # Deduct from inventory
            inventory.quantity -= quantity
            
            # Add to OrderItem bridge table
            price_at_purchase = float(product.price)
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=product_id,
                quantity=quantity,
                price_at_purchase=price_at_purchase
            )
            db.session.add(order_item)
            
            total_amount += (price_at_purchase * quantity)
            
        # Update order total
        new_order.total_amount = total_amount
        db.session.commit()
        
        ActivityLog.log_activity(str(user_id), 'create_order', {"order_id": new_order.id, "total": total_amount})
        return jsonify({"message": "Order placed successfully", "order_id": new_order.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@orders_bp.route('/<int:order_id>', methods=['GET'])
def get_order_details(order_id):
    """
    Read Order Details with JOIN.
    Converts SQL relationship data to nested JSON.
    """
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    # Using relationships to serialize data
    order_data = order.to_dict()
    
    # Implicit JOIN via SQLAlchemy relationships
    items_data = []
    for item in order.items:
        product_name = item.product.name
        items_data.append({
            "product_id": item.product_id,
            "product_name": product_name,
            "quantity": item.quantity,
            "price_at_purchase": float(item.price_at_purchase),
            "subtotal": float(item.price_at_purchase * item.quantity)
        })
        
    order_data['items'] = items_data
    return jsonify({"order": order_data}), 200
