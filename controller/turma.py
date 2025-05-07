from flask import Blueprint
from model.turma_model import *
from model.aluno_model import *
from model.professor_model import *

Turma_Blueprint = Blueprint('turmas', __name__,url_prefix='/turmas')

@Turma_Blueprint.route("/", methods=['GET'])
def listar_turmas():
    return Get_turmas()

@Turma_Blueprint.route('/<int:idTurma>', methods=['GET'])
def get_turma_por_id(idTurma):
    return getTurmaPorID(idTurma)

@Turma_Blueprint.route('/', methods=['POST'])
def criar_turma():
    return createTurma()

@Turma_Blueprint.route('/<int:idTurma>', methods=['PUT'])
def atualizar_turma(idTurma):
    return updateTurma(idTurma)

@Turma_Blueprint.route('/<int:idTurma>', methods=['DELETE'])
def deletar_turma(idTurma):
    return deleteTurma(idTurma)


@Turma_Blueprint.route('/reseta', methods=['POST'])
def resetar_dados():
    Aluno.alunos.clear()
    Professor.professores.clear()
    Turma.turmas.clear()
    return jsonify({'mensagem': 'Dados resetados com sucesso'}), 200

