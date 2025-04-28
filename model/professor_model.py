from flask import Flask, jsonify, request
from config import db

class Professor(db.Model):
    __tablename__ = "Professor"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    idade = db.Column(db.Integer)
    materia = db.Column(db.String(40))
    observacoes = db.Column(db.String(50))

    turmas = db.relationship("Turma", back_populates="professor")

    def __init__(self, id, nome, idade, materia, observacoes):
        self.id = id
        self.nome = nome
        self.idade = idade
        self.materia = materia
        self.observacoes = observacoes
    
    def dici(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "idade": self.idade,
            "Materia": self.materia,
            "Observações": self.observacoes,
        }

def Get_professores():
    professores = Professor.query.all()
    return [professor.dici() for professor in professores]  # <<< sem jsonify

def getProfessorPorID(idProfessor):
    professor = Professor.query.get(idProfessor)
    if professor:
        return professor.dici()  # <<< sem jsonify
    return {'mensagem': 'Professor não encontrado'}, 404

def createProfessor():
    dados = request.json

    id = dados.get("id", "")
    if not id:
        return {'mensagem': 'O professor necessita de um id'}, 400
    if not isinstance(id, int) or id <= 0:
        return {'mensagem': 'ID inválido. Deve ser um número inteiro positivo'}, 400
    if Professor.query.get(id):
        return {'mensagem': 'ID já utilizado'}, 400

    nome = dados.get("nome", "")
    if not nome:
        return {'mensagem': 'O professor necessita de um nome'}, 400
    
    materia = dados.get("Materia", "")
    if not materia:
        return {'mensagem': 'O professor necessita de uma matéria'}, 400

    novo_professor = Professor(
        id=id,
        nome=nome,
        idade=dados.get("idade", ""),
        materia=materia,
        observacoes=dados.get("Observações", "")
    )
    db.session.add(novo_professor)
    db.session.commit()
    return novo_professor.dici(), 201  # <<< sem jsonify

def updateProfessor(idProfessor, data):
    professor = Professor.query.get(idProfessor)
    if professor:
        nome = data.get('nome', "").strip()
        if not nome:
            return {'erro': 'O professor necessita de um nome'}, 400

        materia = data.get("Materia", "").strip()
        if not materia:
            return {'mensagem': 'O professor necessita de uma matéria'}, 400

        professor.nome = nome
        professor.idade = data.get("idade", "")
        professor.materia = materia
        professor.observacoes = data.get("Observações", "")

        db.session.commit()
        return professor.dici(), 200

    return {'mensagem': 'Professor não encontrado'}, 404

def deleteProfessor(idProfessor):
    professor = Professor.query.get(idProfessor)
    if professor:
        db.session.delete(professor)
        db.session.commit()
        return {'mensagem': 'Professor deletado'}, 200

    return {'mensagem': 'Professor não encontrado'}, 404
