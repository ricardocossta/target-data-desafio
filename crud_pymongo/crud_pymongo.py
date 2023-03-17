from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
import pymongo
from flask_login import login_required

crud_pymongo_blueprint = Blueprint('crud_pymongo', __name__, template_folder='templates', url_prefix='/crud_pymongo')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
client = pymongo.MongoClient("mongodb://localhost:27017", username='root',
                             password='root')
db = client["estabelecimentosdb"]
collection = db["estabelecimentos"]


@crud_pymongo_blueprint.route('/')
@login_required
def index():
    estabelecimentos = list(collection.find())
    return render_template('index_crud_pymongo.html', estabelecimentos=estabelecimentos)


@crud_pymongo_blueprint.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        cnpj = request.form['cnpj']
        nome = request.form['nome']
        cep = request.form['cep']
        telefone = request.form['telefone']
        email = request.form['email']

        if not request.form['telefone'].isnumeric():
            flash('Telefone não pode conter letras, inserção não concluida', 'warning')
            return redirect(url_for('crud_pymongo.index'))
        if len(request.form['nome']) < 3:
            flash('Nome Fantasia não pode ter menos que 3 caracteres, inserção não concluida', 'warning')
            return redirect(url_for('crud_pymongo.index'))

        collection.insert_one({
            'CNPJ': cnpj,
            'NomeFantasia': nome,
            'CEP': cep,
            'Telefone': telefone,
            'Email': email
        })
        return redirect(url_for('crud_pymongo.index'))

    return render_template('add_crud_pymongo.html')


@crud_pymongo_blueprint.route('/edit/<string:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    estabelecimento = collection.find_one({'_id': ObjectId(id)})
    if request.method == 'POST':
        cnpj = request.form['cnpj']
        nome = request.form['nome']
        cep = request.form['cep']
        telefone = request.form['telefone']
        email = request.form['email']
        if not request.form['telefone'].isnumeric():
            flash('Telefone não pode conter letras, atualização não concluida', 'warning')
            return redirect(url_for('crud_pymongo.index'))
        if len(request.form['nome']) < 3:
            flash('Nome Fantasia não pode ter menos que 3 caracteres, atualização não concluida', 'warning')
            return redirect(url_for('crud_pymongo.index'))
        collection.update_one({'_id': ObjectId(id)}, {'$set': {
            'CNPJ': cnpj,
            'NomeFantasia': nome,
            'CEP': cep,
            'Telefone': telefone,
            'Email': email
        }})
        return redirect(url_for('crud_pymongo.index'))
    return render_template('edit_crud_pymongo.html', estabelecimento=estabelecimento)


@crud_pymongo_blueprint.route('/delete/<string:id>')
@login_required
def delete(id):
    result = collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 1:
        flash('Estabelecimento excluído com sucesso!', 'success')
    else:
        flash('Erro ao excluir estabelecimento.', 'danger')
    return redirect(url_for('crud_pymongo.index'))


if __name__ == '__main__':
    app.run(debug=True)
