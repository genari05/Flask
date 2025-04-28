from flask_restx import Namespace, Resource, fields
from model.professor_model import Get_professores,getProfessorPorID,createProfessor,deleteProfessor,updateProfessor


professor_ns = Namespace("Professor ", description="Operações relacionadas aos professores")

professor_model = professor_ns.model("Professor", {
    "Nome": fields.String(required=True, description="Nome do professor"),
    "Idade": fields.Integer(required=True, description="Idade"),
    "Materia": fields.String(required=True, description="Descrição do professor"),
    "Observação": fields.String(required=True, description="Nota do segundo semestre"),
})


professor_model_output = professor_ns.model("ProfessorOutput", {
    "id": fields.Integer(description="ID do professor"),
    "Nome": fields.String(required=True, description="Nome do professor"),
    "Idade": fields.Integer(required=True, description="Idade"),
    "Materia": fields.String(required=True, description="Descrição do professor"),
    "Observação": fields.String(required=True, description="Nota do segundo semestre"),
})


@professor_ns.route('/')
class ProfssorResource(Resource):
    @professor_ns.marshal_list_with(professor_model_output)
    def get(self):
        '''Listar todos os professores'''
        return Get_professores()
    
    @professor_ns.expect(professor_model)
    def post(self):
        '''Criar um novo professor'''
        data = professor_ns.payload
        response,status_code = createProfessor(data)
        return response,status_code
    

@professor_ns.route('/<int:id_professores>')
class ProfessorIdResource(Resource):
    @professor_ns.marshal_list_with(professor_model_output)
    def get(self,id_profeessor):
        '''Obtém um professor pelo ID'''
        return getProfessorPorID(id_profeessor)
    
    @professor_ns.expect(professor_model)
    def put(self,Id_professor):
        data = professor_ns.payload
        updateProfessor(Id_professor,data)
        return data, 200
    
    def delete(self,Id_professor):
        '''Excluir professor por id'''
        deleteProfessor(Id_professor)
        return{'messagem':'Professor excluido com sucesso'}, 200    
    