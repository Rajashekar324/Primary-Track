from flask import Flask, render_template, request, redirect

app = Flask(__name__)

tasks = []
task_id = 1

# READ - Show Tasks
@app.route('/')
def home():
    return render_template('index.html', tasks=tasks)

# CREATE - Add Task
@app.route('/add', methods=['POST'])
def add_task():
    global task_id
    title = request.form['title']

    if title != "":
        task = {
            "id": task_id,
            "title": title,
            "status": "pending"
        }
        tasks.append(task)
        task_id += 1

    return redirect('/')

# DELETE - Remove Task
@app.route('/delete/<int:id>')
def delete_task(id):
    global tasks
    tasks = [task for task in tasks if task["id"] != id]
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)