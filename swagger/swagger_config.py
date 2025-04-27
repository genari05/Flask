from . import api
from swagger.namespace.aluno_namespace import alunos_ns  # Seu namespace de alunos
# Adicione outros namespaces se necessário

def configure_swagger(app):
    api.init_app(app)
    
    # Registra o namespace do aluno e qualquer outro
    api.add_namespace(alunos_ns, path="/alunos")
    # Adicione outros namespaces aqui, como professores ou turmas
    
    api.mask_swagger = False  # Desativa o X-Fields, se necessário
