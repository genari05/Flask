from flask import Blueprint
from model.professor_model import *

Professor_Blueprint = Blueprint('professores', __name__, url_prefix='/professores')

@Professor_Blueprint.route("/", methods=['GET'])
def listar_professores():
    return Get_professores()

@Professor_Blueprint.route('/<int:idProfessor>', methods=['GET'])
def get_professor_por_id(idProfessor):
    return getProfessorPorID(idProfessor)

@Professor_Blueprint.route('/', methods=['POST'])
def criar_professor():
    return createProfessor()

@Professor_Blueprint.route('/<int:idProfessor>', methods=['PUT'])
def atualizar_professor(idProfessor):
    return updateProfessor(idProfessor)

@Professor_Blueprint.route('/<int:idProfessor>', methods=['DELETE'])
def deletar_professor(idProfessor):
    return deleteProfessor(idProfessor)

