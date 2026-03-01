from flask import Blueprint, request, jsonify
from src.models.mysql_models import db, Product, Inventory
from src.models.mongo_models import ActivityLog

products_bp = Blueprint('products', __name__)

@products_bp.route('/', methods=['POST'])
def create_product():
    data = request.json
    name = data.get('name')
    price = data.get('price')
    description = data.get('description', '')
    quantity = data.get('quantity', 0)

    if not all([name, price]):
        return jsonify({"error": "Name and price are required"}), 400

    try:
        new_product = Product(name=name, price=price, description=description)
        db.session.add(new_product)
        db.session.flush() # Get product ID
        
        # Add to inventory
        inventory = Inventory(product_id=new_product.id, quantity=quantity)
        db.session.add(inventory)
        
        db.session.commit()
        
        ActivityLog.log_activity('system', 'create_product', {"product_id": new_product.id, "name": name})
        
        # Return complete data
        data_to_return = new_product.to_dict()
        data_to_return['inventory'] = inventory.to_dict()
        
        return jsonify({"message": "Product created", "product": data_to_return}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@products_bp.route('/', methods=['GET'])
def get_products():
    # Demonstrating simple join implicitly through relationships (or explicitly)
    products = Product.query.all()
    result = []
    for p in products:
        p_dict = p.to_dict()
        p_dict['quantity'] = p.inventory.quantity if p.inventory else 0
        result.append(p_dict)
        
    return jsonify({"products": result}), 200

@products_bp.route('/<int:product_id>', methods=['PUT'])
def update_product_price(product_id):
    data = request.json
    new_price = data.get('price')

    if not new_price:
        return jsonify({"error": "Price is required to update"}), 400

    product = Product.query.get(product_id)
    if not product:
         return jsonify({"error": "Product not found"}), 404

    old_price = float(product.price)
    product.price = new_price
    db.session.commit()

    ActivityLog.log_activity('system', 'update_product_price', {"product_id": product_id, "old_price": old_price, "new_price": new_price})
    return jsonify({"message": "Price updated successfully", "product": product.to_dict()}), 200

@products_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
         return jsonify({"error": "Product not found"}), 404

    # Deleting product cascades to Inventory and prevents delete if ordered (RESTRICT)
    try:
        db.session.delete(product)
        db.session.commit()
        ActivityLog.log_activity('system', 'delete_product', {"product_id": product_id})
        return jsonify({"message": "Product deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e), "message": "Cannot delete product that is part of an order"}), 400
