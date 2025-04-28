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

@professor_ns.route('/')
class ProfessorResource(Resource):
    @professor_ns.marshal_list_with(professor_model_output)
    def get(self):
        '''Listar todos os professores'''
        return Get_professores()
    
    @professor_ns.expect(professor_model)
    @professor_ns.marshal_with(professor_model_output, code=201)
    def post(self):
        '''Criar um novo professor'''
        return createProfessor()

@professor_ns.route('/<int:id_professores>')
class ProfessorIdResource(Resource):
    @professor_ns.marshal_with(professor_model_output)
    def get(self, id_professores):
        '''Obtém um professor pelo ID'''
        return getProfessorPorID(id_professores)
    
    @professor_ns.expect(professor_model)
    def put(self, id_professores):
        data = professor_ns.payload
        updateProfessor(id_professores, data)
        return {"message": "Professor atualizado com sucesso"}, 200
    
    def delete(self, id_professores):
        '''Excluir professor por id'''
        deleteProfessor(id_professores)
        return {'message': 'Professor excluído com sucesso'}, 200
