import os.path
from flask import Flask, render_template, request
import json
app = Flask(__name__)

JSON_FILE = 'data.json'

def read_todos():
    if not os.path.exists(JSON_FILE):
        return []

    with open(JSON_FILE, 'r+') as data_file:
        todos = json.load(data_file)
    return todos

def save_todos(todos):
    with open(JSON_FILE, 'w+') as data_file:
        json.dump(todos, data_file)

def find_todo(todos, id):
    for i in range(len(todos)):
        if todos[i]['id'] == int(id):
            return i
    return -1

@app.route('/')
def index():
    todos = read_todos()
    return render_template('index.html', todos=todos)

@app.route('/todos', methods=['GET'])
def todos_get():
    todos = read_todos()
    return render_template('todos.html', todos=todos)

@app.route('/todos/', methods=['POST'])
def todos_post():
    if request.form['text'] == '':
        return ('', 200)

    todos = read_todos()

    id = 1
    if len(todos) > 0:
        id = todos[-1]['id'] + 1

    todos.append({
        'id': id,
        'text': request.form['text'],
        'complete': False
    })

    save_todos(todos)
    return render_template('todo_form.html')

@app.route('/todos/<id>', methods=['DELETE'])
def todos_delete(id):
    todos = read_todos()
    todos.pop(find_todo(todos, id))

    save_todos(todos)
    return('', 200)

@app.route('/todos/<id>', methods=['PUT'])
def toggle_todo(id):
    todos = read_todos()
    i = find_todo(todos, id)
    todos[i]['complete'] = not todos[i]['complete']
    
    save_todos(todos)
    return('', 200)

if __name__ == '__main__':
    Flask.run(app)
