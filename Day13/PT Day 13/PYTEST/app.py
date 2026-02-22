from flask import Flask, request, jsonify

app = Flask(__name__)

tasks = []

def find_task(task_id):
    return next((task for task in tasks if task["id"] == task_id), None)

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks), 200

@app.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = find_task(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task), 200

@app.route("/api/tasks", methods=["POST"])
def create_task():
    if not request.is_json:
        return jsonify({"error": "Invalid JSON"}), 400

    data = request.get_json()

    if "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    if "completed" in data and not isinstance(data["completed"], bool):
        return jsonify({"error": "Completed must be boolean"}), 400

    new_id = max([t["id"] for t in tasks], default=0) + 1

    task = {
        "id": new_id,
        "title": data["title"],
        "description": data.get("description", ""),
        "completed": data.get("completed", False),
    }

    tasks.append(task)
    return jsonify(task), 201

@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = find_task(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    if not request.is_json:
        return jsonify({"error": "Invalid JSON"}), 400

    data = request.get_json()

    if "completed" in data and not isinstance(data["completed"], bool):
        return jsonify({"error": "Completed must be boolean"}), 400

    task["title"] = data.get("title", task["title"])
    task["description"] = data.get("description", task["description"])
    task["completed"] = data.get("completed", task["completed"])

    return jsonify(task), 200

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = find_task(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    tasks.remove(task)
    return jsonify({"message": "Task deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)
