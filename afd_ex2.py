### Compiladores (CC6252)
### Grupo
### Markel Macedo
### Rafael Lino
### Danilo Bizarria
### Matheus Ferreira
### Kaike Rodrigues

print("Digite um dos seguintes inputs:\n>if\n>else\n>then\n>for\n")
cadeia = input()
estado = 0

print('\n_________\n')
########## AFD 'if' ###########

def switch_if(num, state):
    cases = {
            ('i', 0): 1,
            ('f', 1): 2
            }
    return cases.get((num, state))

def afd_if():
    global cadeia
    global estado
    if cadeia != '':
        for c in cadeia:
            novo_estado = switch_if(c, estado)
            estado = novo_estado
            if estado == None:
                break
    else:
        novo_estado = switch_if('', estado)
        estado = novo_estado
    if estado == 2:
        print(cadeia+' '+'(RECONHECIDO)')
    else:
        print('Cadeia nao reconhecida')
    estado = 0


######### AFD 'else' ###########

def switch_else(num, state):
    cases = {
            ('e', 0): 1,
            ('l', 1): 2,
            ('s', 2): 3,
            ('e', 3): 4
            }
    return cases.get((num, state))

def afd_else():
    global cadeia
    global estado
    
    if cadeia != '':
        for c in cadeia:
            novo_estado = switch_else(c, estado)
            estado = novo_estado
            if(estado == None):
                break
    else:
        novo_estado = switch_else('', estado)
        estado = novo_estado
    if estado == 4:
        print(cadeia+' '+'(RECONHECIDO)')
    else:
        print('Cadeia nao reconhecida')
    estado = 0


########## AFD 'then' #############

def switch_then(num, state):
    cases = {
            ('t', 0): 1,
            ('h', 1): 2,
            ('e', 2): 3,
            ('n', 3): 4
            }
    return cases.get((num, state))

def afd_then():
    global cadeia
    global estado

    if cadeia != '':
        for c in cadeia:
            novo_estado = switch_then(c, estado)
            estado = novo_estado
            if (estado == None):
                break
    else:
        novo_estado = switch_then('', estado)
        estado = novo_estado
    if estado == 4:
        print(cadeia+' '+'(RECONHECIDO)')
    else:
        print('Cadeia nao reconhecida')
    estado = 0;



########### AFD 'for' #############

def switch_for(num, state):
    cases = {
            ('f', 0): 1,
            ('o', 1): 2,
            ('r', 2): 3
            }
    return cases.get((num, state))

def afd_for():
    global cadeia
    global estado

    if cadeia != '':
        for c in cadeia:
            novo_estado = switch_for(c, estado)
            estado = novo_estado
            if (estado == None):
                break
    else:
        novo_estado = switch_for('', estado)
        estado = novo_estado
    if estado == 3:
        print(cadeia+' '+'(RECONHECIDO)')
    else:
        print('Cadeia nao reconhecida')
    estado = 0;

print("Resultado 'if':\n ")
afd_if()
print("_________\n")
print("Resultado 'else':\n ")
afd_else()
print("_________\n")
print("Resultado 'then':\n ")
afd_then()
print("_________\n")
print("Resultado 'for':\n ")
afd_for()

