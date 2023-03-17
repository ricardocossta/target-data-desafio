import time
from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_required
from elasticsearch import Elasticsearch

crud_elasticsearch_blueprint = Blueprint('crud_elasticsearch', __name__, template_folder='templates',
                                         url_prefix='/crud_elasticsearch')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

es = Elasticsearch(['http://localhost:9200/'])


@crud_elasticsearch_blueprint.route('/')
@login_required
def index():
    res = es.search(index='estabelecimentos', body={'query': {'match_all': {}}, 'size': 100})
    estabelecimentos = list(res['hits']['hits'])
    return render_template('index_crud_elasticsearch.html', estabelecimentos=estabelecimentos)


@crud_elasticsearch_blueprint.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        data = {
            'CNPJ': request.form['cnpj'],
            'NomeFantasia': request.form['nome'],
            'CEP': request.form['cep'],
            'Telefone': request.form['telefone'],
            'Email': request.form['email']
        }
        if not request.form['telefone'].isnumeric():
            flash('Telefone não pode conter letras, inserção não concluida', 'warning')
            return redirect(url_for('crud_elasticsearch.index'))
        if len(request.form['nome']) < 3:
            flash('Nome Fantasia não pode ter menos que 3 caracteres, inserção não concluida', 'warning')
            return redirect(url_for('crud_elasticsearch.index'))
        res = es.search(index='estabelecimentos', body={'query': {'match_all': {}}, 'size': 100})
        estabelecimentos = res['hits']['hits']
        ultimo_estabelecimento = estabelecimentos[-1]

        es.index(index='estabelecimentos', document=data, id=int(ultimo_estabelecimento["_id"]) + 1)
        time.sleep(1)

        return redirect(url_for('crud_elasticsearch.index'))

    return render_template('add_crud_elasticsearch.html')


@crud_elasticsearch_blueprint.route('/edit/<string:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    estabelecimento = es.get(index='estabelecimentos', id=id)
    if request.method == 'POST':
        data = {
            'CNPJ': request.form['cnpj'],
            'NomeFantasia': request.form['nome'],
            'CEP': request.form['cep'],
            'Telefone': request.form['telefone'],
            'Email': request.form['email']
        }
        if not request.form['telefone'].isnumeric():
            flash('Telefone não pode conter letras, atualização não concluida', 'warning')
            return redirect(url_for('crud_elasticsearch.index'))
        if len(request.form['nome']) < 3:
            flash('Nome Fantasia não pode ter menos que 3 caracteres, atualização não concluida', 'warning')
            return redirect(url_for('crud_elasticsearch.index'))
        es.index(index='estabelecimentos', document=data, id=estabelecimento["_id"])
        time.sleep(1)
        return redirect(url_for('crud_elasticsearch.index'))
    return render_template('edit_crud_elasticsearch.html', estabelecimento=estabelecimento)


@crud_elasticsearch_blueprint.route('/delete/<string:id>')
@login_required
def delete(id):
    result = es.delete(index='estabelecimentos', id=id)
    time.sleep(1)
    if result['result'] == 'deleted':
        flash('Estabelecimento excluído com sucesso!', 'success')
    else:
        flash('Erro ao excluir estabelecimento.', 'danger')
    return redirect(url_for('crud_elasticsearch.index'))


if __name__ == '__main__':
    app.run(debug=True)
