from datetime import datetime
from flask import Flask, jsonify, request
from config import db
from model.turma_model import Turma

class Aluno(db.Model):
    __tablename__ = "Aluno"

    id = db.Column(db.Integer, primary_key=True)
    id_turma = db.Column(db.Integer, db.ForeignKey("Turma.id"), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    nota_semestre_1 = db.Column(db.Float, nullable=False)
    nota_semestre_2 = db.Column(db.Float, nullable=False)
    media_final = db.Column(db.Float, nullable=False)

    turma = db.relationship("Turma", back_populates="alunos")

    def __init__(self, id, nome, id_turma, data_nascimento, nota_semestre_1, nota_semestre_2):
        if not isinstance(nome, str) or len(nome) > 100:
            raise ValueError("Nome inválido. Deve ser uma string de até 100 caracteres")
        if not isinstance(nota_semestre_1, (int, float)) or not isinstance(nota_semestre_2, (int, float)):
            raise ValueError("Notas inválidas. Devem ser números float")
        
        self.id = id
        self.nome = nome
        self.id_turma = id_turma
        if isinstance(data_nascimento, str):
            self.data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d").date()
        else:
            self.data_nascimento = data_nascimento
        self.nota_semestre_1 = nota_semestre_1
        self.nota_semestre_2 = nota_semestre_2
        self.media_final = (nota_semestre_1 + nota_semestre_2) / 2
    
    def CalcularIdade(self, dataNascimento):
        hoje = datetime.now()
        idade = hoje.year - dataNascimento.year - ((hoje.month, hoje.day) < (dataNascimento.month, dataNascimento.day))
        return idade

    def dici(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "idade": self.CalcularIdade(self.data_nascimento),
            "Turma": self.id_turma,
            "Data de nascimento": self.data_nascimento,
            "Nota do primeiro semestre": self.nota_semestre_1,
            "Nota do segundo semestre": self.nota_semestre_2,
            "Media final": self.media_final
        }

def Listar_aluno():
    alunos = Aluno.query.all()
    return jsonify([aluno.dici() for aluno in alunos])

def getAlunosPorID(idAluno):
    aluno = Aluno.query.get(idAluno)
    if aluno:
        return jsonify(aluno.dici())
    return jsonify({'mensagem': 'Aluno não encontrado'}), 404

def createAluno():
    dados = request.json

    id = dados.get("id", "")
    if not id:
        return jsonify({'mensagem': 'O aluno necessita de um id'}), 400
    if not isinstance(id, int) or id <= 0:
        return jsonify({'mensagem': 'ID inválido. Deve ser um número inteiro positivo'}), 400
    if Aluno.query.get(id):
            return jsonify({'mensagem': 'ID já utilizado'}), 400

    nome = dados.get("nome", "")
    if not nome:
        return jsonify({'mensagem': 'O aluno necessita de um nome'}), 400
    
    turma = Turma.query.get(dados['Turma'])
    if(turma is None):
            return {"message": "Turma não existe"}, 400
    
    data_nascimento = dados.get("Data de nascimento", "")
    if data_nascimento:
        if isinstance(data_nascimento, str):
            data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d").date()
    elif not data_nascimento:
        return jsonify({'mensagem': 'O aluno necessita ter data de nascimento'}), 400
    
    nota_semestre_1 = dados.get("Nota do primeiro semestre", 0)
    nota_semestre_2 = dados.get("Nota do segundo semestre", 0)
    if not isinstance(nota_semestre_1, (int, float)) or not isinstance(nota_semestre_2, (int, float)):
        return jsonify({'mensagem': 'Notas inválidas, passe números'}), 400

    try:
        novo_aluno = Aluno(
            id = id,
            nome = nome,
            id_turma = turma.id,
            data_nascimento = data_nascimento,
            nota_semestre_1 = nota_semestre_1,
            nota_semestre_2 = nota_semestre_2
        )
    except ValueError as e:
        return jsonify({'mensagem': str(e)}), 400
    
    db.session.add(novo_aluno)
    db.session.commit()
    return jsonify(novo_aluno.dici()), 201


def updateAluno(idAluno):
    try:
        aluno = Aluno.query.get(idAluno)
        if not aluno:
            return jsonify({'mensagem': 'Aluno não encontrado'}), 404

        dados = request.json

        nome = dados.get("nome")
        if not nome or not nome.strip():
            return jsonify({'mensagem': 'O aluno necessita de um nome'}), 400
        aluno.nome = nome.strip()

        data_nascimento = dados.get("Data de nascimento", "").strip()
        if not data_nascimento:
            return jsonify({'mensagem': 'A data de nascimento é obrigatória'}), 400
        
        try:
            aluno.data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d").date()
        except ValueError as e:
            return jsonify({'mensagem': f'Formato de data inválido. Use YYYY-MM-DD: {str(e)}'}), 400

        turma_id = dados.get("Turma")
        if turma_id:
            turma = Turma.query.get(turma_id)
            if not turma:
                return jsonify({'mensagem': 'Turma não encontrada'}), 400
            aluno.id_turma = turma_id

        try:
            nota_semestre_1 = float(dados.get('Nota do primeiro semestre', aluno.nota_semestre_1))
            nota_semestre_2 = float(dados.get('Nota do segundo semestre', aluno.nota_semestre_2))

            if not (0 <= nota_semestre_1 <= 10) or not (0 <= nota_semestre_2 <= 10):
                return jsonify({'mensagem': 'As notas devem estar entre 0 e 10'}), 400

            aluno.nota_semestre_1 = nota_semestre_1
            aluno.nota_semestre_2 = nota_semestre_2
            aluno.media_final = (nota_semestre_1 + nota_semestre_2) / 2
        except ValueError:
            return jsonify({'mensagem': 'Notas inválidas. Devem ser números'}), 400

        db.session.commit()
        return jsonify(aluno.dici())

    except Exception as e:
        db.session.rollback()
        return jsonify({'mensagem': f'Erro inesperado: {str(e)}'}), 500

def deleteAluno(idAluno):
    aluno = Aluno.query.get(idAluno)
    if aluno:
        db.session.delete(aluno)
        db.session.commit()
        return jsonify({'mensagem': 'Aluno deletado'})
        
    return jsonify({'mensagem': 'Aluno não encontrado'}), 404
