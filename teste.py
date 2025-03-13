import requests
import unittest
from app import app

'''
Cada aluno será representado por um dicionário JSON como o seguinte: 
{"id":1,"nome":"marcos"}

Testes 000 e 001:
Na URL /alunos, se o verbo for GET, 
retornaremos uma lista com um dicionário para cada aluno.

Na URL /alunos, com o verbo POST, ocorrerá a criação do aluno,
enviando um desses dicionários 

Teste 002
Na URL /alunos/<int:id>, se o verbo for GET, devolveremos o nome e id do aluno. 
(exemplo. /alunos/2 devolve o dicionário do aluno(a) de id 2)

Teste 003
Na URL /reseta, apagaremos a lista de alunos e professores (essa URL só atende o verbo POST e DELETE).

Teste 004
Na URL /alunos/<int:id>, se o verbo for DELETE, deletaremos o aluno.
(dica: procure lista.remove)

Teste 005
Na URL /alunos/<int:id>, se o verbo for PUT, 
editaremos o aluno, mudando seu nome. 
Para isso, o usuário vai enviar um dicionário 
com a chave nome, que deveremos processar

Se o usuário manda um dicionário {“nome”:”José”} para a url /alunos/40,
com o verbo PUT, trocamos o nome do usuário 40 para José

Tratamento de erros

Testes 006 a 008b: Erros de usuário darão um código de status 400, e retornarão um dicionário descrevendo o erro. 
No teste 006, tentamos fazer GET, PUT e DELETE na URL  /alunos/15, sendo que o aluno de id 15 não existe. Nesse caso, devemos retornar um código de status 400 e um dicionário {“erro”:'aluno nao encontrado'}
No teste 007, tentamos criar dois alunos com a mesma id. Nesse caso, devemos retornar um código de status 400 e um dicionário {‘erro’:'id ja utilizada'}
No teste 008a, tento enviar um aluno sem nome via post. Nesse caso, devemos retornar um código de status 400 e um dicionário {‘erro’:'aluno sem nome'}
No teste 008b, tento editar um aluno, usando o verbo put, mas mando um dicionário sem nome. Nesse caso, devemos retornar um código de status 400 e um dicionário {“erro”:'aluno sem nome'}
Testes 100 a 109: Teremos as URLs análogas para professores.
'''

class TestStringMethods(unittest.TestCase):
    
    def test_000_alunos_retorna_lista(self):
        r=requests.get('http://localhost:5000/alunos')
        
        if r.status_code == 404:
            self.fail("Voce não defineiu a pagina /alunos no seu server")
        
        try:
            obt_retornado = r.json()
        except:
            self.fail("Queria um Json mas voce retornou outra coisa")
            self.assertEqual(type(obt_retornado), type([]))
            
    def teste_001_adiciona_aluno(self):
        #criar dois alunos
        r= requests.post('http://localhost:5000/alunos',json= {
    "Data de nascimento": "2003-02-01",
    "Media final": 10.0,
    "Nota do primeiro semestre": 10.,
    "Nota do segundo semestre": 10.0,
    "Turma": "1B",
    "id": 4,
    "idade": 16,
    "nome": "Samuel"
  })
        r= requests.post('http://localhost:5000/alunos',json= {
    "Data de nascimento": "2003-05-05",
    "Media final": 10.0,
    "Nota do primeiro semestre": 10.,
    "Nota do segundo semestre": 10.0,
    "Turma": "1C",
    "id": 5,
    "idade": 13,
    "nome": "Davi"
  })
        r_lista =requests.get('http://localhost:5000/alunos')
        lista_retorna = r_lista.json()
        
        achei_samuel = False
        achei_Davi = False
        for aluno in lista_retorna:
            if aluno['nome'] == 'Samuel':
                achei_samuel = True
            if aluno['nome'] == 'Davi':
                achei_Davi = True
            
            
        if not achei_samuel:
            self.fail('aluno Samuel nao apareceu na lista de alunos')
        if not achei_Davi:
            self.fail('aluno Davi nao apareceu na lista de alunos')
            

def runTests():
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStringMethods)
        unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)


if __name__ == '__main__':
    runTests()
