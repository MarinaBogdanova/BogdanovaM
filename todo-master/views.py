from flask import render_template, request, redirect, flash
from flask_login import *
from flask_login import UserMixin, login_user, login_required, current_user, logout_user

from models import Category, Todo, db
from todoapp import app

login_manager = LoginManager()
login_manager.init_app(app)

users = {'user': {'pw': 'user', 'status': 'user'}, 'admin': {'pw': 'admin', 'status': 'admin'}}


class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return
    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return
    user = User()
    user.id = email
    user.is_authenticated = request.form['pw'] == users[email]['pw']
    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'></input>
                <input type='password' name='pw' id='pw' placeholder='password'></input>
                <input type='submit' name='submit'></input>
               </form>
               '''
    email = request.form['email']
    if request.form['pw'] == users[email]['pw']:
        user = User()
        user.id = email
        login_user(user)
        return redirect('/?page=1')
    return 'Bad login'


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/?page=1')


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect('/login')


@app.route('/')
@login_required
def list_all():
    page = request.args.get('page')
    sort = request.args.get('sort')
    if sort == 'desc':
        return render_template('list.html', categories=Category.query.all(), todos=Todo.query.order_by(Todo.id.desc()).limit(50).offset((int(page) - 1) * 50).all())
    return render_template('list.html', categories=Category.query.all(), todos=Todo.query.order_by(Todo.id).limit(50).offset((int(page) - 1) * 50).all())


@app.route('/category/<name>')
@login_required
def list_todos(name):
    page = request.args.get('page')
    sort = request.args.get('sort')
    category = Category.query.filter_by(name=name).first()
    if sort == 'desc':
        return render_template('list.html', todos=Todo.query.filter_by(category=category).order_by(Todo.id.desc()).limit(50).offset((int(page) - 1) * 50).all(), categories=Category.query.all())
    return render_template('list.html', todos=Todo.query.filter_by(category=category).order_by(Todo.id).limit(50).offset((int(page) - 1) * 50).all(), categories=Category.query.all())


@app.route('/new-task', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        category = Category.query.filter_by(id=request.form['category']).first()
        todo = Todo(category=category, description=request.form['description'])
        db.session.add(todo)
        db.session.commit()
        return redirect('/?page=1')
    else:
        return render_template('new-task.html', page='new-task', categories=Category.query.all(), )


@app.route('/update/<int:todo_id>', methods=['GET', 'POST'])
@login_required
def update_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if request.method == 'GET':
        return render_template('new-task.html', todo=todo, categories=Category.query.all())
    else:
        category = Category.query.filter_by(id=request.form['category']).first()
        description = request.form['description']
        todo.category = category
        todo.description = description
        db.session.commit()
        return redirect('/?page=1')


@app.route('/new-category', methods=['GET', 'POST'])
@login_required
def new_category():
    if users[current_user.id]['status'] == 'admin':
        if request.method == 'POST':
            print(request.form['category'])
            category = Category(name=request.form['category'])
            db.session.add(category)
            db.session.commit()
            return redirect('/?page=1')
        else:
            return render_template('new-category.html', page='new-category.html')
    return 'Only for admin'


@app.route('/edit_category/<int:category_id>', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    if users[current_user.id]['status'] == 'admin':
        category = Category.query.get(category_id)
        if request.method == 'GET':
            return render_template('new-category.html', category=category)
        else:
            category_name = request.form['category']
            category.name = category_name
            db.session.commit()
            return redirect('/?page=1')
    return 'Only for admin'


@app.route('/delete-category/<int:category_id>', methods=['POST'])
@login_required
def delete_category(category_id):
    if users[current_user.id]['status'] == 'admin':
        if request.method == 'POST':
            category = Category.query.get(category_id)
            if not category.todos:
                db.session.delete(category)
                db.session.commit()
            else:
                flash('You have TODOs in that category. Remove them first.')
            return redirect('/?page=1')
    return 'Only for admin'


@app.route('/delete-todo/<int:todo_id>', methods=['POST'])
@login_required
def delete_todo(todo_id):
    if request.method == 'POST':
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
        return redirect('/?page=1')


@app.route('/mark-done/<int:todo_id>', methods=['POST'])
@login_required
def mark_done(todo_id):
    if request.method == 'POST':
        todo = Todo.query.get(todo_id)
        todo.is_done = True
        db.session.commit()
        return redirect('/?page=1')
