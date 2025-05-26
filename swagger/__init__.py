from flask_restx import Api

# Inicializa o objeto API do Swagger
api = Api(
    version="1.0",
    title="API de Gestão Escolar",
    description="Documentação da API para Alunos, Professores e Turmas",
    doc="/",       # Essa URL será onde a documentação do Swagger estará disponível
    mask_swagger=False,
    # Prefixa todas as rotas com /api
)
