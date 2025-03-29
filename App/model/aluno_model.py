from datetime import date, datetime
from flask import Flask, jsonify, request

class Aluno():
    alunos = []

    def __init__(self, id, nome, turma_id, data_nascimento, nota_semestre_1, nota_semestre_2):
        if not isinstance(nome, str) or len(nome) > 100:
            raise ValueError("Nome inválido. Deve ser uma string de até 100 caracteres")
        if not isinstance(nota_semestre_1, (int, float)) or not isinstance(nota_semestre_2, (int, float)):
            raise ValueError("Notas inválidas. Devem ser números float")
        
        self.id = id
        self.nome = nome
        self.idade = self.CalcularIdade(data_nascimento)
        self.turma = turma_id
        self.data_nascimento = data_nascimento
        self.nota_1 = nota_semestre_1
        self.nota_2 = nota_semestre_2
        self.media_final = (nota_semestre_1 + nota_semestre_2) / 2
        Aluno.alunos.append(self)
    
    def CalcularIdade(self, data_nascimento):
        try:
            dataNascimento = datetime.strptime(data_nascimento, "%Y-%m-%d")
        except ValueError:
            raise ValueError("O formato da data de nascimento está errado, passe YYYY-MM-DD")

        hoje = datetime.now()
        idade = hoje.year - dataNascimento.year - ((hoje.month, hoje.day) < (dataNascimento.month, dataNascimento.day))
        return idade

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

Aluno(1, "João Silva", "1A", "2004-05-10", 7.5, 8.0)
Aluno(2, "Maria Souza", "2B", "2002-09-15", 6.0, 9.5)
Aluno(3, "Carlos Oliveira", "1A", "2005-02-20", 8.5, 7.0)



class AlunoNaoEncontrado(Exception):
    pass

def Listar_aluno():
    return jsonify([aluno.dici() for aluno in Aluno.alunos])


def getAlunosPorID(idAluno):
    for aluno in Aluno.alunos:
        if aluno.id == idAluno:
            return jsonify(aluno.dici())
    return jsonify({'mensagem': 'Aluno não encontrado'}), 404


def createAluno():
    dados = request.json

    id = dados.get("id", "")
    if not id:
        return jsonify({'mensagem': 'O aluno necessita de um id'}), 400
    if not isinstance(id, int) or id <= 0:
        return jsonify({'mensagem': 'ID inválido. Deve ser um número inteiro positivo'}), 400
    for aluno in Aluno.alunos:
        if aluno.id == id:
            return jsonify({'mensagem': 'ID já utilizado'}), 400

    nome = dados.get("nome", "")
    if not nome:
        return jsonify({'mensagem': 'O aluno necessita de um nome'}), 400
    
    data_nascimento = dados.get("Data de nascimento", "")
    if not data_nascimento:
        return jsonify({'mensagem': 'O aluno necessita ter data de nascimento'}), 400
    
    nota_semestre_1 = dados.get("Nota do primeiro semestre", 0)
    nota_semestre_2 = dados.get("Nota do segundo semestre", 0)
    if not isinstance(nota_semestre_1, (int, float)) or not isinstance(nota_semestre_2, (int, float)):
        return jsonify({'mensagem': 'Notas inválidas, passe números'}), 400

    try:
        novo_aluno = Aluno(
            id = id,
            nome = nome,
            turma_id = dados.get("Turma", ""),
            data_nascimento = data_nascimento,
            nota_semestre_1 = nota_semestre_1,
            nota_semestre_2 = nota_semestre_2
        )
    except ValueError as e:
        return jsonify({'mensagem': str(e)}), 400
    
    return jsonify(novo_aluno.dici()), 201


def updateAluno(idAluno):
    try:
        for aluno in Aluno.alunos:
            if aluno.id == idAluno:
                dados = request.json

                if "nome" not in dados or not dados["nome"].strip():
                    return jsonify({'mensagem': 'O aluno necessita de um nome'}), 400

                if "Data de nascimento" not in dados or not dados["Data de nascimento"].strip():
                    return jsonify({'mensagem': 'A data de nascimento é obrigatória'}), 400

                aluno.nome = dados["nome"]
                aluno.turma = dados.get('Turma', aluno.turma)

                try:
                    aluno.data_nascimento = dados["Data de nascimento"]
                    aluno.idade = aluno.CalcularIdade(aluno.data_nascimento)
                except ValueError as e:
                    return jsonify({'mensagem': str(e)}), 400

                nota_semestre_1 = dados.get('Nota do primeiro semestre', aluno.nota_1)
                nota_semestre_2 = dados.get('Nota do segundo semestre', aluno.nota_2)
                if not isinstance(nota_semestre_1, (int, float)) or not isinstance(nota_semestre_2, (int, float)):
                    return jsonify({'mensagem': 'Notas inválidas, passe números'}), 400
                
                aluno.nota_1 = nota_semestre_1
                aluno.nota_2 = nota_semestre_2
                aluno.media_final = (aluno.nota_1 + aluno.nota_2) / 2
                
                return jsonify(aluno.dici())

        return jsonify({'mensagem': 'Aluno não encontrado'}), 404

    except Exception as e:
        return jsonify({'mensagem': f'Erro inesperado: {str(e)}'}), 500


def deleteAluno(idAluno):
    for aluno in Aluno.alunos:
        if aluno.id == idAluno:
            Aluno.alunos.remove(aluno)
            return jsonify({'mensagem': 'Aluno deletado'})
        
    return jsonify({'mensagem': 'Aluno não encontrado'}), 404
