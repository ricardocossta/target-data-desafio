from flask import Flask, render_template, redirect, url_for, request, flash
from flask_security import Security, UserMixin, RoleMixin
from flask_mongoengine import MongoEngine
from flask_security.datastore import MongoEngineUserDatastore
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
from mongoengine import *

from crud_pymongo.crud_pymongo import crud_pymongo_blueprint
from todo_list.todo_list import todo_list_blueprint
from crud_elasticsearch.crud_elasticsearch import crud_elasticsearch_blueprint


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

app.register_blueprint(crud_pymongo_blueprint)
app.register_blueprint(todo_list_blueprint)
app.register_blueprint(crud_elasticsearch_blueprint)

# DB Config
app.config['MONGODB_SETTINGS'] = {
    'db': 'estabelecimentosdb',
    'host': 'localhost',
    'port': 27017,
    'username': 'root',
    'password': 'root'
}

db = MongoEngine(app)


class Role(Document, RoleMixin):
    name = StringField(max_length=80, unique=True)
    description = StringField(max_length=255)


class User(Document, UserMixin):
    email = StringField(max_length=255, unique=True)
    password = StringField(max_length=255)
    active = BooleanField(default=True)
    roles = ListField(ReferenceField(Role), default=[])


user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.objects(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))

        flash('Email ou senha inválidos.')
        return redirect(url_for('signin'))
    return render_template('security/login_user.html')


login_manager = LoginManager()
login_manager.login_view = 'signin'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if User.objects(email=email).first():
            flash('Este email já está cadastrado.')
            return redirect(url_for('register'))

        hash_pwd = generate_password_hash(password)
        user = user_datastore.create_user(email=email, password=hash_pwd)
        login_user(user)
        return redirect(url_for('home'))
    return render_template('security/register_user.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('signin'))


@app.route('/home')
@login_required
def home():
    return render_template('home.html', email=current_user.email)


if __name__ == '__main__':
    app.run(debug=True)