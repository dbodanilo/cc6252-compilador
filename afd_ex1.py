### Compiladores (CC6252)

### Grupo:
### Markel Macedo
### Rafael Lino
### Danilo Bizarria
### Matheus Ferreira
### Kaike Rodrigues
print('Digit uma cadeia utilizando o alfabeto [0,1]:\n')
cadeia = input()
estado = 0
def switch_afd(num, state):
    cases = {
            ('0', 0): 1,
            ('1', 1): 2,
            ('0', 2): 3
            }
    return cases.get((num, state))

def afd1():
    global cadeia
    global estado
    if cadeia != '':
        for c in cadeia:
            novo_estado = switch_afd(c, estado)
            estado = novo_estado
            if estado == None:
                break
    if estado == 3:
        print(cadeia+' (RECONHECIDO)')
    else:
        print('Cadeia nao reconhecida')
    estado = 0

def switch_afd2(num, state):
    cases = {
            ('', 0): 1,
            ('0', 0): 1,
            ('0', 1): 1,
            ('1', 0): 2,
            ('1', 2): 2
            }
    return cases.get((num, state))

def afd2():
    global cadeia
    global estado
    
    if cadeia != '':
        for c in cadeia:
            novo_estado = switch_afd2(c, estado)
            estado = novo_estado
            if(estado == None):
                break
    else:
        novo_estado = switch_afd2('', estado)
        estado = novo_estado
    if estado == 1 or estado == 2:
        if cadeia == '':
            print('Cadeia vazia (RECONHECIDO)')
        else:
            print(cadeia+' (RECONHECIDO)')
    else:
        print('Cadeia nao reconhecida')
    estado = 0

def switch_afd3(num, state):
    cases = {
            ('0', 0): 0,
            ('1', 0): 1,
            ('1', 1): 2,
            ('1', 2): 2
            }
    return cases.get((num, state))

def afd3():
    global cadeia
    global estado

    if cadeia != '':
        for c in cadeia:
            novo_estado = switch_afd3(c, estado)
            estado = novo_estado
            if (estado == None):
                break
    else:
        novo_estado = switch_afd3('', estado)
        estado = novo_estado
    if estado == 2:
        print(cadeia+' '+'(RECONHECIDO)')
    else:
        print('Cadeia nao reconhecida')
    estado = 0;

print("_________\n")
print("Resultado para a expressao '010':\n ")
afd1()
print("_________\n")
print("Resultado para a expressao '0*|1*':\n ")
afd2()
print("_________\n")
print("Resultado para a expressao '0*11+':\n ")
afd3()
