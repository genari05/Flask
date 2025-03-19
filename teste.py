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
''''''
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
        r = requests.post('http://localhost:5000/alunos',json= {
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
       
    def teste_002_aluno_por_id(self):
        #Criar um aluno marcos com id 20 
        r = requests.post('http://localhost:5000/alunos', json={  
            "Data de nascimento": "2003-05-05",
            "Media final": 10.0,
            "Nota do primeiro semestre": 10.,
            "Nota do segundo semestre": 10.0,
            "Turma": "1C",
            "id": 8,
            "idade": 15,
            "nome": "mario"
            })
        resposta = requests.get('http://localhost:5000/alunos/8')
        dic_retornado = resposta.json()# Pega o dicionario e retorna Json
        self.assertEqual(type(dic_retornado), dict)
        self.assertIn('nome',dic_retornado)
        self.assertEqual(dic_retornado['nome'], 'mario')
        
    def teste_003_reseta(self):
         r = requests.post('http://localhost:5000/alunos', json={  
            "Data de nascimento": "2005-05-05",
            "Nota do primeiro semestre": 10,
            "Nota do segundo semestre": 10,
            "Turma": "1C",
            "id": 7,
            "idade": 17,
            "nome": "caio"
            })
     
         r_lista = requests.get('http://localhost:5000/alunos')
         self.assertTrue(len(r_lista.json()) > 0)
         
         r_reseta = requests.post('http://localhost:5000/reseta')
         self.assertEqual(r_reseta.status_code,200)
         r_lista_depois = requests.get('http://localhost:5000/alunos')
        
         #e agora tem que ter 0 elementos
         self.assertEqual(len(r_lista_depois.json()),0)
         
    def teste_004_delete(self):
        r_reseta = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reseta.status_code,200)
        requests.post('http://localhost:5000/alunos', json={  
            "Data de nascimento": "2005-05-05",
            "Nota do primeiro semestre": 10,
            "Nota do segundo semestre": 10,
            "Turma": "1C",
            "id": 10,
            "idade": 20,
            "nome": "cicero"
            })
        requests.post('http://localhost:5000/alunos', json={  
            "Data de nascimento": "2005-05-05",
            "Nota do primeiro semestre": 10,
            "Nota do segundo semestre": 10,
            "Turma": "1C",
            "id": 11,
            "idade": 19,
            "nome": "lucas"
            })
        requests.post('http://localhost:5000/alunos', json={  
            "Data de nascimento": "2005-05-05",
            "Nota do primeiro semestre": 10,
            "Nota do segundo semestre": 10,
            "Turma": "1C",
            "id": 12,
            "idade": 18,
            "nome": "marta"
            })
        
        r_lista = requests.get('http://localhost:5000/alunos')
        lista_retornada = r_lista.json()
        self.assertEqual(len(lista_retornada),3)
        #Removendo o marta id 12
        requests.delete('http://localhost:5000/alunos/12')  
        #Retornando a lista com apenas dois id 8 e 10
        r_lista2 = requests.get('http://localhost:5000/alunos')
        lista_retornada2 = r_lista2.json()
        #e vejo se ficou só um elemento
        self.assertEqual(len(lista_retornada2),2)  
        
        acheilucas = False
        acheiCicero = False
        for aluno in lista_retornada2:
            if aluno['nome'] == 'lucas': 
                acheilucas=True
            if aluno['nome'] == 'cicero':
                acheiCicero=True
                
        if not acheilucas or not acheiCicero:
            self.fail("voce parece ter deletado o aluno errado!")

        r = requests.delete('http://localhost:5000/alunos/11')

        r_lista3 = requests.get('http://localhost:5000/alunos')
        lista_retornada3 = r_lista3.json()
        self.assertEqual(len(lista_retornada3),1) 

        if lista_retornada3[0]['nome'] == 'cicero':
            pass
        else:
            self.fail("voce parece ter deletado o aluno errado!")
              
    def teste_005_editar(self):
        #Reseta
         r_reseta = requests.post('http://localhost:5000/reseta')
         self.assertEqual(r_reseta.status_code,200)
        #Criando um aluno 
         requests.post('http://localhost:5000/alunos', json={  
            "Data de nascimento": "2005-05-05",
            "Nota do primeiro semestre": 10,
            "Nota do segundo semestre": 10,
            "Turma": "1C",
            "id": 11,
            "idade": 18,
            "nome": "lucas"
            })   
         #e peguei o dicionario dele
         r_antes = requests.get('http://localhost:5000/alunos/11')
         self.assertEqual(r_antes.json()['nome'],'lucas')
         
         # vamos fazer um PUT porque vamos alterar apenas o nome mas no ID 11
         requests.put('http://localhost:5000/alunos/11', json={  
            "Data de nascimento": "2005-05-05",
            "Nota do primeiro semestre": 10,
            "Nota do segundo semestre": 10,
            "Turma": "1C",
            "id": 11,
            "idade": 18,
            "nome": "lucas mendes"
            })  
         
         #Vamos puxar e ver o novo nome, agora lucas mensdes 
         r_depois = requests.get('http://localhost:5000/alunos/11')
         self.assertEqual(r_depois.json()['nome'],'lucas mendes')
         self.assertEqual(r_depois.json()['id'],11)
         
    def test_006a_id_inexistente_no_put(self):
        #Reseta
         r_reseta = requests.post('http://localhost:5000/reseta')
         self.assertEqual(r_reseta.status_code,200)
         #estou tentando EDITAR um aluno que nao existe (verbo PUT)
         r = requests.put('http://localhost:5000/alunos/15',json={'nome':'bowser','id':15})
        #tem que dar erro 400 ou 404
        #ou seja, r.status_code tem que aparecer na lista [400,404]
         self.assertIn(r.status_code,[400,404])
        #qual a resposta que a linha abaixo pede?
        #um json, com o dicionario {"erro":"aluno nao encontrado"}
         self.assertEqual(r.json()['mensagem'], 'Aluno não encontrado')
                
    def test_006b_id_inexistente_no_get(self):
        #reseto
        r_reset = requests.post('http://localhost:5000/reseta')
        #vejo se nao deu pau resetar
        self.assertEqual(r_reset.status_code,200)
        #agora faço o mesmo teste pro GET, a consulta por id
        r = requests.get('http://localhost:5000/alunos/15')
        self.assertIn(r.status_code,[400,404])
        #olhando pra essa linha debaixo, o que está especificado que o servidor deve retornar
        self.assertEqual(r.json()['mensagem'], 'Aluno não encontrado')

    def test_006c_id_inexistente_no_delete(self):
        #reseto
        r_reset = requests.post('http://localhost:5000/reseta')
        #vejo se nao deu pau resetar
        self.assertEqual(r_reset.status_code,200)
        r = requests.delete('http://localhost:5000/alunos/15')
        self.assertIn(r.status_code,[400,404])
        self.assertEqual(r.json()['mensagem'], 'Aluno não encontrado')
   
    def test_007b_criar_com_id_ja_existente(self):

        
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        
        r = requests.post('http://localhost:5000/alunos', json={  
            "Data de nascimento": "2005-05-05",
            "Nota do primeiro semestre": 10,
            "Nota do segundo semestre": 10,
            "Turma": "1C",
            "id": 12,
            "idade": 18,
            "nome": "lucas"
            })  
        
        r = requests.post('http://localhost:5000/alunos', json={  
            "Data de nascimento": "2005-05-05",
            "Nota do primeiro semestre": 10,
            "Nota do segundo semestre": 10,
            "Turma": "1C",
            "id": 12,
            "idade": 18,
            "nome": "lucas"
            })  
        self.assertEqual(r.status_code,400)

    def test_008b_put_sem_nome(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code, 200)

        # Criar um aluno válido primeiro
        r_create = requests.post('http://localhost:5000/alunos', json={  
            "Data de nascimento": "2005-05-05",
            "Nota do primeiro semestre": 10,
            "Nota do segundo semestre": 10,
            "Turma": "1C",
            "id": 13,
            "idade": 18,
            "nome": "Tiago"
        })
        self.assertEqual(r_create.status_code, 201)  # API retorna 201 ao criar um aluno

        # Tentar editar o aluno sem enviar nome
        r_update = requests.put('http://localhost:5000/alunos/13', json={  
            "Data de nascimento": "2005-05-05",
            "Nota do primeiro semestre": 10,
            "Nota do segundo semestre": 10,
            "Turma": "1C",
            "id":13,
            "idade": 19
        })
        
        # Verificar se a API retorna erro 400 e a mensagem correta
        self.assertEqual(r_update.status_code, 400)
        self.assertEqual(r_update.json()['mensagem'], 'O aluno necessita de um nome')

    def test_008a_post_sem_nome(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)

        #tentei criar um aluno, sem enviar um nome
        r = requests.post('http://localhost:5000/alunos', json={  
            "Data de nascimento": "2005-05-05",
            "Nota do primeiro semestre": 10,
            "Nota do segundo semestre": 10,
            "Turma": "1C",
            "id": 11,
            "idade": 18,
            })
        self.assertEqual(r.status_code,400)
        
    def test_100_professores_retorna_lista(self):
        r = requests.get('http://localhost:5000/professores')
        self.assertEqual(type(r.json()),type([]))
        
    def test_100b_nao_confundir_professor_e_aluno(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        requests.post('http://localhost:5000/alunos', json={  
            "Data de nascimento": "2005-05-05",
            "Nota do primeiro semestre": 10,
            "Nota do segundo semestre": 10,
            "Turma": "1C",
            "id": 1,
            "idade": 18,
            "nome": "lucas"
            })          
        self.assertEqual(r_reset.status_code,200)
        requests.post('http://localhost:5000/alunos', json={  
            "Data de nascimento": "2005-05-05",
            "Nota do primeiro semestre": 10,
            "Nota do segundo semestre": 10,
            "Turma": "1C",
            "id": 2,
            "idade": 18,
            "nome": "Kathe"
            })          
        self.assertEqual(r_reset.status_code,200)
        r_lista = requests.get('http://localhost:5000/professores')
        self.assertEqual(len(r_lista.json()),0)
        r_lista_alunos = requests.get('http://localhost:5000/alunos')
        self.assertEqual(len(r_lista_alunos.json()),2)
        
        
        
        #'Matheus', 29, 'Filosofia', 'Autor de livros sobre ética'
   
    def test_101_adiciona_professores(self):
        r = requests.post('http://localhost:5000/professores',json={
                    "Materia": "Matemática",
                    "Observações": "Doutor em álgebra",
                    "id": 4,
                    "idade": 40,
                    "nome": "fernando"})
        r = requests.post('http://localhost:5000/professores',json={
                    "Materia": "Matemática",
                    "Observações": "Doutor em álgebra",
                    "id": 5,
                    "idade": 40,
                    "nome": "roberto"})
        
        r_lista = requests.get('http://localhost:5000/professores')
        achei_fernando = False
        achei_roberto = False
        for professor in r_lista.json():
            if professor['nome'] == 'fernando':
                achei_fernando = True
            if professor['nome'] == 'roberto':
                achei_roberto = True
        if not achei_fernando:
            self.fail('professor fernando nao apareceu na lista de professores')
        if not achei_roberto:
            self.fail('professor roberto nao apareceu na lista de professores')
            
    def test_102_professores_por_id(self):
        r = requests.post('http://localhost:5000/professores',json={
                    "Materia": "Matemática",
                    "Observações": "Doutor em álgebra",
                    "id": 6,
                    "idade": 40,
                    "nome": "mario"})
        r_lista = requests.get('http://localhost:5000/professores/6')
        self.assertEqual(r_lista.json()['nome'],'mario')
   
    def test_103_adiciona_e_reseta(self):
        r = requests.post('http://localhost:5000/professores',json={
                    "Materia": "Matemática",
                    "Observações": "Doutor em álgebra",
                    "id": 1,
                    "idade": 40,
                    "nome": "Lois"})
        r_lista = requests.get('http://localhost:5000/professores')
        self.assertTrue(len(r_lista.json()) > 0)
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)
        r_lista_depois = requests.get('http://localhost:5000/professores')
        self.assertEqual(len(r_lista_depois.json()),0)     
     
    def test_104_deleta(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)
        requests.post('http://localhost:5000/professores',json={
                    "Materia": "Matemática",
                    "Observações": "Doutor em álgebra",
                    "id": 8,
                    "idade": 40,
                    "nome": "mario"})
        requests.post('http://localhost:5000/professores',json={
                    "Materia": "Matemática",
                    "Observações": "Doutor em álgebra",
                    "id": 9,
                    "idade": 40,
                    "nome": "jose"})
        r_lista = requests.get('http://localhost:5000/professores')
        self.assertEqual(len(r_lista.json()),2)
        requests.delete('http://localhost:5000/professores/8')
        r_lista = requests.get('http://localhost:5000/professores')
        self.assertEqual(len(r_lista.json()),1)
     
    def test_105_edita(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)
        requests.post('http://localhost:5000/professores',json={
                    "Materia": "Matemática",
                    "Observações": "Doutor em álgebra",
                    "id": 10,
                    "idade": 40,
                    "nome": "Dunga"})
        r_antes = requests.get('http://localhost:5000/professores/10')
        self.assertEqual(r_antes.json()['nome'],'Dunga')
        requests.put('http://localhost:5000/professores/10',json={
                    "Materia": "Matemática",
                    "Observações": "Doutor em álgebra",
                    "id": 10,
                    "idade": 40,
                    "nome": "Dunga mendes"})
        r_depois = requests.get('http://localhost:5000/professores/10')
        self.assertEqual(r_depois.json()['nome'],'Dunga mendes')

    def test_106_id_inexistente(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code, 200)

        # Tentativa de atualizar um professor inexistente (ID 15)
        r = requests.put('http://localhost:5000/professores/15', json={  # Corrigido: Adicionado o ID na URL
            "Materia": "Matemática",
            "Observações": "Doutor em álgebra",
            "idade": 40,
            "nome": "broser"
        })
        self.assertEqual(r.status_code, 404)  # Alterado para 404, pois professor não encontrado deve retornar 404
        self.assertEqual(r.json()['mensagem'], 'Professor não encontrado')  # Correção da chave JSON

        # Tentativa de buscar um professor inexistente
        r = requests.get('http://localhost:5000/professores/15')
        self.assertEqual(r.status_code, 404)  # Alterado para 404
        self.assertEqual(r.json()['mensagem'], 'Professor não encontrado')

        # Tentativa de deletar um professor inexistente
        r = requests.delete('http://localhost:5000/professores/15')
        self.assertEqual(r.status_code, 404)  # Alterado para 404
        self.assertEqual(r.json()['mensagem'], 'Professor não encontrado')

    def test_107_criar_com_id_ja_existente_professor(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)
        r=  requests.post('http://localhost:5000/professores',json={
                    "Materia": "Matemática",
                    "Observações": "Doutor em álgebra",
                    "id": 11,
                    "idade": 40,
                    "nome": "durval"})
        self.assertEqual(r.status_code,201)
        r=  requests.post('http://localhost:5000/professores',json={
                    "Materia": "Matemática",
                    "Observações": "Doutor em álgebra",
                    "id": 11,
                    "idade": 40,
                    "nome": "durval"})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['mensagem'], 'ID já utilizado')
    
    def test_108_post_ou_put_sem_nome(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)
        r =  requests.post('http://localhost:5000/professores',json={
                    "Materia": "Matemática",
                    "Observações": "Doutor em álgebra",
                    "id": 12,
                    "idade": 40,
                    })
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['mensagem'], 'O professor necessita de um nome')
        
        r =  requests.post('http://localhost:5000/professores',json={
                    "Materia": "Matemática",
                    "Observações": "Doutor em álgebra",
                    "id": 13,
                    "idade": 40,
                    "nome": "maximus"})
        self.assertEqual(r.status_code,201)
        r =  requests.put('http://localhost:5000/professores/13',json={
                    "Materia": "Matemática",
                    "Observações": "Doutor em álgebra",
                    "id": 13,
                    "idade": 40,
                    })
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],  'O professor necessita de um nome')

    def test_109_nao_confundir_professor_e_aluno(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        r =  requests.post('http://localhost:5000/professores',json={
                    "Materia": "Matemática",
                    "Observações": "Doutor em álgebra",
                    "id": 1,
                    "idade": 40,
                    "nome": "durval"})
        self.assertEqual(r.status_code,201)
        r =  requests.post('http://localhost:5000/professores',json={
                    "Materia": "Matemática",
                    "Observações": "Doutor em álgebra",
                    "id": 2,
                    "idade": 40,
                    "nome": "leo"})
        self.assertEqual(r.status_code,201)
        r_lista = requests.get('http://localhost:5000/professores')
        self.assertEqual(len(r_lista.json()),2)
        r_lista_alunos = requests.get('http://localhost:5000/alunos')
        self.assertEqual(len(r_lista_alunos.json()),0)

   #ALUNO
    def test_008c_aluno_sem_dataNasci_post(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code,200)
        #tentei criar um aluno, sem enviar a data nascimento
        r = requests.post('http://localhost:5000/alunos', json={  
            "Nota do primeiro semestre": 10,
            "Nota do segundo semestre": 10,
            "Turma": "1C",
            "id": 11,
            "idade": 18,
            "Nome": "Lulu"
            })
        self.assertEqual(r.status_code,400)

    def test_008d_aluno_sem_dataNasc_put(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code, 200)

        # Criar um aluno válido primeiro
        r_create = requests.post('http://localhost:5000/alunos', json={  
            "Data de nascimento": "2005-05-05",
            "Nota do primeiro semestre": 10,
            "Nota do segundo semestre": 10,
            "Turma": "1C",
            "id": 14,
            "idade": 18,
            "nome": "Tiago"
        })
        self.assertEqual(r_create.status_code, 201)  # API retorna 201 ao criar um aluno
       
        # Agora Realizar um put sem data
        r_update = requests.put('http://localhost:5000/alunos/14', json={  
            "Nota do primeiro semestre": 10,
            "Nota do segundo semestre": 10,
            "Turma": "1C",
            "id": 14,
            "idade": 18,
            "nome": "Tiago"
        })
        self.assertEqual(r_update.status_code, 400)
        self.assertEqual(r_update.json()['mensagem'], 'A data de nascimento é obrigatória')
    
    def test_008k_criar_com_id_ja_existente(self):

        # Resetar o estado da API para garantir um ambiente limpo
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code, 200)

        # Criar um aluno com ID 12
        r1 = requests.post('http://localhost:5000/alunos', json={  
            "Data de nascimento": "2005-05-05",
            "Nota do primeiro semestre": 10,
            "Nota do segundo semestre": 10,
            "Turma": "1C",
            "id": 12,
            "idade": 18,
            "nome": "Lucas"
        })  
        self.assertEqual(r1.status_code, 201)  # Esperado sucesso na criação

        # Tentar criar outro aluno com o mesmo ID 12
        r2 = requests.post('http://localhost:5000/alunos', json={  
            "Data de nascimento": "2005-05-05",
            "Nota do primeiro semestre": 10,
            "Nota do segundo semestre": 10,
            "Turma": "1C",
            "id": 12,
            "idade": 18,
            "nome": "Lucas"
        })  
        self.assertEqual(r2.status_code, 400)  # Esperado erro de ID duplicado
        self.assertEqual(r2.json(), {'mensagem': 'ID já utilizado'}) 
    #PROFESSOR
    def test_008e_professor_sem_materia_post(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        r =  requests.post('http://localhost:5000/professores',json={
                    "Observações": "Doutor em álgebra",
                    "id": 1,
                    "idade": 40,
                    "nome": "durval"})
        self.assertEqual(r.status_code,400)
    
    def test_008f_professor_sem_materia_put(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code, 200)

        
        r = requests.post('http://localhost:5000/professores',json={
                    "Materia": "Matemática",
                    "Observações": "Doutor em álgebra",
                    "id": 4,
                    "idade": 40,
                    "nome": "fernando"})
        self.assertEqual(r.status_code, 201)  # API retorna 201 ao criar um aluno
       
        
        r_update = requests.put('http://localhost:5000/professores/4',json={
                    "Observações": "Doutor em álgebra",
                    "id": 4,
                    "idade": 40,
                    "nome": "fernando"})
        self.assertEqual(r_update.status_code, 400)
        self.assertEqual(r_update.json()['mensagem'], 'O professor necessita de uma matéria')
    #TURMA
    def test_008g_turma_sem_descrisao_post(self):
        r_reset = requests.post('http://localhost:5000/reseta')

        r = requests.post('http://localhost:5000/turmas',json={
                "Ativo": True,
                "Professor": "",
                "Materia": "Matemática",
                "Observações": "Doutor em álgebra",
                "idade": 40,
                "id": 1,
                "nome": "twatw"})
        self.assertEqual(r.status_code, 400)

    def test_008h_turma_sem_descrisao_put(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code, 200)

        # Criando uma turma válida primeiro
        r_create = requests.post('http://localhost:5000/turmas', json={
            "id": 1,
            "Descrição": "Turma de matemática",
            "Ativo": True,
            "Professor": {"id": 5}
        })
        self.assertEqual(r_create.status_code, 201)

        # Tentando atualizar sem descrição
        r_update = requests.put('http://localhost:5000/turmas/1', json={
            "Ativo": True,
            "Professor": {"id": 5}
            # "Descrição" foi omitida de propósito para testar a validação
        })
        
        self.assertEqual(r_update.status_code, 400)  # Esperado erro 400
        self.assertIn(r_update.json()["mensagem"], "A turma necessita de uma descrição")  # Mensagem esperada

    def test_008i_turma_sem_ativo_post(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code, 200)

        # Criando uma turma válida primeiro
        r = requests.post('http://localhost:5000/turmas', json={
            "id": 1,
            "Descrição": "Turma 2C",
            "Professor": {"id": 5}
        })
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()['mensagem'], 'A turma deve estar ativa ou inativa') 

    def test_008j_turma_sem_ativo_put(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code, 200)

        # Criando uma turma válida primeiro
        r = requests.post('http://localhost:5000/turmas', json={
            "id": 1,
            "Descrição": "Turma de matemática",
            "Ativo": True,
            "Professor": {"id": 5}
        })
        self.assertEqual(r_reset.status_code, 200)
        
        
        r_update = requests.put('http://localhost:5000/turmas/1', json={
             "id": 1,
            "Descrição": "Turma de matemática",
            "Professor": {"id": 5}
            })
        
        self.assertEqual(r_update.status_code, 400)  # Esperado erro 400
        self.assertIn(r_update.json()["mensagem"], 'A turma deve estar ativa ou inativa')  # Mensagem esperada
        
    def test_008m_turma_com_id_duplicado(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code, 200)

        r_create = requests.post('http://localhost:5000/turmas', json={
            "id": 5,
            "Descrição": "Turma de História",
            "Ativo": True,
            "Professor": {"id": 8}
        })
        self.assertEqual(r_create.status_code, 201)

        r_duplicate = requests.post('http://localhost:5000/turmas', json={
            "id": 5,
            "Descrição": "Turma de História Moderna",
            "Ativo": True,
            "Professor": {"id": 9}
        })
        
        self.assertEqual(r_duplicate.status_code, 400)
        self.assertEqual(r_duplicate.json()['mensagem'], 'ID já utilizado')

    def test_008n_turma_id_invalido(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code, 200)

        r = requests.post('http://localhost:5000/turmas', json={
            "id": "abc",
            "Descrição": "Turma de Filosofia",
            "Ativo": True,
            "Professor": {"id": 10}
        })
        
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()['mensagem'], 'ID da turma deve ser numérico')

    def test_008o_turma_sem_id_post(self):
        r_reset = requests.post('http://localhost:5000/reseta')
        self.assertEqual(r_reset.status_code, 200)

        r = requests.post('http://localhost:5000/turmas', json={
            "Descrição": "Turma de Inglês",
            "Ativo": True,
            "Professor": {"id": 11}
        })
        
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()['mensagem'], 'A turma necessita de um id')
        

def runTests():
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStringMethods)
        unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)
        
if __name__ == '__main__':
    runTests()
