import sys

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'

# Imprime texto com cores. Por exemplo, para imprimir "Oi mundo!" em vermelho, basta usar
#
# printCores('Oi mundo!', RED)
# printCores('Texto amarelo e negrito', YELLOW + BOLD)

def printCores(texto, cor) :
  print(cor + texto + RESET)
  

# Adiciona um compromisso aa agenda. Um compromisso tem no minimo
# uma descrição. Adicionalmente, pode ter, em caráter opcional, uma
# data (formato DDMMAAAA), um horário (formato HHMM), uma prioridade de A a Z, 
# um contexto onde a atividade será realizada (precedido pelo caractere
# '@') e um projeto do qual faz parte (precedido pelo caractere '+'). Esses
# itens opcionais são os elementos da tupla "extras", o segundo parâmetro da
# função.
#
# extras ~ (data, hora, prioridade, contexto, projeto)
#
# Qualquer elemento da tupla que contenha um string vazio ('') não
# deve ser levado em consideração. 
def adicionar(descricao, extras):
  # não é possível adicionar uma atividade que não possui descrição. 
  if descricao  == '' :
    return False
                                            #(desc, (data, hora, pri, contexto, projeto) 
  atividadeOrdenada = [extras[0], extras[1], extras[2], descricao, extras[3], extras[4]] # DDMMAAAA HHMM (P) DESC @CONTEXT +PROJ
  novaAtividade = ' '.join(atividadeOrdenada) #transformando em string
  try: 
    fp = open(TODO_FILE, 'a')
    fp.write(novaAtividade + '\n')
    fp.close()
  except IOError as err:
    print("Não foi possível escrever para o arquivo ", TODO_FILE)
    print(err)
    return False

  return True


# Valida a prioridade.
def prioridadeValida(pri):
  pri = pri.upper()
  if len(pri) != 3:
    return False
  elif pri[0] != '(' or pri[2] != ')':
    return False
  elif (pri[1] < 'A' or pri[1] > 'Z'):
    return False
  return True


# Valida a hora. Consideramos que o dia tem 24 horas, como no Brasil, ao invés
# de dois blocos de 12 (AM e PM), como nos EUA.
def horaValida(horaMin):
  if len(horaMin) != 4 or not soDigitos(horaMin):
    return False
  else:
    if horaMin[0:2] > '23' or horaMin[2:] > '59': #checando se a hora está maior que 23.
      return False                      
    return True

# Valida datas. Verificar inclusive se não estamos tentando
# colocar 31 dias em fevereiro. Não precisamos nos certificar, porém,
# de que um ano é bissexto. 
def dataValida(data) :
  if len(data) != 8 or not soDigitos(data): #checando se nao é menor ou maior que 8 carecteres e se é so numeros
    return False
  else:
    if data[:2] > '31' or data[2:4] > '12': #checando se o dia e o mês serão inválidos(caso geral)
      return False
    
    if data[2:4] == '02' and data[:2] > '29': #Fevereiro 
      return False

    if data[2:4] == '04' and data[:2] > '30': #Abril
      return False

    if data[2:4] == '06' and data[:2] > '30': #Junho
      return False

    if data[2:4] == '09' and data[:2] > '30': #Setembro
      return False

    if data[2:4] == '11' and data[:2] > '30': #Novembro
      return False

    return True

  
# Valida que o string do projeto está no formato correto. 
def projetoValido(proj):
  if len(proj) > 2 and proj[0] == '+': #validando se começa com + e tem mais de dois caracteres.
    return True
  return False


# Valida que o string do contexto está no formato correto. 
def contextoValido(cont):
  if len(cont) > 2 and cont[0] == '@': #validando se começa com + e tem mais de dois caracteres.
    return True
  return False

# Valida que a data ou a hora contém apenas dígitos, desprezando espaços
# extras no início e no fim.
def soDigitos(numero) :
  if type(numero) != str :
    return False
  for x in numero :
    if x < '0' or x > '9' :
      return False
  return True


# Dadas as linhas de texto obtidas a partir do arquivo texto todo.txt, devolve
# uma lista de tuplas contendo os pedaços de cada linha, conforme o seguinte
# formato:
#
# (descrição, prioridade, (data, hora, contexto, projeto))
#
# É importante lembrar que linhas do arquivo todo.txt devem estar organizadas de acordo com o
# seguinte formato:
#
# DDMMAAAA HHMM (P) DESC @CONTEXT +PROJ
#
# Todos os itens menos DESC são opcionais. Se qualquer um deles estiver fora do formato, por exemplo,
# data que não tem todos os componentes ou prioridade com mais de um caractere (além dos parênteses),
# tudo que vier depois será considerado parte da descrição.  
def organizar(linhas):
  itens = []  
  for l in linhas:
    
    data = '' 
    hora = ''
    pri = ''
    desc = ''
    contexto = ''
    projeto = ''
  
    l = l.strip() # remove espaços em branco e quebras de linha do começo e do fim
    
    tokens = l.split() # quebra o string em palavras
    
    # Processa os tokens um a um, verificando se são as partes da atividade.
    # Por exemplo, se o primeiro token é uma data válida, deve ser guardado
    # na variável data e posteriormente removido a lista de tokens. Feito isso,
    # é só repetir o processo verificando se o primeiro token é uma hora. Depois,
    # faz-se o mesmo para prioridade. Neste ponto, verifica-se os últimos tokens
    # para saber se são contexto e/ou projeto. Quando isso terminar, o que sobrar
    # corresponde à descrição. É só transformar a lista de tokens em um string e
    # construir a tupla com as informações disponíveis. 

    dataCheck = False
    horaCheck = False
    i = 0
    while i < len(tokens): 

      if tokens[i][:1] <= '9' and tokens[i][:1] >= '0': #checando se é um número pra testar hora e data
          
        if len(tokens[i]) == 8 and not(dataCheck): #vendo se é uma data
          
          if dataValida(tokens[i]): #se for válida adiciona a variável
            data = tokens[i]
            tokens.pop(i)
            dataCheck = True #nao deixa mais entrar nessa condição, pois invalidou a primeira data, a segunda poderá ser descrição.

          else:
            desc = desc +' '+tokens[i]
            tokens.pop(i) #mesmo que seja válida você remove pra no final ficar fácil add variável em descrição

          
       
        elif len(tokens[i]) == 4 and not(horaCheck): # vendo se é uma hora

          if horaValida(tokens[i]): #mesmo processo da Data
            hora = tokens[i]
            tokens.pop(i)
            horaCheck = True
            
          else:
            desc = desc +' '+tokens[i]
            tokens.pop(i)
            
          
          
        else:
          desc = desc +' '+tokens[i]
          tokens.pop(i)

        
          
      else:   #se não for número aí vamos as letras
        
        if tokens[i][:1] == '+': #checando o projeto
          
          if projetoValido(tokens[i]):
            projeto = tokens[i]
          tokens.pop(i)
          
          
        elif tokens[i][:1] == '(': #checando prioridade

          if prioridadeValida(tokens[i]):
            pri = tokens[i]
          tokens.pop(i)
          

        elif tokens[i][:1] == '@': #checando contexto

          if contextoValido(tokens[i]):
            contexto = tokens[i]
          tokens.pop(i)
        else:
          desc = desc +' '+tokens[i]
          tokens.pop(i)
      
    desc = desc +''+ ' '.join(tokens) #pegando o resto do que sobrou nos tokens
    if desc == '' or desc == ' '*len(desc):
      raise ValueError('Não há descrição.')
    
    itens.append((desc, (data, hora, pri, contexto, projeto)))  #(DESC, (DATA, HORA, PRI, CONTEXTO, PROJETO)). 

  return itens

# Datas e horas são armazenadas nos formatos DDMMAAAA e HHMM, mas são exibidas
# como se espera (com os separadores apropridados). 
#
# Uma extensão possível é listar com base em diversos critérios: (i) atividades com certa prioridade;
# (ii) atividades a ser realizadas em certo contexto; (iii) atividades associadas com
# determinado projeto; (vi) atividades de determinado dia (data específica, hoje ou amanhã). Isso não
# é uma das tarefas básicas do projeto, porém. 
def listar():
  
  fp = open(TODO_FILE,'r')
  arquivo_lido = fp.read() #lendo arquivo
  fp.close()
  
  lista_arquivo = arquivo_lido.splitlines() #criando lista sem \n :D
  
  tuplas_organizadas = organizar(lista_arquivo) #organizando em tuplas

  ordenar_tuplas = ordenarPorPrioridade(ordenarPorDataHora(tuplas_organizadas))

  enumerar_lista = {} #dicionário para enumerar
  i = 00 #indice para adicionar enumeração na chave do dicionário
  for x in ordenar_tuplas: #(DESC, (DATA, HORA, PRI, CONTEXTO, PROJETO)). 
    
    if x[1][0] != '' and x[1][1] != '': #se tiver data e hr
      enumerar_lista[i] = '{} {}/{}/{} {}:{} {} {} {} {}'.format(str(i), x[1][0][:2], x[1][0][2:4], x[1][0][4:], x[1][1][:2], x[1][1][2:], x[1][2], x[0], x[1][3], x[1][4])
      
      if x[1][2][1:2] == 'A':
        printCores(enumerar_lista[i], BLUE + BOLD)
      elif x[1][2][1:2] == 'B':
        printCores(enumerar_lista[i], GREEN)
      elif x[1][2][1:2] == 'C':
        printCores(enumerar_lista[i], YELLOW) 
      elif x[1][2][1:2] == 'D':
        printCores(enumerar_lista[i], CYAN)
      else:
        print(enumerar_lista[i])
        
    elif x[1][0] != '' and x[1][1] == '':
      enumerar_lista[i] = '{} {}/{}/{} {} {} {} {}'.format(str(i), x[1][0][:2], x[1][0][2:4], x[1][0][4:], x[1][2], x[0], x[1][3], x[1][4])

      if x[1][2][1:2] == 'A':
        printCores(enumerar_lista[i], BLUE + BOLD)
      elif x[1][2][1:2] == 'B':
        printCores(enumerar_lista[i], GREEN)
      elif x[1][2][1:2] == 'C':
        printCores(enumerar_lista[i], YELLOW) 
      elif x[1][2][1:2] == 'D':
        printCores(enumerar_lista[i], CYAN)
      else:
        print(enumerar_lista[i])
        
    elif x[1][0] == '' and x[1][1] != '':
      enumerar_lista[i] = '{} {}:{} {} {} {} {}'.format(str(i), x[1][1][:2], x[1][1][2:], x[1][2], x[0], x[1][3], x[1][4])

      if x[1][2][1:2] == 'A':
        printCores(enumerar_lista[i], BLUE + BOLD)
      elif x[1][2][1:2] == 'B':
        printCores(enumerar_lista[i], GREEN)
      elif x[1][2][1:2] == 'C':
        printCores(enumerar_lista[i], YELLOW) 
      elif x[1][2][1:2] == 'D':
        printCores(enumerar_lista[i], CYAN)
      else:
        print(enumerar_lista[i])

    elif x[1][0] == '' and x[1][1] == '':
      enumerar_lista[i] = '{} {} {} {} {}'.format(str(i), x[1][2], x[0], x[1][3], x[1][4])

      if x[1][2][1:2] == 'A':
        printCores(enumerar_lista[i], BLUE + BOLD)
      elif x[1][2][1:2] == 'B':
        printCores(enumerar_lista[i], GREEN)
      elif x[1][2][1:2] == 'C':
        printCores(enumerar_lista[i], YELLOW) 
      elif x[1][2][1:2] == 'D':
        printCores(enumerar_lista[i], CYAN)
      else:
        print(enumerar_lista[i])
    i = i + 1
    
def remover(num):          #farei o mesmo que a função listar.
  
  if type(num) != int:
    raise ValueError('é necessário receber uma numeração para que esta função execute')
  
  fp = open(TODO_FILE,'r')
  arquivo_lido = fp.read() 
  fp.close()
  
  lista_arquivo = arquivo_lido.splitlines() 

  tuplas_organizadas = organizar(lista_arquivo) 

  ordenar_tuplas = ordenarPorPrioridade(ordenarPorDataHora(tuplas_organizadas)) #

  enumerar_lista = {}
  i = 0
  for x in ordenar_tuplas: #aqui só crio o dicionário para que ele tenha o mesmo modo que a função listar.
    enumerar_lista[i] = x
    i = i + 1

  atualizar = False  #variavel para ajudar a atualizar o arquivo todo.txt
  if not(num in enumerar_lista): #se o numero nao tiver no dicionario: 
    raise ValueError('Item nã existe')
  else: #caso ele exista, você retira da lista ordenar_tuplas
    ordenar_tuplas.remove(enumerar_lista[num])
    atualizar = True #olha a variavel aqui mudada, caso a lista tenha um item removido

  if atualizar:
    abrir = open(TODO_FILE,'w')
    for x in ordenar_tuplas:
      abrir.write('%s %s %s %s %s %s\n' %(x[1][0], x[1][1], x[1][2], x[0], x[1][3], x[1][4]))
    abrir.close()
  
# prioridade é uma letra entre A a Z, onde A é a mais alta e Z a mais baixa.
# num é o número da atividade cuja prioridade se planeja modificar, conforme
# exibido pelo comando 'l'.

def priorizar(num, prioridade):
  
  if type(num) != int:
    raise ValueError('é necessário receber uma numeração para que esta função execute')
  
  if (prioridade < 'A' or prioridade > 'Z') and (prioridade < 'a' or prioridade > 'z'):
    raise ValueError('a prioridade precisa ser um caractere alfabético')
  prioridade = prioridade.upper()
  prioridade = '(%s)' %(prioridade)
  fp = open(TODO_FILE,'r')
  arquivo_lido = fp.read() 
  fp.close()
  
  lista_arquivo = arquivo_lido.splitlines() 

  tuplas_organizadas = organizar(lista_arquivo) 

  ordenar_tuplas = ordenarPorPrioridade(ordenarPorDataHora(tuplas_organizadas)) #

  enumerar_lista = {}
  i = 0
  for x in ordenar_tuplas: #aqui só crio o dicionário para que ele tenha o mesmo modo que a função listar.
    enumerar_lista[i] = x
    i = i + 1
  
  atualizar = False
  if not(num in enumerar_lista):
    raise ValueError('Item não existe')
  
  if prioridadeValida(enumerar_lista[num][1][2]):
    raise ValueError('Já existe uma prioridade para este item')
  
  
  else:                  #(DESC, (DATA, HORA, PRI, CONTEXTO, PROJETO))
    salve_tupla = (enumerar_lista[num][0],(enumerar_lista[num][1][0], enumerar_lista[num][1][1], prioridade, enumerar_lista[num][1][3], enumerar_lista[num][1][4]))
    ordenar_tuplas.remove(enumerar_lista[num])
    enumerar_lista[num] = salve_tupla
    
    ordenar_tuplas.append(enumerar_lista[num])
    
    atualizar = True

  if atualizar:
    abrir = open(TODO_FILE,'w')
    for x in ordenar_tuplas:
      abrir.write('%s %s %s %s %s %s\n' %(x[1][0], x[1][1], x[1][2], x[0], x[1][3], x[1][4]))
    abrir.close()

  
def fazer(num):

  if type(num) != int:
    raise ValueError('é necessário receber uma numeração para que esta função execute')

  fp = open(TODO_FILE,'r')
  arquivo_lido = fp.read() 
  fp.close()
  
  lista_arquivo = arquivo_lido.splitlines() 

  tuplas_organizadas = organizar(lista_arquivo) 

  ordenar_tuplas = ordenarPorPrioridade(ordenarPorDataHora(tuplas_organizadas)) #

  enumerar_lista = {}
  i = 0
  for x in ordenar_tuplas: 
    enumerar_lista[i] = x
    i = i + 1
    
  atualizar = False
  if not(num in enumerar_lista):
    raise ValueError('Item não existe')

  else:
    para_todo = enumerar_lista[num] #para_todo vai guardar a tupla correspondente para ser escrita no arquivo todo.txt
    ordenar_tuplas.remove(enumerar_lista[num])
    atualizar = True

  if atualizar:
    abrir = open(TODO_FILE,'w')
    for x in ordenar_tuplas:
      
      abrir.write('%s %s %s %s %s %s\n' %(x[1][0], x[1][1], x[1][2], x[0], x[1][3], x[1][4]))
    abrir.close()

  if atualizar:
    
    escrever = open(ARCHIVE_FILE,'a')
    
    escrever.write('%s %s %s %s %s %s\n' %(para_todo[1][0], para_todo[1][1], para_todo[1][2], para_todo[0], para_todo[1][3], para_todo[1][4]))
    escrever.close



def ordenarPorDataHora(itens): #(DESC, (DATA, HORA, PRI, CONTEXTO, PROJETO)).

  i = 0
  while i < len(itens):
    j = 0
    while j < len(itens) -1:
        
      if itens[j][1][0][4:] >= itens[j+1][1][0][4:]:  #organizando por ano
        itens[j], itens[j+1] = itens[j+1], itens[j]
        
        if itens[j][1][0][2:4] >= itens[j+1][1][0][2:4]: #organizando por mês
          itens[j], itens[j+1] = itens[j+1], itens[j]
        
          if itens[j][1][0][:2] >= itens[j+1][1][0][:2]: #organizando por dia
            itens[j], itens[j+1] = itens[j+1], itens[j]

      j = j + 1   #explicação: Se não identar os ifs, tudo fica se desordenando.
    i = i + 1
    
  i = 0
  while i < len(itens):
    j = 0
    while j < len(itens)-1:

      if itens[j][1][0] == itens[j+1][1][0]:
        if itens[j][1][1] > itens[j+1][1][1]: #ordenando por hora
          itens[j], itens[j+1] = itens[j+1], itens[j]
      j = j + 1
    i = i + 1
  
  semDataHr = [] #lista para todos os itens sem data ou hora
  i = 0
  while i < len(itens):
    if itens[i][1][0] == '' or itens[i][1][1] == '':
      semDataHr.append(itens[i])
      itens.pop(i)
      i = i - 1
    i = i + 1
    
  for item in semDataHr: #colocando de volta na lista principal sem ordem definida
    itens.append(item)
  
  return itens


   
def ordenarPorPrioridade(itens): #(DESC, (DATA, HORA, PRI, CONTEXTO, PROJETO)).

  i = 0
  while i < len(itens):
    j = 0
    while j < len(itens) -1:
      if itens[j][1][2] > itens[j+1][1][2]: #sem igual pq se não vai deslocar o que já tá organizado pela data.
        itens[j], itens[j+1] = itens[j+1], itens[j]
      j = j + 1
    i = i + 1
    
  semPrioridade = [] #lista para todos os itens sem prioridade
  i = 0
  while i < len(itens):
    if itens[i][1][2] == '':    
      semPrioridade.append(itens[i])
      itens.pop(i)
      i = i - 1
    i = i + 1
    
  for item in semPrioridade: #colocando de volta na lista principal sem ordem definida
    itens.append(item)
  

  return itens



# Esta função processa os comandos e informações passados através da linha de comando e identifica
# que função do programa deve ser invocada. Por exemplo, se o comando 'adicionar' foi usado,
# isso significa que a função adicionar() deve ser invocada para registrar a nova atividade.
# O bloco principal fica responsável também por tirar espaços em branco no início e fim dos strings
# usando o método strip(). Além disso, realiza a validação de horas, datas, prioridades, contextos e
# projetos. 
def processarComandos(comandos) :
  foiListado = False #criei essa variável como prevenção de remoção de itens aleatórios
  
  if comandos[1] == 'a':
    comandos.pop(0) # remove 'agenda.py'
    comandos.pop(0) # remove 'adicionar'
    itemParaAdicionar = organizar([' '.join(comandos)])[0]
    if itemParaAdicionar[0] != '':
      # itemParaAdicionar = (descricao, (prioridade, data, hora, contexto, projeto))
      adicionar(itemParaAdicionar[0], itemParaAdicionar[1]) # novos itens não têm prioridade
    
    
  elif comandos[1] == 'l':
    foiListado = True #caso seja listado a variavel recebe True
    listar()
    
  elif comandos[1] == 'r':
    remover(int(comandos[2]))

  elif comandos[1] == 'f':
    fazer(int(comandos[2]))
      
    

  elif comandos[1] == 'p':
      priorizar(int(comandos[2]), comandos[3])
      
       


  else :
    print("Comando inválido.")
    
  
# sys.argv é uma lista de strings onde o primeiro elemento é o nome do programa
# invocado a partir da linha de comando e os elementos restantes são tudo que
# foi fornecido em sequência. Por exemplo, se o programa foi invocado como
#
# python3 agenda.py a Mudar de nome.
#
# sys.argv terá como conteúdo
#
# ['agenda.py', 'a', 'Mudar', 'de', 'nome']
processarComandos(sys.argv)
