import time
from personagemView import PersonagemView
from personagem import Personagem
from exceptions import CadastroInvalidoException, ItemIndisponivelException, OperacaoNaoPermitidaException


class PersonagemController:
    def __init__(self):
        self.__personagens = []
        self.__personagemView = PersonagemView()

    @property
    def personagens(self):
        return self.__personagens

    def pega_personagem_por_nome(self, nome: str):
        for personagem in self.__personagens:
            if personagem.nome == nome:
                return personagem
        return None

    def cadastrar_personagem(self, nome, nivel=1, experiencia_total=0, pontos_disponiveis=10, nome_classe="", exibir_mensagem=True):
        try:
            if self.pega_personagem_por_nome(nome) is not None:
                raise CadastroInvalidoException(entidade="Personagem", campo="nome")
            
            personagem = Personagem(
                nome=nome,
                nivel=nivel,
                experiencia_total=experiencia_total,
                pontos_disponiveis=pontos_disponiveis,
                nome_classe=nome_classe
            )

            self.__personagens.append(personagem)
            if exibir_mensagem:
                self.__personagemView.mostrar_mensagem(
                    f"Personagem {nome} da classe {nome_classe} criado com sucesso! Nível: {nivel}, Experiência: {experiencia_total}"
                )
            time.sleep(1)
            return personagem
        except CadastroInvalidoException as e:
            self.__personagemView.mostrar_mensagem(str(e))

    def calcular_nivel(self, experiencia_total):
        nivel = 1
        experiencia_para_proximo = 100

        while experiencia_total >= experiencia_para_proximo:
            nivel += 1
            experiencia_total -= experiencia_para_proximo
            experiencia_para_proximo = 100 + (nivel * 10)

        return nivel

    def experiencia_para_proximo_nivel(self, personagem: Personagem):
        nivel_atual = self.calcular_nivel(personagem.experiencia_total)
        return 100 + (nivel_atual * 10)

    def ganhar_experiencia(self, personagem: Personagem, experiencia_ganha: int):
        nivel_anterior = self.calcular_nivel(personagem.experiencia_total)
        personagem.experiencia_total += experiencia_ganha
        novo_nivel = self.calcular_nivel(personagem.experiencia_total)

        if novo_nivel > nivel_anterior:
            aumento_niveis = novo_nivel - nivel_anterior
            personagem.pontos_disponiveis += aumento_niveis * 5
            personagem.nivel = novo_nivel

            self.__personagemView.mostrar_mensagem(
                f"{personagem.nome} upou para o nível {novo_nivel}! Pontos disponíveis: {personagem.pontos_disponiveis}"
            )

        self.__personagemView.mostrar_mensagem(
            f"{personagem.nome} ganhou {experiencia_ganha} XP! Experiência total: {personagem.experiencia_total}"
        )
        self.__personagemView.mostrar_mensagem(
            f"XP para próximo nível: {self.experiencia_para_proximo_nivel(personagem)}"
        )

    def mostrar_status(self, personagem: Personagem):
        try:
            status = {
                'nome': personagem.nome,
                'nivel': personagem.nivel,
                'experiencia_total': personagem.experiencia_total,
                'experiencia_para_proximo_nivel': self.experiencia_para_proximo_nivel(personagem),
                'pontos_disponiveis': personagem.pontos_disponiveis,
                'ataque': personagem.classe_personagem.atributos['ataque'],
                'defesa': personagem.classe_personagem.atributos['defesa'],
                'hp': personagem.classe_personagem.atributos['hp'],
                'estamina': personagem.classe_personagem.atributos['estamina'],
                'pocoes_hp': personagem.pocao_hp.quant,
                'pocoes_est': personagem.pocao_est.quant
            }
            self.__personagemView.mostrar_status(status)
        except KeyError as e:
            raise OperacaoNaoPermitidaException(operacao="Mostrar status") from e

    def upar_atributos(self, personagem: Personagem):
        try:
            if personagem.pontos_disponiveis > 0:
                atributo_escolhido = self.__personagemView.escolher_atributo()
                pontos = self.__personagemView.pega_quantidade_pontos()
                if pontos <= personagem.pontos_disponiveis:
                    if atributo_escolhido in personagem.classe_personagem.atributos:
                        personagem.classe_personagem.atributos[atributo_escolhido] += pontos
                        personagem.pontos_disponiveis -= pontos
                        self.__personagemView.mostrar_mensagem(f"Atributo {atributo_escolhido} aumentado em {pontos} pontos!")
                    else:
                        raise CadastroInvalidoException(entidade="Personagem", campo=atributo_escolhido)
                else:
                    raise OperacaoNaoPermitidaException(operacao="Distribuir pontos de atributos")
            else:
                self.__personagemView.mostrar_mensagem("Você não tem pontos disponíveis para distribuir.")
        except CadastroInvalidoException as e:
            self.__personagemView.mostrar_mensagem(str(e))

    def usar_item(self, personagem: Personagem):
        try:
            tipo_item = self.__personagemView.escolher_item()
            if tipo_item == 1 and personagem.pocao_hp and personagem.pocao_hp.quant > 0:
                personagem.classe_personagem.atributos['hp'] += personagem.pocao_hp.valor
                personagem.pocao_hp.quant -= 1
                self.__personagemView.mostrar_mensagem(f"{personagem.nome} usou Poção de HP!")
            elif tipo_item == 2 and personagem.pocao_est and personagem.pocao_est.quant > 0:
                personagem.classe_personagem.atributos['estamina'] += personagem.pocao_est.valor
                personagem.pocao_est.quant -= 1
                self.__personagemView.mostrar_mensagem(f"{personagem.nome} usou Poção de Estamina!")
            else:
                raise ItemIndisponivelException(item="Poção")
        except ItemIndisponivelException as e:
            self.__personagemView.mostrar_mensagem(str(e))

    def usar_habilidade(self, classe_personagem: Personagem):
        #colocar a logica em que o jogador escolhe qual habilidade ele quer usar,
        #podendo escolher entre 3 habilidades, que tem efeitos diferentes no inimigo.
        pass

    