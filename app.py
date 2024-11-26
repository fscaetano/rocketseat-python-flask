from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)

tasks = []
task_id_control = 1

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_control

    data = request.get_json()

    id = task_id_control
    task_id_control += 1

    # ttile is mandatoory
    # description is optional, so "" is the default
    new_task = Task(id, title=data["title"], description=data.get("description", ""))
    tasks.append(new_task)
    print(tasks, new_task)
    return jsonify({"message": "Nova tarefa criada com sucesso", "id":new_task.id})


@app.route('/tasks', methods=['GET'])
def get_tasks():
    task_list = [ task.to_dict() for task in tasks ]
    output  = {
        "tasks":task_list, 
        "total_tasks":len(task_list)
        }
    return jsonify(output)


@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    # task_list = [task.to_dict() for task in tasks if task.id == id]
    # if len(task_list) > 0:
    #     return jsonify(task_list[0])

    for task in tasks:
        if task.id == id:
            return jsonify(task.to_dict())
    
    return jsonify({"message":f"Task id {id} not found."}), 404


@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break

    if task is None:
        return jsonify({"message":f"Task id {id} not found."}), 404

    data = request.get_json()
    task.title = data.get("title", "")
    task.description = data.get("description", "")
    task.completed = data.get("completed", "")
    return jsonify({"message":f"Task id {id} updated successfully."})


@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            # note: do not modify the list during iteration!
            task = t
            break

    if task is None:
        return jsonify({"message":f"Task id {id} not found."}), 404

    tasks.remove(task)
    return jsonify({"message":f"Task id {id} deleted successfully."})


# dev-only app init
if __name__=="__main__":
    app.run(debug=True)

