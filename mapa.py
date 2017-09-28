import pygame
from interface import Cor

class Terreno:
    AGUA = 'A'
    GRAMA = 'G'
    MONTANHA = 'M'

class Mapa:

    def __init__(self, txt, alturaTile, larguraTile):
        """
        :param txt: Caminho para arquivo de texto contendo matriz que representa um mapa.
        """
        self.tiles = {}
        self.alturaTile = alturaTile
        self.larguraTile = larguraTile

        arquivo = open(txt, 'r')
        linhas  = arquivo.readlines()
        i = 0
        for linha in linhas:
            linha = linha.replace('\n', '') # Remove as quebras de linha
            j = 0
            for char in linha:
                self.tiles[j,i] = char
                j += 1
            i += 1

    def getTiles(self):
        return self.tiles

    def desenhar(self, tela):
        for key in self.tiles.keys():
            x = key[0]
            y = key[1]
            cor = Cor.PRETO
            if self.tiles[key] == Terreno.AGUA:
                cor = Cor.AZUL
            elif self.tiles[key] == Terreno.MONTANHA:
                cor = Cor.MARROM
            elif self.tiles[key] == Terreno.GRAMA:
                cor = Cor.VERDE
            pygame.draw.rect(tela, cor, [x*self.larguraTile, y*self.alturaTile, self.larguraTile, self.alturaTile])
