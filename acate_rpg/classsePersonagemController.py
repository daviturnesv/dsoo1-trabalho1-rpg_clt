from classePersonagem import ClassePersonagem

class ClassePersonagemController():
    def __init__(self):
        self.modificadores_classe = {
            "Estagiario": {"ataque": 20, "defesa": 20, "hp": 30, "estamina": 10},
            "CLT": {"ataque": 40, "defesa": 40, "hp": 100, "estamina": 40}
        }

    def definir_atributos_iniciais(self, classe_personagem: ClassePersonagem):
        modificador = self.modificadores_classe.get(classe_personagem.nome_classe)

        if modificador:
            atributos = classe_personagem.atributos
            try:
                atributos['ataque'] += modificador['ataque']
                atributos['defesa'] += modificador['defesa']
                atributos['hp'] += modificador['hp']
                atributos['estamina'] += modificador['estamina']
                classe_personagem.atributos = atributos

            except KeyError as e:
                raise ValueError(f"Atributo inválido ao definir atributos iniciais: {e}")
        else:
            raise ValueError(f"Classe {classe_personagem.nome_classe} não tem modificador definido.")