from datetime import datetime
from flask import Flask, jsonify, request
import model.aluno_model as modelAluno
import model.professor_model as modelProfessor
import model.turma_model as modelTurma

app = Flask(__name__)

# =================== ROUTER ALUNO ===================

@app.route("/alunos", methods=["GET"])
def get_alunos():
    return modelAluno.Listar_aluno()

@app.route("/alunos/<int:idAluno>", methods=["GET"])
def get_aluno_por_id(idAluno):
    try:
        return modelAluno.getAlunosPorID(idAluno)
    except modelAluno.AlunoNaoEncontrado:
        return jsonify({"mensagem": "Aluno não encontrado"}), 404

@app.route("/alunos", methods=["POST"])
def create_aluno():
    dados = request.json
    resultado, status = modelAluno.createAluno(dados)
    return jsonify(resultado), status

@app.route("/alunos/<int:idAluno>", methods=["PUT"])
def update_aluno(idAluno):
    dados = request.json
    resultado, status = modelAluno.updateAluno(idAluno, dados)
    return jsonify(resultado), status

@app.route("/alunos/<int:idAluno>", methods=["DELETE"])
def delete_aluno(idAluno):
    resultado, status = modelAluno.deleteAluno(idAluno)
    return jsonify(resultado), status


# =================== ROUTER PROFESSOR ===================


@app.route("/professores", methods=['GET'])
def Get_professores():
    return modelProfessor.Get_professores()

@app.route('/professores/<int:idProfessor>', methods=['GET'])
def get_Professor_Por_ID(idProfessor):
    try:
        return modelProfessor.getProfessorPorID(idProfessor)
    except modelProfessor.ProfessorNaoEncontrado:
        return jsonify({'mensagem': 'Professor não encontrado'}), 404

@app.route('/professores', methods=['POST'])
def create_Professor():
    dados = request.json
    resultado,status = modelProfessor.createProfessor(dados)
    return jsonify(resultado),status
   
@app.route('/professores/<int:idProfessor>', methods=['PUT'])
def updateProfessor(idProfessor):
   dados = request.json
   resultado,status = modelProfessor.updateProfessor(idProfessor)
   return jsonify(resultado),status

@app.route('/professores/<int:idProfessor>', methods=['DELETE'])
def deleteProfessor(idProfessor):
    resultado, status = modelProfessor.deleteProfessor(idProfessor)
    return jsonify(resultado), status

# =================== ROUTER TURMA ===================

@app.route("/turmas", methods=['GET'])
def Get_turmas():
    return modelTurma.Get_turmas()

@app.route('/turmas/<int:idTurma>', methods=['GET'])
def getTurmaPorID(idTurma):
    try:
        return modelTurma.getTurmaPorID(idTurma)
    except modelTurma.TurmaNaoEncontrado:
        return jsonify({'mensagem': 'Turma não encontrada'}), 404

@app.route('/turmas', methods=['POST'])
def createTurma():
    dados = request.json
    resultado,status = modelTurma.createTurma(dados)
    return jsonify(resultado), status

@app.route('/turmas/<int:idTurma>', methods=['PUT'])
def updateTurma(idTurma):
    
    resultado,status = modelTurma.updateTurma(idTurma)
    return jsonify(resultado),status

@app.route('/turmas/<int:idTurma>', methods=['DELETE'])
def deleteTurma(idTurma):
    resultado,status = modelTurma.deleteTurma(idTurma)
    return jsonify(resultado),status

@app.route('/reseta', methods=['POST'])
def resetar_dados():
    modelAluno.alunos.clear()
    modelProfessor.professores.clear()
    modelTurma.turmas.clear()
    return jsonify({'mensagem': 'Dados resetados com sucesso'}), 200

if __name__ == "__main__":
    app.run(debug=True)
