import heapq

class Fila:

    def __init__(self):
        self.lista = []

    def inserir(self, elemento):
        self.lista.append(elemento)

    def remover(self):
        return self.lista.pop(0)

    def vazia(self):
        return len(self.lista) == 0

class Pilha:

    def __init__(self):
        self.lista = []

    def inserir(self, elemento):
        self.lista.append(elemento)

    def remover(self):
        return self.lista.pop()

    def vazia(self):
        return len(self.lista) == 0

class ListaDePrioridade:

    def __init__(self, funcaoPrioridade):
        self.lista = []
        self.contador = 0
        self.funcaoPrioridade = funcaoPrioridade

    def inserir(self, elemento):
        registro = (self.funcaoPrioridade(elemento), self.contador, elemento)
        heapq.heappush(self.lista, registro)
        self.contador += 1

    def remover(self):
        (_, _, elemento) = heapq.heappop(self.lista)
        return elemento

    def vazia(self):
        return len(self.lista) == 0






