from flask import Blueprint,jsonify
from model.turma_model import *
from model.aluno_model import *
from model.professor_model import *

Turma_Blueprint = Blueprint('turmas', __name__,url_prefix='/turmas')

@Turma_Blueprint.route("/", methods=['GET'])
def listar_turmas():
    get_turma = Get_turmas()
    return jsonify(get_turma
                   )
@Turma_Blueprint.route('/<int:idTurma>', methods=['GET'])
def get_turma_por_id(idTurma):
    get_turma_id = getTurmaPorID(idTurma)
    return jsonify(get_turma_id)

@Turma_Blueprint.route('/', methods=['POST'])
def criar_turma():
    create_turma= createTurma()
    return jsonify(create_turma)

@Turma_Blueprint.route('/<int:idTurma>', methods=['PUT'])
def atualizar_turma(idTurma):
    update_turma= updateTurma(idTurma)
    return jsonify(update_turma)

@Turma_Blueprint.route('/<int:idTurma>', methods=['DELETE'])
def deletar_turma(idTurma):
    delete_turma= deleteTurma(idTurma)
    return jsonify(delete_turma)

@Turma_Blueprint.route('/reseta', methods=['POST'])
def resetar_dados():
    Aluno.alunos.clear()
    Professor.professores.clear()
    Turma.turmas.clear()
    return jsonify({'mensagem': 'Dados resetados com sucesso'}), 200

