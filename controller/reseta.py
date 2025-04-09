from flask import Blueprint
from model.reseta import resetar_dados

Reseta_Blueprint = Blueprint('reseta', __name__,url_prefix='/reseta')

@Reseta_Blueprint.route('/', methods=['POST'])
def ReseteDados():
    return resetar_dados()