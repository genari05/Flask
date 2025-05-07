from config import app, db
from flask import Flask, Blueprint
from swagger.swagger_config import configure_swagger
from model.aluno_model import Aluno
from model.professor_model import Professor
from model.turma_model import Turma
from controller.aluno import Alunos_Blueprint
from controller.professor import Professor_Blueprint
from controller.reseta import Reseta_Blueprint
from controller.turma import Turma_Blueprint

# =================== CONFIGURAÇÃO DO SWAGGER ========
configure_swagger(app)
# =================== ROUTES ALUNO ===================
app.register_blueprint(Alunos_Blueprint)
# =================== ROUTES PROFESSOR ===============
app.register_blueprint(Professor_Blueprint)
# =================== ROUTES TURMA ===================
app.register_blueprint(Turma_Blueprint)
# =================== ROUTES RESETA ==================
app.register_blueprint(Reseta_Blueprint)
# =================== CRIAR TABELAS ===================
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
