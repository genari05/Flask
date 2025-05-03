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

erro_model = turma_ns.model("Erro", {
    "mensagem": fields.String(example="Turma não encontrada")
})

@turma_ns.route('/')
class TurmaResource(Resource):
    @turma_ns.marshal_list_with(turma_model_output)
    def get(self):
        '''Listar todas as turmas'''
        return Get_turmas()
    
    @turma_ns.expect(turma_model)
    @turma_ns.response(201, "Turma criada com sucesso", model=turma_model_output)
    @turma_ns.response(400, "Dados inválidos", model=erro_model)
    def post(self):
        '''Criar uma nova turma'''
        dados = turma_ns.payload
        resultado, status_code = createTurma(dados)
        return resultado, status_code

@turma_ns.route('/<int:id_turma>')
class TurmaIdResource(Resource):
    @turma_ns.response(200, "Turma encontrado", turma_model_output)
    @turma_ns.response(404, "Turma não encontrada", model=erro_model)
    def get(self, id_turma):
        '''Obter uma turma pelo ID'''
        resultado, status_code = getTurmaPorID(id_turma)
        return resultado, status_code
    
    @turma_ns.expect(turma_model)
    @turma_ns.response(400, "Dados inválidos", erro_model)
    @turma_ns.response(404, "Turma não encontrada", model=erro_model)
    def put(self, id_turma):
        '''Atualizar uma turma pelo ID'''
        dados = turma_ns.payload
        resultado, status_code = updateTurma(id_turma, dados)
        return resultado, status_code
    
    @turma_ns.response(404, "Turma não encontrada", model=erro_model)
    def delete(self, id_turma):
        '''Excluir uma turma pelo ID'''
        resultado, status_code = deleteTurma(id_turma)
        return resultado, status_code