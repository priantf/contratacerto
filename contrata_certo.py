from experta import *

# https://www.transfermarkt.pt/santos/profil/spieler/140811
# https://www.lance.com.br/brasileirao/footstats-monta-selecao-estatistica-campeonato-brasileiro-2018.html

contrato = "SIM"

class Jogador(Fact):
    pass

class Contratacao(KnowledgeEngine):

    @Rule()
    def startup(self):
        self.declare(Jogador(nome=input("Qual é o nome do atleta? ").lower()))
        self.declare(Jogador(valor_contratacao=float(input("Quanto custa a contrataçao do jogador? "))))
        self.declare(Jogador(titulos_carreira=int(input("Quantos titulos na carreira? "))))
        self.declare(Jogador(imc=float(input("Qual valor do IMC do atleta? "))))
        self.declare(Jogador(qtd_lesoes=int(input("Quantas lesoes graves esse jogador já teve? "))))
        self.declare(Jogador(idade=int(input("Qual idade do jogador? "))))
        self.declare(Jogador(posicao=input("Qual posicao? ").lower()))
        print("Na última temporada:")

    @Rule(OR(Jogador(nome="deyverson"),
        Jogador(idade = P(lambda idade: idade > 30)),
        Jogador(idade = P(lambda idade: idade < 22)),
        Jogador(imc = P(lambda imc: imc < 22)),
        Jogador(imc = P(lambda imc: imc > 25)),
        Jogador(titulos_carreira = P(lambda titulos_carreira: titulos_carreira < 4)),
        Jogador(qtd_lesoes = P(lambda qtd_lesoes: qtd_lesoes > 2))),
        AND(Jogador(valor_contratacao = P(lambda valor_contratacao: valor_contratacao > 10000000))))
    def contrata_geral(self):
        global contrato
        contrato = "NAO"

    @Rule(Jogador(posicao="goleiro"))
    def goleiro(self):
        defesas_dificeis=int(input("Qntd. defesas dificeis: "))
        gols_tomados=int(input("Qntd. gols tomados: "))
        self.declare(Jogador(finalizacao_gol_sofrido=float(input("Nº de finalizaçoes para sofrer um gol: "))))
        self.declare(Jogador(media_gol_defesa=defesas_dificeis/gols_tomados))
        
    @Rule(OR(Jogador(finalizacao_gol_sofrido = P(lambda finalizacao_gol_sofrido: finalizacao_gol_sofrido < 3)),
          Jogador(media_gol_defesa = P(lambda media_gol_defesa: media_gol_defesa < 1.5))))
    def goleiro_contrata(self):
        global contrato
        contrato = "NAO"

    @Rule(Jogador(posicao="zagueiro"))
    def zagueiro(self):
        jogos = int(input("Numero de jogos: "))
        amarelos = int(input("Numero de cartões amarelos: "))
        vermelhos = int(input("Numero de cartões vermelhos: "))
        self.declare(Jogador(vermelhos = vermelhos))
        self.declare(Jogador(media_amarelos = amarelos / jogos))

    @Rule(OR(Jogador(vermelhos = P(lambda vermelhos: vermelhos > 2)),
             Jogador(media_amarelos = P(lambda media_amarelos: media_amarelos > 0.8))))
    def zagueiro_contrata(self):
        global contrato
        contrato = "NAO"

    @Rule(Jogador(posicao="lateral"))
    def lateral(self):
        jogos = int(input("Numero de jogos: "))
        desarmes = int(input("Numero de desarmes: "))
        assitencias = int(input("Qutd. de assitencias: "))
        passes_errados = int(input("Qutd. de passes errados: "))

        self.declare(Jogador(media_desarmes = desarmes / jogos))
        self.declare(Jogador(media_assitencias = assitencias / jogos))
        self.declare(Jogador(passes_errados = passes_errados))

    @Rule(OR(Jogador(media_desarmes = P(lambda media_desarmes: media_desarmes < 1.3)),
             Jogador(media_assitencias = P(lambda media_assitencias: media_assitencias < 0.17)),
             Jogador(passes_errados = P(lambda passes_errados: passes_errados > 55))))
    def lateral_contrata(self):
        global contrato
        contrato = "NAO"

    @Rule(Jogador(posicao="volante"))
    def volante(self):
        jogos = int(input("Numero de jogos: "))
        passes_errados = int(input("Qutd. de passes errados: "))
        faltas = int(input("Numero de faltas: "))
        desarmes = int(input("Numero de desarmes: "))

        self.declare(Jogador(passes_errados = passes_errados))
        self.declare(Jogador(media_faltas = faltas / jogos))
        self.declare(Jogador(media_desarme = desarmes / jogos))

    @Rule(OR(Jogador(media_interceptacao = P(lambda media_interceptacao: media_interceptacao < 0.5)),
             Jogador(media_faltas = P(lambda media_faltas: media_faltas > 3)),
             Jogador(passes_errados = P(lambda passes_errados: passes_errados > 55))))
    def volante_contrata(self):
        global contrato
        contrato = "NAO"

    @Rule(Jogador(posicao="meio-campo"))
    def meia(self):
        jogos = int(input("Numero de jogos: "))
        gols = int(input("Numero de gols: "))
        assistencias = int(input("Numero de assistencias: "))

        self.declare(Jogador(media_gol = gols / jogos))
        self.declare(Jogador(media_assistencia = assistencias / jogos))

    @Rule(OR(Jogador(media_gol = P(lambda media_gol: media_gol < 0.2)),
             Jogador(media_finalizacao = P(lambda media_assistencia:  media_assistencia < 0.4))))
    def contrata_meia(self):
        global contrato
        contrato = "NAO"

    @Rule(Jogador(posicao="atacante"))
    def atacante(self):
        jogos = int(input("Numero de jogos: "))
        gols = int(input("Numero de gols: "))
        assistencias = int(input("Numero de assistencias: "))

        self.declare(Jogador(media_gol = gols / jogos))
        self.declare(Jogador(media_assistencia = assistencias / jogos))
        
    @Rule(OR(Jogador(media_gol = P(lambda media_gol: media_gol < 0.4)),
             Jogador(media_finalizacao = P(lambda media_assistencia:  media_assistencia < 0.5))))
    def atacante_contrata(self):
        global contrato
        contrato = "NAO"
        
    def fim(self):
        if contrato == "NAO":
            print("Nao contrata!!!!!!!!!")
        elif contrato == "SIM":
            print("Eu contrataria")

x = Contratacao()
x.reset()
x.run()
x.fim()
