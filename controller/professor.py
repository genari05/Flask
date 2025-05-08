from flask import Blueprint,jsonify
from model.professor_model import *

Professor_Blueprint = Blueprint('professores', __name__, url_prefix='/professores')

@Professor_Blueprint.route("/", methods=['GET'])
def listar_professores():
    get_pf=Get_professores()
    return jsonify(get_pf) 
@Professor_Blueprint.route('/<int:idProfessor>', methods=['GET'])
def get_professor_por_id(idProfessor):
    get_pf_id=getProfessorPorID(idProfessor)
    return jsonify(get_pf_id) 
 
@Professor_Blueprint.route('/', methods=['POST'])
def criar_professor():
    create_pf=createProfessor()
    return jsonify(create_pf) 

@Professor_Blueprint.route('/<int:idProfessor>', methods=['PUT'])
def atualizar_professor(idProfessor):
    update_pf=updateProfessor(idProfessor)
    return jsonify(update_pf) 

@Professor_Blueprint.route('/<int:idProfessor>', methods=['DELETE'])
def deletar_professor(idProfessor):
    delete_pf=deleteProfessor(idProfessor)
    return jsonify(delete_pf) 

