from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/professor', methods=['GET'])
def getProfessor():
    dados = {
        "professor":[
            {"id":1, "nome":"Matheus", "idade":44, "materia":"api", "observacoes":""},
            {"id":2, "nome":"Tiago", "idade":29, "materia":"bd", "observacoes":""},
        ],
    }
    return jsonify(dados["professor"])

@app.route('/turma', methods=['GET'])
def getTurma():
    dados = {
        "turma":[
            {"id":1, "descricao":"api", "professor_id":1, "ativo":True},
            {"id":2, "descricao":"bd", "professor_id":2, "ativo":True},
            {"id":3, "descricao":"dev", "professor_id":0, "ativo":False},
        ]
    }
    return jsonify(dados["turma"])

@app.route('/aluno', methods=['GET'])
def getAluno():
    dados = {
        "aluno":[
            {"id":88, "nome":"João", "idade":18, "turma_id":2, "data_nascimento":"28/03/2008", "nota_primeiro_semestre":7.7, "nota_segundo_semestre":6.4, "media_final":7.05}
        ]
    }
    return jsonify(dados["aluno"])

if __name__ == '__main__':
    app.run(debug=True)