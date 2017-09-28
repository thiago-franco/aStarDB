class Goku:

    def __init__(self, problema, alcanceRadar = 3):
        self.estadoAtual = problema.estadoInicial
        self.alcanceRadar = alcanceRadar
        self.esferasColetadas = 0
        self.coletandoEsfera = False
        self.custoTotal = 0

    def atualizarEstado(self, novoEstado):
        self.estadoAtual = novoEstado

    def radar(self, mapaEsferas):
        """
        Identifica as esferas dentro do alcance do agente.
        :param mapaEsferas: mapa contendo a posição de todas as esferas.
        :return: esferas visiveis para o atual estado do agente.
        """
        intervaloI = range(self.estadoAtual.i-self.alcanceRadar, self.estadoAtual.i+self.alcanceRadar+1)
        intervaloJ = range(self.estadoAtual.j-self.alcanceRadar, self.estadoAtual.j+self.alcanceRadar+1)
        esferasVisiveis = []
        for esfera in mapaEsferas:
            if esfera[0] in intervaloI and esfera[1] in intervaloJ:
                esferasVisiveis.append(esfera)
        return esferasVisiveis

    def coletarEsfera(self):
        self.esferasColetadas += 1