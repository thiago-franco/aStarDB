import pygame
from interface import Tela
from interface import Cor
from mapa import Mapa
import busca
from busca import Problema
from agente import Goku
import pontos

map = Mapa("Mapa01.txt", Tela.LARGURA/42, Tela.ALTURA/42)
mapEsferas = [(1,4), (39,5), (19,9), (3,22), (37,27), (36,29), (22,37)]
#mapEsferas = [(0,0), (0,41), (41,0), (41,41), (25,35), (25,19), (30,10)]
#mapEsferas = pontos.esferasAleatorias()
NUM_ESFERAS = len(mapEsferas)

#Pontos Focais
focos = pontos.pontosFocaisPadrao()

INICIO = (19,19)
fim = pontos.maisProximo(INICIO, focos)
prob = Problema(INICIO, fim, map)
agente = Goku(prob)
esferas = agente.radar(mapEsferas)
esferasAvistadas = []
esferasColetadas = []
for e in esferas:
    mapEsferas.remove(e)
    esferasAvistadas.append(e)
if len(esferas) > 0:
    fim = pontos.maisProximo(agente.estadoAtual.id, esferas)
    esferas.remove(fim)
else:
    focos.remove(fim)

heuristica = lambda p1, p2: (abs(p1.i - p2.i) + abs(p1.j - p2.j))*4.7 # Distancia de Manhattan * multiplicador
print('pensando...')
solucao = busca.aEstrela(prob, heuristica)
custoTotal = 0

# Inicializando a engine
pygame.init()

tela = pygame.display.set_mode((Tela.LARGURA, Tela.ALTURA+30))
fullscreen = False

pygame.display.set_caption("Dragon Ball")

logo = pygame.image.load('dblogo.jpg')

pygame.mixer.music.load('Dragon Ball Theme Song 8 Bit.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.pause()
#Video

VELOCIDADE = 10
ACOMPANHAR_TRAJETO = False
REVISITAR_FOCOS = False

done = False
clock = pygame.time.Clock()
pause = True

while not done:
    # Loop será executado no máximo VELOCIDADE vezes por segundo
    clock.tick(VELOCIDADE)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause = True
                pygame.mixer.music.pause()
            if event.key == pygame.K_f:
                if fullscreen == False:
                    tela = pygame.display.set_mode((Tela.LARGURA, Tela.ALTURA+30), pygame.FULLSCREEN)
                    fullscreen = True
                else:
                    tela = pygame.display.set_mode((Tela.LARGURA, Tela.ALTURA+30))
                    fullscreen = False
    while pause == True:
        tela.blit(logo, (0,0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pause = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = False
                    pygame.mixer.music.unpause()
                if event.key == pygame.K_f:
                    if fullscreen == False:
                        tela = pygame.display.set_mode((Tela.LARGURA, Tela.ALTURA+30), pygame.FULLSCREEN)
                        fullscreen = True
                    else:
                        tela = pygame.display.set_mode((Tela.LARGURA, Tela.ALTURA+30))
                        fullscreen = False

    # Limpa a tela e define cor de fundo
    tela.fill(Cor.PRETO)

    map.desenhar(tela)

    s = agente.estadoAtual
    i = prob.estadoInicial
    f = prob.estadoFinal

    if s.id in esferasAvistadas and s.id not in esferasColetadas:
        if len(esferasColetadas) + 1 == NUM_ESFERAS:
            prob = Problema(agente.estadoAtual.id, INICIO, map)
            solucao = busca.aEstrela(prob, heuristica)
        esferasColetadas.append(s.id)

    if ACOMPANHAR_TRAJETO:
        pygame.draw.rect(tela, Cor.AZULESCURO, [i.i*15, i.j*15,15,15]) # estado inicial atual
        pygame.draw.rect(tela, Cor.VERMELHO, [f.i*15, f.j*15,15,15]) # estado objetivo atual

    for e in esferasAvistadas:
        cor = Cor.AMARELO
        if e in esferasColetadas:
            cor = Cor.CINZA
        pygame.draw.rect(tela, cor, (e[0]*15, e[1]*15, 15, 15)) # esferas avistadas
        #pygame.draw.circle(tela, cor, (e[0]*15,e[1]*15),6)

    # Goku
    pygame.draw.rect(tela, Cor.PRETO, [s.i*15, s.j*15, 15, 15])
    # Radar
    pygame.draw.rect(tela, Cor.ROSA, [(s.i-agente.alcanceRadar)*15, (s.j-agente.alcanceRadar)*15, 15*(agente.alcanceRadar*2+1), 15*(agente.alcanceRadar*2+1)], 1)

    fonteDB = pygame.font.Font("Saiyan-Sans.ttf", 30)
    fonte = pygame.font.SysFont("monospace", 20)
    texto1 = "KI USADO"
    texto2 = ": " + str(agente.custoTotal)
    label1 = fonteDB.render(texto1, 1, (255,255,0))
    label2 = fonte.render(texto2, 1, (255,255,0))

    tela.blit(label1, (225, 632))
    tela.blit(label2, (325, 632))

    # Atualiza a tela
    pygame.display.update()

    esferas += [e for e in esferasAvistadas if e not in esferasColetadas and e not in esferas]
    esferas += agente.radar(mapEsferas)
    for e in esferas:
        if e in mapEsferas:
            mapEsferas.remove(e)
            esferasAvistadas.append(e)
    if len(solucao) > 0 and len(esferasColetadas) < NUM_ESFERAS:
        if len(esferas) > 0 and not agente.coletandoEsfera:
            agente.coletandoEsfera = True
            if REVISITAR_FOCOS:
                # visitará o foco mesmo que o caminho seja desvidado para uma esfera
                if prob.estadoFinal.id not in esferasAvistadas: # se o objetivo não era esfera, então era um foco
                    focos.append(prob.estadoFinal.id)
            proximo = pontos.maisProximo(agente.estadoAtual.id, esferas)
            esferas.remove(proximo)
            prob = Problema((agente.estadoAtual.i, agente.estadoAtual.j), proximo, map)
            print('pensando...')
            solucao = busca.aEstrela(prob, heuristica)
        s = solucao.pop(0)
        if s.id != agente.estadoAtual.id:
            agente.atualizarEstado(s)
            agente.custoTotal += prob.criarEstado(s.id).custo
        if len(solucao) == 0:
            agente.coletandoEsfera = False
            print('custo:', s.custo)
            custoTotal += s.custo
            if len(esferas) > 0:
                proximo = pontos.maisProximo(agente.estadoAtual.id, esferas)
                esferas.remove(proximo)
                prob = Problema((agente.estadoAtual.i, agente.estadoAtual.j), proximo, map)
                print('pensando...')
                solucao = busca.aEstrela(prob, heuristica)
                agente.coletandoEsfera = True
            elif len(focos) > 0:
                proximo = pontos.maisProximo(agente.estadoAtual.id, focos)
                focos.remove(proximo)
                prob = Problema((agente.estadoAtual.i, agente.estadoAtual.j), proximo, map)
                print('pensando...')
                solucao = busca.aEstrela(prob, heuristica)
    elif len(esferasColetadas) == NUM_ESFERAS and agente.estadoAtual != INICIO:
        if len(solucao) > 0:
            s = solucao.pop(0)
            if s.id != agente.estadoAtual.id:
                agente.atualizarEstado(s)
                agente.custoTotal += prob.criarEstado(s.id).custo


pygame.quit()

