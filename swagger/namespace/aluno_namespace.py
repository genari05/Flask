from flask_restx import Namespace, Resource, fields
from model.aluno_model import Listar_aluno, createAluno, updateAluno, deleteAluno, getAlunosPorID

alunos_ns = Namespace("Aluno", description="Operações relacionadas aos alunos")

aluno_model = alunos_ns.model("Aluno", {
    "nome": fields.String(required=True, description="Nome do aluno", example = 'Tiago Genari'),
    "Data de nascimento": fields.String(required=True, description="Data de nascimento (YYYY-MM-DD)",example = '2005-05-28'),
    "Nota do primeiro semestre": fields.Float(required=True, description="Nota do primeiro semestre",example = 7.8),
    "Nota do segundo semestre": fields.Float(required=True, description="Nota do segundo semestre",example = 9.0),
    "Turma": fields.Integer(required=True, description="ID da turma associada",example = 1),
})

aluno_output_model = alunos_ns.model("AlunoOutput", {
    "id": fields.Integer(description="ID do aluno",example = 1),
    "nome": fields.String(required=True, description="Nome do aluno",example = 'Tiago Genari'),
    "idade": fields.Integer(required=True, description="Idade do aluno", example = 20),
    "Data de nascimento": fields.String(required=True, description="Data de nascimento (YYYY-MM-DD)",example = '2005-05-28'),
    "Nota do primeiro semestre": fields.Float(required=True, description="Nota do primeiro semestre",example = 7.8),
    "Nota do segundo semestre": fields.Float(required=True, description="Nota do segundo semestre",example = 9.0),
    "Media final": fields.Float(required=True, description="Média final do aluno",exemple = 8.4),
    "Turma": fields.Integer(required=True, description="ID da turma associada", exemple= 1),
})

erro_model = alunos_ns.model("Erro", {
    "mensagem": fields.String(example="Aluno não encontrado")
})

@alunos_ns.route("/")
class AlunosResource(Resource):
    @alunos_ns.marshal_list_with(aluno_output_model)
    def get(self):
        """Lista todos os alunos"""
        return Listar_aluno()

    @alunos_ns.expect(aluno_model)
    @alunos_ns.response(201, "Aluno criado com sucesso", aluno_output_model)
    @alunos_ns.response(400, "Dados inválidos", model=erro_model)
    def post(self):
        """Cria um novo aluno"""
        dados = alunos_ns.payload
        resultado, status_code = createAluno(dados)
        return resultado, status_code

@alunos_ns.route("/<int:id_aluno>")
class AlunoIdResource(Resource):
    @alunos_ns.response(200, "Aluno encontrado", aluno_output_model)
    @alunos_ns.response(404, "Aluno não encontrado", erro_model)
    def get(self, id_aluno):
        """Obtém um aluno pelo ID"""
        resultado, status_code = getAlunosPorID(id_aluno)
        return resultado, status_code

    @alunos_ns.expect(aluno_model)
    @alunos_ns.response(400, "Dados inválidos", model=erro_model)
    @alunos_ns.response(404, "Aluno não encontrado", model=erro_model)
    def put(self, id_aluno):
        """Atualiza um aluno pelo ID"""
        dados = alunos_ns.payload
        resposta, status_code = updateAluno(id_aluno, dados)
        return resposta, status_code

    @alunos_ns.response(404, "Aluno não encontrado", model=erro_model)
    def delete(self, id_aluno):
        """Exclui um aluno pelo ID"""
        resultado, status_code = deleteAluno(id_aluno)
        return resultado, status_code
