from flask import Flask, jsonify, request

app = Flask(__name__)

# =================== CLASSE ALUNO ===================
class Aluno():
    alunos = []
    contador_id = 1

    def __init__(self, nome, idade, turma_id, data_nascimento, nota_semestre_1, nota_semestre_2):
        self.id = Aluno.contador_id
        self.nome = nome 
        self.idade = idade
        self.turma = turma_id
        self.data_nascimento = data_nascimento
        self.nota_1 = nota_semestre_1
        self.nota_2 = nota_semestre_2
        self.media_final = (nota_semestre_1 + nota_semestre_2) / 2
        Aluno.contador_id += 1
        Aluno.alunos.append(self)
    
    def dici(self):
        return {
            "id": self.id, 
            "nome": self.nome,
            "idade": self.idade, 
            "Turma": self.turma,
            "Data de nascimento": self.data_nascimento,
            "Nota do primeiro semestre": self.nota_1,
            "Nota do segundo semestre": self.nota_2,
            "Media final": self.media_final
        }

Aluno("João Silva", 20, "1A", "2004-05-10", 7.5, 8.0)
Aluno("Maria Souza", 22, "2B", "2002-09-15", 6.0, 9.5)
Aluno("Carlos Oliveira", 19, "1A", "2005-02-20", 8.5, 7.0)

@app.route("/alunos", methods=['GET'])
def Get_Alunos():
    return jsonify([aluno.dici() for aluno in Aluno.alunos])

@app.route('/alunos/<int:idAluno>', methods=['GET'])
def getAlunosPorID(idAluno):
    for aluno in Aluno.alunos:
        if aluno.id == idAluno:
            return jsonify(
                {
                    "id": aluno.id, 
                    "nome": aluno.nome,
                    "idade": aluno.idade, 
                    "Turma": aluno.turma,
                    "Data de nascimento": aluno.data_nascimento,
                    "Nota do primeiro semestre": aluno.nota_1,
                    "Nota do segundo semestre": aluno.nota_2,
                    "Media final": aluno.media_final
                }
            )
    return jsonify({'mensagem': 'Usuário não encontrado'}), 404

@app.route('/alunos', methods=['POST'])
def createAluno():
    dados = request.json
    novo_aluno = Aluno(
        nome=dados["nome"],
        idade=dados["idade"],
        turma_id=dados["Turma"],
        data_nascimento=dados["Data de nascimento"],
        nota_semestre_1=dados["Nota do primeiro semestre"],
        nota_semestre_2=dados["Nota do segundo semestre"]
    )
    return jsonify(novo_aluno.dici()), 201

@app.route('/alunos/<int:idAluno>', methods=['PUT'])
def updateAluno(idAluno):
    for aluno in Aluno.alunos:
        if aluno.id == idAluno:
            dados = request.json
            aluno.nome = dados.get('nome', aluno.nome)
            aluno.idade = dados.get('idade', aluno.idade)
            aluno.turma = dados.get('turma', aluno.turma)
            aluno.data_nascimento = dados.get('data_nascimento', aluno.data_nascimento)
            aluno.nota_1 = dados.get('nota_1', aluno.nota_1)
            aluno.nota_2 = dados.get('nota_2', aluno.nota_2)
            aluno.media_final = (aluno.nota_1 + aluno.nota_2) / 2
            return jsonify(aluno.dici())
        
    return jsonify({'mensagem': 'Usuário não encontrado'}), 404

@app.route('/alunos/<int:idAluno>', methods=['DELETE'])
def deleteAluno(idAluno):
    for aluno in Aluno.alunos:
        if aluno.id == idAluno:
            Aluno.alunos.remove(aluno)
            return jsonify({'mensagem': 'Usuário deletado'})
        
    return jsonify({'mensagem': 'Usuário não encontrado'}), 404

# =================== CLASSE PROFESSOR ===================
class Professor():
    professores = []
    contador_id = 1

    def __init__(self, nome, idade, materia, observacoes):
        self.id = Professor.contador_id
        self.nome = nome 
        self.idade = idade
        self.materia = materia 
        self.observacoes = observacoes
        Professor.contador_id += 1
        Professor.professores.append(self)
    
    def dici(self):
        return {
            "id": self.id, 
            "nome": self.nome,
            "idade": self.idade, 
            "Materia": self.materia,
            "Observações": self.observacoes,
        }

# Criando professores
prof1 = Professor('Tiago', 40, 'Matemática', 'Doutor em álgebra')
prof2 = Professor('Katherine', 35, 'Ciências', 'Especialista em biologia')
prof3 = Professor('Matheus', 29, 'Filosofia', 'Autor de livros sobre ética')

@app.route("/professores", methods=['GET'])
def Get_professores():
    return jsonify([professor.dici() for professor in Professor.professores])

# =================== CLASSE TURMA ===================
class Turma():
    turmas = []
    contador_id = 1

    def __init__(self, descricao, professor_id, ativo=True):
        self.id = Turma.contador_id
        self.descricao = descricao
        self.professor = self.get_professor_id(professor_id)  
        self.ativo = ativo  
        Turma.contador_id += 1
        Turma.turmas.append(self)
    
    def get_professor_id(self, professor_id):
        for professor in Professor.professores:
            if professor.id == professor_id:
                return professor.dici()  # Retorna o dicionário do professor
        return {"Professor não encontrado": "Erro"}        
    
    def dici(self):
        return {
            "id": self.id, 
            "Descrição": self.descricao,
            "Ativo": self.ativo, 
            "Professor": self.professor,  
        }


Turma("Turma 1A", 1)  
Turma("Turma 2B", 2)  
Turma("Turma 3C", 3)  

@app.route("/turmas", methods=['GET'])
def Get_turmas():
    return jsonify([turma.dici() for turma in Turma.turmas])

if __name__ == "__main__":
    app.run(debug=True)
