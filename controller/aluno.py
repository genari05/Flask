from flask import Blueprint
from model.aluno_model import *

Alunos_Blueprint = Blueprint('alunos', __name__,url_prefix='/alunos')

@Alunos_Blueprint.route("/", methods=['GET'])
def listar_alunos():
    return Listar_aluno()

@Alunos_Blueprint.route('/<int:idAluno>', methods=['GET'])
def get_aluno_por_id(idAluno):
    return getAlunosPorID(idAluno)

@Alunos_Blueprint.route('/', methods=['POST'])
def criar_aluno():
    return createAluno()

@Alunos_Blueprint.route('/<int:idAluno>', methods=['PUT'])
def atualizar_aluno(idAluno):
    return updateAluno(idAluno)

@Alunos_Blueprint.route('/<int:idAluno>', methods=['DELETE'])
def deletar_aluno(idAluno):
    return deleteAluno(idAluno)
