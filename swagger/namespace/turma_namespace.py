from flask_restx import Namespace, Resource, fields
from model.turma_model import Get_turmas, getTurmaPorID, createTurma, updateTurma, deleteTurma

turma_ns = Namespace("Turma", description="Operações relacionadas às turmas")

turma_model = turma_ns.model("Turma", {
    "Descrição": fields.String(required=True, description="Descrição da Turma"),
    "Ativo": fields.Boolean(required=True, description="Indica se a turma está ativa"),
    "Professor": fields.Nested(turma_ns.model("ProfessorRef", {
        "id": fields.Integer(required=True, description="ID do professor responsável")
    }))
})

turma_model_output = turma_ns.model("TurmaOutput", {
    "id": fields.Integer(description="ID do professor"),
    "Descrição": fields.String(required=True, description="Descrição da Turma"),
    "Ativo": fields.Boolean(required=True, description="Indica se a turma está ativa"),
    "Professor": fields.Nested(turma_ns.model("ProfessorInfo", {
        "nome": fields.String(description="Nome do professor")
    }), allow_null=True)
})

@turma_ns.route('/')
class TurmaResource(Resource):
    @turma_ns.marshal_list_with(turma_model_output)
    def get(self):
        '''Listar todas as turmas'''
        return Get_turmas()
    
    @turma_ns.expect(turma_model)
    @turma_ns.marshal_with(turma_model_output, code=201)
    def post(self):
        '''Criar uma nova turma'''
        return createTurma()

@turma_ns.route('/<int:id_turma>')
class TurmaIdResource(Resource):
    @turma_ns.marshal_with(turma_model_output)
    def get(self, id_turma):
        '''Obter uma turma pelo ID'''
        return getTurmaPorID(id_turma)
    
    @turma_ns.expect(turma_model)
    @turma_ns.marshal_with(turma_model_output)
    def put(self, id_turma):
        '''Atualizar uma turma pelo ID'''
        updateTurma(id_turma)
        return {"message": "Turma atualizada com sucesso"}, 200
    
    def delete(self, id_turma):
        '''Excluir uma turma pelo ID'''
        deleteTurma(id_turma)
        return {'message': 'Turma excluída com sucesso'}, 200