from flask import Flask, jsonify, request
import model.professor_model as modelProfessor
from config import db

class Turma(db.Model):
    __tablename__ = "Turma"

    id = db.Column(db.Integer, primary_key=True)
    id_professor = db.Column(db.Integer)
    descricao = db.Column(db.String(100))
    ativo = db.Column(db.Boolean)

    def __init__(self, id, descricao, professor_id, ativo=True):
        self.id = id
        self.descricao = descricao
        self.professor = self.get_professor_id(professor_id)
        self.ativo = ativo
    
    def get_professor_id(self, professor_id):
        for professor in modelProfessor.Professor.professores:
            if professor.id == professor_id:
                return professor.dici()
        return {"mensagem": "Professor não encontrado"}
    
    def dici(self):
        return {
            "id": self.id,
            "Descrição": self.descricao,
            "Ativo": self.ativo,
            "Professor": self.professor,
        }

def Get_turmas():
    turmas = Turma.query.all()
    return jsonify([turma.dici() for turma in turmas])

def getTurmaPorID(idTurma):
    turma = Turma.query.get(idTurma)
    if turma:
        return jsonify(
            {
                "id": turma.id,
                "Descrição": turma.descricao,
                "Ativo": turma.ativo,
                "Professor": turma.professor,
            }
        )

    return jsonify({'mensagem': 'Turma não encontrada'}), 404

def createTurma():
    dados = request.json

    id = dados.get("id", "")
    if not id:
        return jsonify({'mensagem': 'A turma necessita de um id'}), 400
    if not isinstance(id, int) or id <= 0:
        return jsonify({'mensagem': 'ID da turma deve ser numérico'}), 400
    if Turma.query.get(id):
        return jsonify({'mensagem': 'ID já utilizado'}), 400

    descricao = dados.get("Descrição", "")
    if not descricao:
        return jsonify({'mensagem': 'A turma necessita de uma descrição'}), 400
    
    ativo = dados.get("Ativo", "")
    if not isinstance(ativo, bool):
        return jsonify({'mensagem': 'A turma deve estar ativa ou inativa'}), 400

    nova_turma = Turma(
        id=id,
        descricao=descricao,
        professor_id=dados.get('Professor', {}).get('id'),
        ativo=ativo
    )

    db.session.add(nova_turma)
    db.session.commit()
    return jsonify(nova_turma.dici()), 201

def updateTurma(idTurma):
    turma = Turma.query.get(idTurma)
    if turma:
        dados = request.json

        descricao = dados.get("Descrição", "")
        if not descricao:
            return jsonify({'mensagem': 'A turma necessita de uma descrição'}), 400
    
        ativo = dados.get("Ativo", "")
        if not ativo:
            return jsonify({'mensagem': 'A turma deve estar ativa ou inativa'}), 400
            
        turma.id = turma.id
        turma.descricao = descricao
        turma.ativo = ativo

        professor_id = dados.get('Professor', {}).get('id')
        if professor_id:
            turma.professor = turma.get_professor_id(professor_id)
                
        db.session.commit()
        return jsonify(turma.dici())
    
    return jsonify({'mensagem': 'Turma não encontrada'}), 404

def deleteTurma(idTurma):
    turma = Turma.query.get(idTurma)
    if turma:
        db.session.delete(turma)
        db.session.commit()
        return jsonify({'mensagem': 'Turma deletada'})
        
    return jsonify({'mensagem': 'Turma não encontrada'}), 404
