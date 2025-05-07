from . import api
from swagger.namespace.aluno_namespace import alunos_ns
from swagger.namespace.professor_namespace import professor_ns
from swagger.namespace.turma_namespace import turma_ns


def configure_swagger(app):
    api.init_app(app)
    
    # Registra o namespace do aluno e qualquer outro
    api.add_namespace(alunos_ns, path="/alunos")
    api.add_namespace(professor_ns, path="/professores")
    api.add_namespace(turma_ns, path="/turmas")
    # Adicione outros namespaces aqui, como professores ou turmas
    
    api.mask_swagger = False  # Desativa o X-Fields, se necessário
