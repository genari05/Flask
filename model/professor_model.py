from datetime import date, datetime
from flask import Flask, jsonify, request

class Professor():
    professores = []

    def __init__(self, id, nome, idade, materia, observacoes):
        self.id = id
        self.nome = nome
        self.idade = idade
        self.materia = materia
        self.observacoes = observacoes
        Professor.professores.append(self)
    
    def dici(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "idade": self.idade,
            "Materia": self.materia,
            "Observações": self.observacoes,
        }

prof1 = Professor(1, 'Tiago', 40, 'Matemática', 'Doutor em álgebra')
prof2 = Professor(2, 'Katherine', 35, 'Ciências', 'Especialista em biologia')
prof3 = Professor(3, 'Matheus', 29, 'Filosofia', 'Autor de livros sobre ética')



class ProfessorNaoEncontrado(Exception):
    pass

def Get_professores():
    return jsonify([professor.dici() for professor in Professor.professores])


def getProfessorPorID(idProfessor):
    for professor in Professor.professores:
        if professor.id == idProfessor:
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
    for professor in Professor.professores:
        if professor.id == id:
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
    return jsonify(novo_professor.dici()), 201


def updateProfessor(idProfessor):
    try:
        for professor in Professor.professores:
            if professor.id == idProfessor:
                dados = request.json
                
                nome = dados.get('nome', "").strip()
                if not nome: 
                    return jsonify({'erro': 'O professor necessita de um nome'}), 400

                materia = dados.get("Materia", "").strip()
                if not materia:
                    return jsonify({'mensagem': 'O professor necessita de uma matéria'}), 400

                professor.nome = nome
                professor.materia = materia

                try:
                    professor.data_nascimento = dados["Data de nascimento"]
                    professor.idade = professor.CalcularIdade(professor.data_nascimento)
                except ValueError as e:
                    return jsonify({'mensagem': str(e)}), 400

                return jsonify(professor.dici())

        return jsonify({'mensagem': 'Professor não encontrado'}), 404

    except Exception as e:
        return jsonify({'mensagem': f'Erro inesperado: {str(e)}'}), 500


def deleteProfessor(idProfessor):
    for professor in Professor.professores:
        if professor.id == idProfessor:
            Professor.professores.remove(professor)
            return jsonify({'mensagem': 'Professor deletado'})
        
    return jsonify({'mensagem': 'Professor não encontrado'}), 404

