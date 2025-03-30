from flask import Flask
from model.aluno_model import *
from model.professor_model import *
from model.turma_model import *



app = Flask(__name__)

# =================== ROUTES ALUNO ===================
@app.route("/alunos", methods=['GET'])
def listar_alunos():
    return Listar_aluno()

@app.route('/alunos/<int:idAluno>', methods=['GET'])
def get_aluno_por_id(idAluno):
    return getAlunosPorID(idAluno)

@app.route('/alunos', methods=['POST'])
def criar_aluno():
    return createAluno()

@app.route('/alunos/<int:idAluno>', methods=['PUT'])
def atualizar_aluno(idAluno):
    return updateAluno(idAluno)

@app.route('/alunos/<int:idAluno>', methods=['DELETE'])
def deletar_aluno(idAluno):
    return deleteAluno(idAluno)

# =================== ROUTES PROFESSOR ===================
@app.route("/professores", methods=['GET'])
def listar_professores():
    return Get_professores()

@app.route('/professores/<int:idProfessor>', methods=['GET'])
def get_professor_por_id(idProfessor):
    return getProfessorPorID(idProfessor)

@app.route('/professores', methods=['POST'])
def criar_professor():
    return createProfessor()

@app.route('/professores/<int:idProfessor>', methods=['PUT'])
def atualizar_professor(idProfessor):
    return updateProfessor(idProfessor)

@app.route('/professores/<int:idProfessor>', methods=['DELETE'])
def deletar_professor(idProfessor):
    return deleteProfessor(idProfessor)

# =================== ROUTES TURMA ===================
@app.route("/turmas", methods=['GET'])
def listar_turmas():
    return Get_turmas()

@app.route('/turmas/<int:idTurma>', methods=['GET'])
def get_turma_por_id(idTurma):
    return getTurmaPorID(idTurma)

@app.route('/turmas', methods=['POST'])
def criar_turma():
    return createTurma()

@app.route('/turmas/<int:idTurma>', methods=['PUT'])
def atualizar_turma(idTurma):
    return updateTurma(idTurma)

@app.route('/turmas/<int:idTurma>', methods=['DELETE'])
def deletar_turma(idTurma):
    return deleteTurma(idTurma)


@app.route('/reseta', methods=['POST'])
def resetar_dados():
    Aluno.alunos.clear()
    Professor.professores.clear()
    Turma.turmas.clear()
    return jsonify({'mensagem': 'Dados resetados com sucesso'}), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
