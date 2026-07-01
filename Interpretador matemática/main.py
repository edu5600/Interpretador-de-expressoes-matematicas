from PrettyPrint import PrettyPrintTree

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.esquerda = None
        self.direita = None

def analiseLexica(expressao) :
    tokens = expressao.split()
    tokens = converterParaValor(tokens)
    return tokens


def converterParaValor(tokens)  :
    for i in range(len(tokens)) :
        if tokens[i][0].isdigit() or (tokens[i][0] == "-" and tokens[i][1].isdigit()) :
            if "." in tokens[i] :
                tokens[i] = float(tokens[i])
            else :
                tokens[i] = int(tokens[i])
    return tokens


def isOperator(op) :
    if (op in ["+", "-", "*", "/", "%", "//"]) :
        return True
    else :
        return False


def prioridade(op) :
    if op == "(" : return 0
    elif op == "-" : return 1
    elif op == "+" : return 1
    elif op == "/" : return 2
    elif op == "*" : return 2
    elif op == "%" : return 2
    elif op == "//" : return 2


def shuntingYard(expressao) :
    output = []
    operadores = []
    for obj in expressao :
        if isOperator(obj) :
            if len(operadores) == 0 :
                operadores.append(obj)
            elif prioridade(obj) > prioridade(operadores[-1]):
                operadores.append(obj)
            else:
                while len(operadores) != 0 and prioridade(operadores[-1]) >= prioridade(obj) :
                    output.append(operadores.pop())
                operadores.append(obj)

        elif obj == "(" :
            operadores.append(obj)

        elif obj == ")" :
            op = operadores.pop()
            while (op != "(") :
                output.append(op)
                op = operadores.pop()

        else:
            output.append(obj)

    while (len(operadores) != 0) :
        output.append(operadores.pop())

    return output


def resolver (expressao) :
    tam = len(expressao)
    i = 0
    while i != tam :
        if isOperator(expressao[i]):
            op = expressao.pop(i)
            y = expressao.pop(i - 1)
            x = expressao.pop(i - 2)
            expressao.insert(i - 2, realizarOperacao(x, op, y))
            i -= 2
            tam -= 2
        else:
            i += 1
    return expressao


def realizarOperacao(x, op, y) :
    if op == "+" : return x + y
    elif op == "-" : return x - y
    elif op == "*" : return x * y
    elif op == "/" : return x / y
    elif op == "%" : return x % y
    elif op == "//" : return x // y


def montarArvore(postFix):
    token = postFix.pop()
    nodo = Nodo(token)

    if isOperator(token):
        nodo.direita = montarArvore(postFix)
        nodo.esquerda = montarArvore(postFix)

    return nodo

expressao = input()

expressao = analiseLexica(expressao)
print ("tokens: ", expressao)

expressao = shuntingYard(expressao)
print ("postfix: ", expressao)

arvore = montarArvore(expressao.copy())
pt = PrettyPrintTree(
    get_children=lambda node: [n for n in (node.esquerda, node.direita) if n is not None],
    get_val=lambda node: str(node.valor)
)
pt(arvore)

expressao = resolver(expressao)
print("Resultado da operacao: ", expressao)
