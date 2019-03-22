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
    flash)


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
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            return redirect('/todo')
        else:
            return redirect('/login')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
@login_required
def todo(id):
    todo = Todo.query.filter_by(id=id, user_id=current_user.id).first()
    return render_template('todo.html', todo=todo)


@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
@login_required
def todos():
    todos = Todo.query.filter_by(user_id=current_user.id)
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

    return redirect('/todo')


@app.route('/todo/<id>', methods=['POST'])
@login_required
def todo_delete(id):
    todo = Todo.query.filter_by(id=id, user_id=current_user.id).first()
    if todo is None:
        return redirect('/todo')
    db.session.delete(todo)
    db.session.commit()
    flash("Todo removed")
    return redirect('/todo')


@app.route('/todo/<status>/<id>/', methods=['POST'])
@login_required
def todo_completed(id, status):
    todo = Todo.query.filter_by(id=id, user_id=current_user.id).first()
    if todo is None:
        return redirect('/todo')
    if status == 'done':
        todo.is_completed = True
        flash("Todo completed")
    elif status == 'undone':
        todo.is_completed = False
        flash("Todo not completed")
    else:
        return redirect('/todo')

    db.session.commit()
    return redirect('/todo')


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')
