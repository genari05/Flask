from flask import Flask, jsonify, request
from model.aluno_model import Aluno
from model.professor_model import Professor
from model.turma_model import Turma
from config import db

def resetar_dados():
    db.session.query(Aluno).delete()
    db.session.query(Professor).delete()
    db.session.query(Turma).delete()
    db.session.commit()
    return jsonify({'mensagem': 'Dados resetados com sucesso'}), 200