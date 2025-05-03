from flask_restx import Namespace, Resource, fields
from model.professor_model import Get_professores,getProfessorPorID,createProfessor,deleteProfessor,updateProfessor

professor_ns = Namespace("Professor ", description="Operações relacionadas aos professores")

professor_model = professor_ns.model("Professor", {
    "nome": fields.String(required=True, description="Nome do professor"),
    "idade": fields.Integer(required=True, description="Idade"),
    "Materia": fields.String(required=True, description="Descrição do professor"),
    "Observações": fields.String(required=True, description="Nota do segundo semestre"),
})

professor_model_output = professor_ns.model("ProfessorOutput", {
    "id": fields.Integer(description="ID do professor"),
    "nome": fields.String(required=True, description="Nome do professor"),
    "idade": fields.Integer(required=True, description="Idade"),
    "Materia": fields.String(required=True, description="Descrição do professor"),
    "Observações": fields.String(required=True, description="Nota do segundo semestre"),
})

erro_model = professor_ns.model("Erro", {
    "mensagem": fields.String(example="Professor não encontrado")
})

@professor_ns.route('/')
class ProfessorResource(Resource):
    @professor_ns.marshal_list_with(professor_model_output)
    def get(self):
        '''Listar todos os professores'''
        return Get_professores()
    
    @professor_ns.expect(professor_model)
    @professor_ns.response(201, "Professor criado com sucesso", professor_model_output)
    @professor_ns.response(400, "Dados inválidos", model=erro_model)
    def post(self):
        '''Criar um novo professor'''
        dados = professor_ns.payload
        resultado, status_code = createProfessor(dados)
        return resultado, status_code

@professor_ns.route('/<int:id_professores>')
class ProfessorIdResource(Resource):
    @professor_ns.response(200, "Professor encontrado", professor_model_output)
    @professor_ns.response(404, "Professor não encontrado", model=erro_model)
    def get(self, id_professores):
        '''Obtém um professor pelo ID'''
        resultado, status_code = getProfessorPorID(id_professores)
        return resultado, status_code
    
    @professor_ns.expect(professor_model)
    @professor_ns.response(400, "Dados inválidos", model=erro_model)
    @professor_ns.response(404, "Professor não encontrado", model=erro_model)
    def put(self, id_professores):
        dados = professor_ns.payload
        resultado, status_code = updateProfessor(id_professores, dados)
        return resultado, status_code
    
    @professor_ns.response(404, "Professor não encontrado", model=erro_model)
    def delete(self, id_professores):
        '''Excluir professor por id'''
        resultado, status_code = deleteProfessor(id_professores)
        return resultado, status_code
