import os
import sys

# Add the project root directory to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from src.utils.db import SQLALCHEMY_DATABASE_URI
from src.models.mysql_models import db

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app) # Enable cross origin resource sharing for frontend
    
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize SQLAlchemy with app
    db.init_app(app)
    
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy", "service": "Cloud Inventory API"}), 200
        
    # Import and register blueprints
    from src.routes.auth import auth_bp
    from src.routes.products import products_bp
    from src.routes.orders import orders_bp
    from src.routes.logs import logs_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(orders_bp, url_prefix='/api/orders')
    app.register_blueprint(logs_bp, url_prefix='/api/logs')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=(os.getenv("FLASK_ENV") == "development"))
