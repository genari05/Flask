from flask import Blueprint, jsonify
from model.aluno_model import *

Alunos_Blueprint = Blueprint('alunos', __name__,url_prefix='/alunos')

@Alunos_Blueprint.route("/", methods=['GET'])
def listar_alunos():
    aluno = Listar_aluno()
    return jsonify(aluno)

@Alunos_Blueprint.route('/<int:idAluno>', methods=['GET'])
def get_aluno_por_id(idAluno):
    get_aluno = getAlunosPorID(idAluno)
    return jsonify(get_aluno)

@Alunos_Blueprint.route('/', methods=['POST'])
def criar_aluno():
    create_aluno = createAluno()
    return jsonify(create_aluno)

@Alunos_Blueprint.route('/<int:idAluno>', methods=['PUT'])
def atualizar_aluno(idAluno):
    update_aluno= updateAluno(idAluno)
    return jsonify(update_aluno)

@Alunos_Blueprint.route('/<int:idAluno>', methods=['DELETE'])
def deletar_aluno(idAluno):
    delete_aluno=deleteAluno(idAluno)
    return jsonify(delete_aluno)