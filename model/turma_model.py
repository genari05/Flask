from flask import Flask, jsonify, request
from model.professor_model import Professor
from config import db

class Turma(db.Model):
    __tablename__ = "Turma"

    id = db.Column(db.Integer, primary_key=True)
    id_professor = db.Column(db.Integer, db.ForeignKey("Professor.id"), nullable=False)
    descricao = db.Column(db.String(100))
    ativo = db.Column(db.Boolean)

    professor = db.relationship("Professor", back_populates="turmas")
    alunos = db.relationship("Aluno", back_populates="turma")

    def __init__(self, descricao, id_professor, ativo=True):
        self.descricao = descricao
        self.id_professor = id_professor
        self.ativo = ativo
    
    def dici(self):
        return {
            "id": self.id,
            "Descrição": self.descricao,
            "Ativo": self.ativo,
            "Professor": {
                "nome": self.professor.nome
            } if self.professor else None
    }

def Get_turmas():
    turmas = Turma.query.all()
    return [turma.dici() for turma in turmas]

def getTurmaPorID(idTurma):
    turma = Turma.query.get(idTurma)
    if turma:
        return turma.dici(), 200
    else:
        return {'mensagem': 'Turma não encontrada'}, 404

def createTurma(dados):
    descricao = dados.get("Descrição", "")
    if not descricao:
        return {'mensagem': 'A turma necessita de uma descrição'}, 400
    
    ativo = dados.get("Ativo", "")
    if not isinstance(ativo, bool):
        return {'mensagem': 'A turma deve estar ativa ou inativa'}, 400

    nova_turma = Turma(
        descricao = descricao,
        id_professor = dados.get('Professor', {}).get('id'),
        ativo = ativo
    )

    db.session.add(nova_turma)
    db.session.commit()
    return nova_turma.dici(), 201

def updateTurma(idTurma, dados):
    turma = Turma.query.get(idTurma)
    if turma:
        descricao = dados.get("Descrição", "")
        if not descricao:
            return {'mensagem': 'A turma necessita de uma descrição'}, 400
    
        ativo = dados.get("Ativo", "")
        if not ativo:
            return {'mensagem': 'A turma deve estar ativa ou inativa'}, 400
            
        turma.descricao = descricao
        turma.ativo = ativo

        professor_id = dados.get('Professor', {}).get('id')
        if professor_id:
            professor = Professor.query.get(professor_id)
            if not professor:
                return {'mensagem': 'Professor não encontrado'}, 404
            turma.professor = professor
                
        db.session.commit()
        return turma.dici(), 200
    
    return {'mensagem': 'Turma não encontrada'}, 404

def deleteTurma(idTurma):
    turma = Turma.query.get(idTurma)
    if turma:
        db.session.delete(turma)
        db.session.commit()
        return {'mensagem': 'Turma deletada'}
        
    return {'mensagem': 'Turma não encontrada'}, 404
