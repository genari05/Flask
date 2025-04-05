from config import app
from flask import Flask,Blueprint
from controller.aluno import Alunos_Blueprint
from controller.professor import Professor_Blueprint
from controller.turma import Turma_Blueprint


# =================== ROUTES ALUNO ===================
app.register_blueprint(Alunos_Blueprint)
# =================== ROUTES PROFESSOR ===================
app.register_blueprint(Professor_Blueprint)
# =================== ROUTES TURMA ===================
app.register_blueprint(Turma_Blueprint)

if __name__ == '__main__':
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )