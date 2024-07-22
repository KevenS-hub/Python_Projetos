from flask import Blueprint, render_template, request
from database.cliente import CLIENTES
from database.models.cliente import Cliente

cliente_route = Blueprint('cliente', __name__)

"""
Rota de clientes
    - /
    - /clientes/ (GET) - Listar os clientes
    - /clientes/ (POST) - Inserir o cliente no servidor
    - /clientes/new (GET) - Renderizar o formulario para criar um cliente
    - /clientes/<id> (GET) - obter os dados de um cliente
    - /clientes/<id>/edit (GET) - renderizar um formulario para editar um cliente
    - /clientes/<id>/update (PUT) - atualizar os dados do cliente
    - /clientes/<id>/delete (DELETE) - Deleta o registro do usuário
"""


@cliente_route.route('/')
def lista_clientes():
    """listar os clientes"""
    clientes = Cliente.select()
    print('lista_clientes.html', clientes)
    return render_template('lista_clientes.html', clientes=clientes)

@cliente_route.route('/', methods=['POST'])
def inserir_cliente():
    """inserir os dados do cliente"""
    
    data = request.json

    novo_usuario = Cliente.create(
        nome = data['nome'],
        email = data['email'],
    )

    return render_template('item_cliente.html', cliente=novo_usuario)

@cliente_route.route('/new')
def form_cliente():
    """formulario para cadastrar um cliente"""
    return render_template('formulario_cliente.html')

@cliente_route.route('/<int:cliente_id>')
def detalhe_cliente(cliente_id):
    """exibir detalhes do cliente"""

    cliente = Cliente.get_by_id(cliente_id)
    return render_template('detalhe_cliente.html', cliente=cliente)

@cliente_route.route('/<int:cliente_id>/edit')
def form_edit_cliente(cliente_id):
    """formulario para editar um cliente"""
    cliente = Cliente.get_by_id(cliente_id)

    return render_template('formulario_cliente.html', cliente=cliente)

@cliente_route.route('/<int:cliente_id>/update', methods=['PUT'])
def atualizar_cliente(cliente_id):
    """ atualizar informações do cliente """
    cliente_editado = None
    # obter dados do formulario de edição
    data = request.json

    cliente_editado = Cliente.get_by_id(cliente_id)

    # editar usuario
    return render_template('item_cliente.html', cliente=cliente_editado)
    

#Esses últimos 2 não vão nada pois não renderizam nada, apenas realizam ações

@cliente_route.route('/<int:cliente_id>/delete', methods=['DELETE'])
def deletar_cliente(cliente_id):
    global CLIENTES
    CLIENTES = [ c for c in CLIENTES if c['id'] != cliente_id]

    return {'delete': 'ok'}
    
