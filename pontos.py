import pygame
from mapa import Terreno
from mapa import Mapa
from busca import Custo
#ParaPermutacoes
import itertools
import random

#Gerar as Esferas Aleatoriamente
def esferasAleatorias():
    L = []
    while(len(L)<7):
        p = (random.randrange(0,42), random.randrange(0,42))
        if not p in L:
            L.append(p)
    return L

def distanciaManhattan2(x1,y1,x2,y2):
    return abs(x1-x2) + abs(y1-y2)

def maisProximo(ponto, pontos):
    perto = (9999,9999)
    for p in pontos:
        if distanciaManhattan2(p[0], p[1], ponto[0], ponto[1]) < distanciaManhattan2(perto[0], perto[1], ponto[0], ponto[1]):
            perto = p
    return perto
    """perto = ponto
    menorCusto = 999999
    map = Mapa("Mapa01.txt", Tela.LARGURA/42, Tela.ALTURA/42)
    for p in pontos:
        prob = busca.Problema(ponto, p, map)
        heuristica = lambda p1, p2: (abs(p1.i - p2.i) + abs(p1.j - p2.j))*5 # Distancia de Manhattan * multiplicador
        solucao = busca.aEstrela(prob, heuristica)
        custo = solucao.pop().custo
        if custo < menorCusto:
            perto = p
    return perto"""

def imprimeListaArquivo(L, titulo):
    f = open('Lista de Pontos.txt', 'w')
    f.write(titulo + '\n')
    for t in L:
        line = ' '.join(str(x) for x in t)
        f.write(line + '\n')
    f.close()

def pontosFocaisPadrao():
    P = []
    i = j = 3
    for k in range(0,6):
        for l in range(0,6):
            P.append((i+k*7, j+l*7))
    #Testanto e imprimindo os valores no arquivo
    f = open('focosP.txt', 'w')
    for t in P:
        line = ' '.join(str(x) for x in t)
        f.write(line + '\n')
    f.close()
    return P

def CustoM(m, id):
    terreno = m.getTiles()[id]
    custo = 0
    if terreno == Terreno.AGUA:
        custo = Custo.AGUA
    elif terreno == Terreno.GRAMA:
        custo = Custo.GRAMA
    elif terreno == Terreno.MONTANHA:
        custo = Custo.MONTANHA
    return custo

def melhorPonto(i, j, M):
    LI = min(4, i) #limita para não sair pra cima da matriz, i ou j menor que 0
    LJ = min(4, j)
    Atual = (i, j)
    CAtual = CustoM(M, (i, j))
    #print('Inicial:', i, ',',j, ' Custo Inicial', CAtual)
    p = (i,j)
    d = 0 #inf ou grande
    if CAtual == 1:
        return (i, j)
    for k in range(0, LJ+1):
        for l in range(0,LI+1):
            #print('l=',l, 'k=', k , 'Custo (i-l, j-k) = ', CustoM(M, (i-l, j-k)) , 'distancia = ', distanciaManhattan2(i-l, j-k, i,j))
            if CustoM(M, (i-l, j-k)) < CAtual:
                d = distanciaManhattan2(i-l, j-k, i,j)
                CAtual = CustoM(M, (i-l, j-k))
                p = (i-l, j-k)
                #print('IF','ponto: ', p[0], ',', p[1], 'CAtual: ', CAtual)
            elif CustoM(M, (i-l, j-k)) == CAtual:
                if distanciaManhattan2(i - l, j - k, i, j) > 0 and distanciaManhattan2(i - l, j - k, i, j) < d:
                    d = distanciaManhattan2(i - l, j - k, i, j)
                    p = (i - l, j - k)
                    #print('ELIF', 'ponto: ', p[0], ',', p[1], 'CAtual: ', CAtual)
    #print('Melhor ponto: ', p[0], ',', p[1], 'CAtual: ', CAtual, 'LI', LI, 'LJ', LJ)
    return p



