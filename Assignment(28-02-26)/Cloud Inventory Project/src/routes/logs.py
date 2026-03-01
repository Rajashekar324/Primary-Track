from flask import Blueprint, request, jsonify
from src.models.mongo_models import ActivityLog
from datetime import datetime

logs_bp = Blueprint('logs', __name__)

@logs_bp.route('/', methods=['GET'])
def get_logs():
    """Fetch logs from MongoDB, optionally filter by user_id, action, or date range"""
    user_id = request.args.get('user_id')
    
    # Implement filtering by date
    start_date = request.args.get('start_date') # Format: YYYY-MM-DD
    end_date = request.args.get('end_date') # Format: YYYY-MM-DD
    
    collection = ActivityLog.get_collection()
    if collection is None:
         return jsonify({"error": "MongoDB not connected"}), 500
         
    query = {}
    if user_id:
        query['user_id'] = user_id
        
    if start_date or end_date:
        query['timestamp'] = {}
        if start_date:
             query['timestamp']['$gte'] = datetime.strptime(start_date, '%Y-%m-%d')
        if end_date:
             # Make it inclusive of the end date till 23:59:59
             end_datetime = datetime.strptime(end_date + " 23:59:59", '%Y-%m-%d %H:%M:%S')
             query['timestamp']['$lte'] = end_datetime

    cursor = collection.find(query).sort('timestamp', -1).limit(100)
    
    logs = []
    for doc in cursor:
        doc['_id'] = str(doc['_id'])
        if 'timestamp' in doc:
            doc['timestamp'] = doc['timestamp'].isoformat()
        logs.append(doc)
        
    return jsonify({"logs": logs}), 200
