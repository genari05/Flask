from datetime import date, datetime
from flask import Flask, jsonify, request
import model.professor_model as modelProfessor

class Turma():
    turmas = []

    def __init__(self, id, descricao, professor_id, ativo=True):
        self.id = id
        self.descricao = descricao
        self.professor = self.get_professor_id(professor_id)
        self.ativo = ativo
        Turma.turmas.append(self)
    
    def get_professor_id(self, professor_id):
        for professor in modelProfessor.professores:
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


Turma(1,"Turma 1A", 1)
Turma(2, "Turma 2B", 2)
Turma(3, "Turma 3C", 3)


class TurmaNaoEncontrado(Exception):
    pass

def Get_turmas():
    return jsonify([turma.dici() for turma in Turma.turmas])


def getTurmaPorID(idTurma):
    for turma in Turma.turmas:
        if turma.id == idTurma:
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
    for turma in Turma.turmas:
        if turma.id == id:
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

    return jsonify(nova_turma.dici()), 201


def updateTurma(idTurma):
    for turma in Turma.turmas:
        if turma.id == idTurma:
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
                
            return jsonify(turma.dici())
    
    return jsonify({'mensagem': 'Turma não encontrada'}), 404


def deleteTurma(idTurma):
    for turma in Turma.turmas:
        if turma.id == idTurma:
            Turma.turmas.remove(turma)
            return jsonify({'mensagem': 'Turma deletada'})
        
    return jsonify({'mensagem': 'Turma não encontrada'}), 404

