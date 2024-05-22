from flask import Blueprint, request, jsonify
from models import db, Task
from marshmallow import Schema, fields, ValidationError

bp = Blueprint('tasks', __name__)

class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

@bp.route('/tasks', methods=['POST'])
def create_task():
    json_data = request.get_json()
    try:
        data = task_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_task = Task(
        title=data['title'],
        description=data.get('description')
    )
    db.session.add(new_task)
    db.session.commit()

    return task_schema.jsonify(new_task), 201

@bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return tasks_schema.jsonify(tasks), 200

@bp.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get_or_404(id)
    return task_schema.jsonify(task), 200

@bp.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)
    json_data = request.get_json()
    try:
        data = task_schema.load(json_data, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    
    db.session.commit()
    return task_schema.jsonify(task), 200

@bp.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully"}), 200