from flask import Flask, jsonify, request
from config import db

class Professor(db.Model):
    __tablename__ = "Professor"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    idade = db.Column(db.Integer)
    materia = db.Column(db.String(40))
    observacoes = db.Column(db.String(50))

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
    return jsonify([professor.dici() for professor in professores])

def getProfessorPorID(idProfessor):
    professor = Professor.query.get(idProfessor)
    if professor:
        return jsonify(
            {
                "id": professor.id,
                "nome": professor.nome,
                "idade": professor.idade,
                "Materia": professor.materia,
                "Observações": professor.observacoes,
            }
        )
        
    return jsonify({'mensagem': 'Professor não encontrado'}), 404

def createProfessor():
    dados = request.json

    id = dados.get("id", "")
    if not id:
        return jsonify({'mensagem': 'O professor necessita de um id'}), 400
    if not isinstance(id, int) or id <= 0:
        return jsonify({'mensagem': 'ID inválido. Deve ser um número inteiro positivo'}), 400
    if Professor.query.get(id):
        return jsonify({'mensagem': 'ID já utilizado'}), 400

    nome = dados.get("nome", "")
    if not nome:
        return jsonify({'mensagem': 'O professor necessita de um nome'}), 400
    
    materia = dados.get("Materia", "")
    if not materia:
        return jsonify({'mensagem': 'O professor necessita de uma matéria'}), 400

    novo_professor = Professor(
        id = id,
        nome = nome,
        idade = dados.get("idade", ""),
        materia = materia,
        observacoes = dados.get("Observações", "")
    )
    db.session.add(novo_professor)
    db.session.commit()
    return jsonify(novo_professor.dici()), 201

def updateProfessor(idProfessor):
    try:
        professor = Professor.query.get(idProfessor)
        if professor:
            dados = request.json
                
            nome = dados.get('nome', "").strip()
            if not nome: 
                return jsonify({'erro': 'O professor necessita de um nome'}), 400

            materia = dados.get("Materia", "").strip()
            if not materia:
                return jsonify({'mensagem': 'O professor necessita de uma matéria'}), 400

            professor.nome = nome
            professor.idade = dados.get("idade", "")
            professor.materia = materia
            professor.observacoes = dados.get("Observações", "")

            db.session.commit()
            return jsonify(professor.dici())

        return jsonify({'mensagem': 'Professor não encontrado'}), 404

    except Exception as e:
        return jsonify({'mensagem': f'Erro inesperado: {str(e)}'}), 500

def deleteProfessor(idProfessor):
    professor = Professor.query.get(idProfessor)
    if professor:
        db.session.delete(professor)
        db.session.commit()
        return jsonify({'mensagem': 'Professor deletado'})
        
    return jsonify({'mensagem': 'Professor não encontrado'}), 404
