from flask import Flask, jsonify, request
from model.aluno_model import Aluno
from model.professor_model import Professor
from model.turma_model import Turma

def resetar_dados():
    Aluno.alunos.clear()
    Professor.professores.clear()
    Turma.turmas.clear()
    return jsonify({'mensagem': 'Dados resetados com sucesso'}), 200