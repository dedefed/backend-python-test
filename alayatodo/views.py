from flask_login import login_user, login_required, current_user, logout_user

from alayatodo import app, login_manager, db
from alayatodo.forms import LoginForm, TodoForm
from alayatodo.models.user_model import User
from alayatodo.models.todo_model import Todo
from flask import (
    g,
    redirect,
    render_template,
    request,
    session,
    flash, jsonify, url_for)


@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    login_form = LoginForm()
    return render_template('login.html', form=login_form)


@app.route('/login', methods=['POST'])
def login_POST():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('todos'))
        else:
            return redirect(url_for('login'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/todo/<id>', methods=['GET'])
@login_required
def todo(id):
    todo = Todo.query.filter_by(id=id, user_id=current_user.id).first()
    return render_template('todo.html', todo=todo)


@app.route('/todo/<id>/json', methods=['GET'])
@login_required
def todo_to_json(id):
    todo = Todo.query.filter_by(id=id, user_id=current_user.id).first()
    return jsonify(todo.to_dict())


@app.route('/todos', methods=['GET'])
@app.route('/todos/', methods=['GET'])
@app.route('/todos/<page>', methods=['GET'])
@login_required
def todos(page=1):
    todos = Todo.query.filter_by(user_id=current_user.id).paginate(page=int(page), per_page=4, error_out=False)
    todo_form = TodoForm()
    return render_template('todos.html', todos=todos, form=todo_form)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
@login_required
def todos_POST():
    form = TodoForm()
    if form.validate_on_submit():
        todo = Todo(description=form.description.data, user_id=current_user.id)
        db.session.add(todo)
        db.session.commit()
        flash("Todo Created")

    return redirect(url_for('todos'))


@app.route('/todo/<id>', methods=['POST'])
@login_required
def todo_delete(id):
    todo = Todo.query.filter_by(id=id, user_id=current_user.id).first()
    if todo is None:
        return redirect(url_for('todos'))
    db.session.delete(todo)
    db.session.commit()
    flash("Todo removed")
    return redirect(url_for('todos'))


@app.route('/todo/<status>/<id>/', methods=['POST'])
@login_required
def todo_completed(id, status):
    todo = Todo.query.filter_by(id=id, user_id=current_user.id).first()
    if todo is None:
        return redirect(url_for('todos'))
    if status == 'done':
        todo.is_completed = True
        flash("Todo completed")
    elif status == 'undone':
        todo.is_completed = False
        flash("Todo not completed")
    else:
        return redirect(url_for('todos'))

    db.session.commit()
    return redirect(url_for('todos'))


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login'))
