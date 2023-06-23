from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import asc

from models import db, ToDo

app = Flask(__name__, static_url_path='/static')

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/todos", methods=["GET", "POST"])
def todos():
    if request.method == "GET":
        todos = ToDo.query.order_by(asc(ToDo.mark_as_done)).all()
        return render_template("todos.html", todos=todos)

    if request.method == "POST":
        todo_id = request.form.get("id")
        todo = ToDo.query.get(todo_id)
        if todo:
            action = request.form.get("action")
            if action == "delete":
                db.session.delete(todo)
            elif action == "mark_done":
                todo.mark_as_done = True
            elif action == "mark_undone":
                todo.mark_as_done = False
            db.session.commit()

    todos = ToDo.query.order_by(asc(ToDo.mark_as_done)).all()
    return render_template("todos.html", todos=todos)


@app.route("/todos/add", methods=["GET", "POST"])
def add_todos():
    if request.method == "POST":
        create_todo = request.form["create_todo"]
        todo = ToDo(create_todo=create_todo)
        db.session.add(todo)
        db.session.commit()
        todos = ToDo.query.order_by(asc(ToDo.mark_as_done)).all()

        return render_template("todos.html", todos=todos)

    return render_template("todos_add.html")


@app.route("/todos/<int:todo_id>/edit", methods=["GET", "POST"])
def todo_edit(todo_id):
    todo = ToDo.query.get_or_404(todo_id)

    if request.method == "POST":
        todo.create_todo = request.form.get("create_todo")
        db.session.commit()
        return redirect(url_for('todos'))

    return render_template("todos_edit.html", todo=todo)


if __name__ == "__main__":
    app.run(debug=True)
