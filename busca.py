import math

from estruturasDeDados import Fila
from estruturasDeDados import Pilha
from estruturasDeDados import ListaDePrioridade
from mapa import Terreno


class Acao:
    NORTE = 'norte'
    SUL = 'sul'
    LESTE = 'leste'
    OESTE = 'oeste'

class Estado:

    def __init__(self, id, custo):
        """
        :param id: Um par ordenado.
        """
        self.id = id
        self.i = id[0]
        self.j = id[1]
        self.custo = custo

class Custo:
    AGUA = 10
    GRAMA = 1
    MONTANHA = 60

class Problema:
    """
    Classe que modela o problema de busca no qual o espaço de estados
    é uma matriz 42x42 e as possíveis ações são movimentos nas direções
    norte, sul, leste e oeste.
    """

    def __init__(self, estadoInicial, estadoFinal, mapa):
        self.mapa = mapa
        self.estadoInicial = self.criarEstado(estadoInicial)
        self.estadoFinal = self.criarEstado(estadoFinal)
        self.acoes = Acao()


    def definirCustoDoEstado(self, id):
        if id not in self.mapa.getTiles():
            return math.inf
        terreno = self.mapa.getTiles()[id]
        custo = 0
        if terreno == Terreno.AGUA:
            custo = Custo.AGUA
        elif terreno == Terreno.GRAMA:
            custo = Custo.GRAMA
        elif terreno == Terreno.MONTANHA:
            custo = Custo.MONTANHA
        return custo

    def criarEstado(self, id):
        custo = self.definirCustoDoEstado(id)
        e = Estado(id, custo)
        return e

    def estadosAdjacentes(self, estado):
        """
        Função que gera os estados adjacentes ao estado atual.
        :param estado: Estado atual do agente.
        :return: Lista de estados.
        """
        if not estado: # estado inválido
            return
        adjacencias = []
        if estado.i == 0 and estado.j == 0: # Estado é o canto superior esquerdo da matriz
            e1 = self.criarEstado((estado.i+1, estado.j))
            e2 = self.criarEstado((estado.i, estado.j+1))
            adjacencias.append(e1)
            adjacencias.append(e2)
        elif estado.i == 0 and estado.j == 41: # Estado é o canto superior direito da matriz
            e1 = self.criarEstado((estado.i+1, estado.j))
            e2 = self.criarEstado((estado.i, estado.j-1))
            adjacencias.append(e1)
            adjacencias.append(e2)
        elif estado.i == 0: # Estado é uma das demais posições da primeira linha da matriz
            e1 = self.criarEstado((estado.i+1, estado.j))
            e2 = self.criarEstado((estado.i, estado.j+1))
            e3 = self.criarEstado((estado.i, estado.j-1))
            adjacencias.append(e1)
            adjacencias.append(e2)
            adjacencias.append(e3)
        elif estado.i == 41 and estado.j == 0: # Estado é o canto inferior esquerdo da matriz
            e1 = self.criarEstado((estado.i-1, estado.j))
            e2 = self.criarEstado((estado.i, estado.j+1))
            adjacencias.append(e1)
            adjacencias.append(e2)
        elif estado.i == 41 and estado.j == 41: # Estado é o canto inferior direito da matriz
            e1 = self.criarEstado((estado.i-1, estado.j))
            e2 = self.criarEstado((estado.i, estado.j-1))
            adjacencias.append(e1)
            adjacencias.append(e2)
        elif estado.i == 41: # Estado é uma das demais posições da última linha da matriz
            e1 = self.criarEstado((estado.i-1, estado.j))
            e2 = self.criarEstado((estado.i, estado.j+1))
            e3 = self.criarEstado((estado.i, estado.j-1))
            adjacencias.append(e1)
            adjacencias.append(e2)
            adjacencias.append(e3)
        elif estado.j == 0: # Estado é uma das demais posições da primeira coluna da matriz
            e1 = self.criarEstado((estado.i+1, estado.j))
            e2 = self.criarEstado((estado.i-1, estado.j))
            e3 = self.criarEstado((estado.i, estado.j+1))
            adjacencias.append(e1)
            adjacencias.append(e2)
            adjacencias.append(e3)
        elif estado.j == 41: # Estado é uma das demais poisições da última coluna da matriz
            e1 = self.criarEstado((estado.i+1, estado.j))
            e2 = self.criarEstado((estado.i-1, estado.j))
            e3 = self.criarEstado((estado.i, estado.j-1))
            adjacencias.append(e1)
            adjacencias.append(e2)
            adjacencias.append(e3)
        else: # Estado não pertence linhas e colunas mais externas da matriz
            e1 = self.criarEstado((estado.i+1, estado.j))
            e2 = self.criarEstado((estado.i-1, estado.j))
            e3 = self.criarEstado((estado.i, estado.j+1))
            e4 = self.criarEstado((estado.i, estado.j-1))
            adjacencias.append(e1)
            adjacencias.append(e2)
            adjacencias.append(e3)
            adjacencias.append(e4)
        return adjacencias

def obterSolucao(arvoreDeBusca, estadoFinal):
    """
    Obtém a sequência de estados que leva ao estado final.
    :param arvoreDeBusca: dicionario cujas chaves são os nós e os valores, seus pais.
    :param estadoFinal: último estado na sequência de solução.
    :return: lista ordenada de estados.
    """
    solucao = []
    estado = estadoFinal
    terminou = False
    while not terminou:
        solucao.insert(0, estado)
        if estado.id not in arvoreDeBusca:
            terminou = True
        else:
            estado = arvoreDeBusca[estado.id]
    return solucao


def buscaEmGrafo(problema, fronteira):
    """
    Algoritmo genérico para busca em grafo.
    :param problema: definição do problema, contendo estado inicial, final e função sucessora.
    :param fronteira: estrutura de dados (fila, pilha ou lista de prioridade) que define a estratégia da busca.
    :return: sequencia de estados que soluciona o problema de busca.
    """
    arvoreDeBusca = {} # Dicionário cujas chaves são os nós e os valores, seus pais.
    explorados = []
    fronteira.inserir(problema.estadoInicial)
    while not fronteira.vazia():
        atual = fronteira.remover()
        if atual.id == problema.estadoFinal.id:
            problema.estadoFinal.custo = atual.custo
            break
        if atual not in explorados:
            explorados.append(atual.id)
            novosEstados = problema.estadosAdjacentes(atual)
            for adjacente in novosEstados:
                if adjacente.id not in explorados:
                    adjacente.custo += atual.custo
                    arvoreDeBusca[adjacente.id] = atual
                    fronteira.inserir(adjacente)
    return obterSolucao(arvoreDeBusca, problema.estadoFinal)

def buscaEmLargura(problema):
    fronteira = Fila()
    return buscaEmGrafo(problema, fronteira)

def buscaEmProfundidade(problema):
    fronteira = Pilha()
    return buscaEmGrafo(problema, fronteira)

def aEstrela(problema, heuristica):
    funcaoPrioridade = lambda estado: estado.custo + heuristica(estado, problema.estadoFinal)
    fronteira = ListaDePrioridade(funcaoPrioridade)
    return buscaEmGrafo(problema, fronteira)




