from flask import Flask, render_template, Blueprint
from flask_login import login_required

todo_list_blueprint = Blueprint('todo_list', __name__, template_folder='templates', url_prefix='/todo_list',
                                static_folder='static')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'


@todo_list_blueprint.route('/')
@login_required
def index():
    return render_template('index_todo_list.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int("5000"), debug=True)
