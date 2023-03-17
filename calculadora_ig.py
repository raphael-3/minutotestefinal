from datetime import datetime, timedelta

class IdadeGestacional:
    def __init__(self, data_ultima_menstruacao, data_ultrassom, idade_gestacional_ultrassom):
        self.data_ultima_menstruacao = data_ultima_menstruacao
        self.data_ultrassom = data_ultrassom
        self.idade_gestacional_ultrassom = idade_gestacional_ultrassom

    def calcular_idade_gestacional_pela_dum(self):
        hoje = datetime.today().date()
        data_parto = self.data_ultima_menstruacao + timedelta(days=280)
        idade_gestacional = (hoje - self.data_ultima_menstruacao).days
        semanas_dum, dias_dum = divmod(idade_gestacional, 7)
        int(semanas_dum), int(dias_dum)
        return f"{semanas_dum} semanas e {dias_dum} dias", semanas_dum, dias_dum, data_parto.strftime("%d/%m/%Y")

    def calcular_idade_gestacional_pelo_ultrassom(self):
        hoje = datetime.today().date()
        idade_gestacional = (hoje - self.data_ultrassom).days + self.idade_gestacional_ultrassom
        semanas_usg, dias_usg = divmod(idade_gestacional, 7)
        int(semanas_usg), int(dias_usg)
        data_parto = self.data_ultrassom + timedelta(days=280 - self.idade_gestacional_ultrassom)
        return f"{semanas_usg} semanas e {dias_usg} dias", semanas_usg, dias_usg, data_parto.strftime("%d/%m/%Y")

    def qual_ig_usar(self):
        idade_calculada_pelo_usg, semanas_usg, dias_usg, data_parto_usg = self.calcular_idade_gestacional_pelo_ultrassom()
        idade_calculada_pela_dum, semanas_dum, dias_dum, data_parto_dum = self.calcular_idade_gestacional_pela_dum()
        delta_ig = abs((semanas_usg*7 + dias_usg) - (dias_dum + semanas_dum*7))
        if self.idade_gestacional_ultrassom < 9*7:
            if delta_ig > 5:
                outra_ig = idade_calculada_pela_dum
                idade_final = idade_calculada_pelo_usg
                return "USG", idade_final, outra_ig, "DUM"
            else:
                outra_ig = idade_calculada_pelo_usg
                idade_final = idade_calculada_pela_dum
                return "DUM", idade_final, outra_ig, "USG"
        elif self.idade_gestacional_ultrassom < 14*7:
            if delta_ig > 7:
                outra_ig = idade_calculada_pela_dum
                idade_final = idade_calculada_pelo_usg
                return "USG", idade_final, outra_ig, "DUM"
            else:
                outra_ig = idade_calculada_pelo_usg
                idade_final = idade_calculada_pela_dum
                return "DUM", idade_final, outra_ig, "USG"
        elif self.idade_gestacional_ultrassom < 16*7:
            if delta_ig > 10:
                outra_ig = idade_calculada_pela_dum
                idade_final = idade_calculada_pelo_usg
                return "USG", idade_final, outra_ig, "DUM"
            else:
                outra_ig = idade_calculada_pelo_usg
                idade_final = idade_calculada_pela_dum
                return "DUM", idade_final, outra_ig, "USG"
        elif self.idade_gestacional_ultrassom < 22*7:
            if delta_ig > 14:
                outra_ig = idade_calculada_pela_dum
                idade_final = idade_calculada_pelo_usg
                return "USG", idade_final, outra_ig, "DUM"
            else:
                outra_ig = idade_calculada_pelo_usg
                idade_final = idade_calculada_pela_dum
                return "DUM", idade_final, outra_ig, "USG"
        else:
            if delta_ig > 21:
                outra_ig = idade_calculada_pela_dum
                idade_final = idade_calculada_pelo_usg
                return "USG", idade_final, outra_ig, "DUM"
            else:
                outra_ig = idade_calculada_pelo_usg
                idade_final = idade_calculada_pela_dum
                return "DUM", idade_final, outra_ig, "USG"

# ###  Exemplo de uso: ###
# # Exemplo de uso da classe IdadeGestacional
# dum = datetime(2023, 1, 30).date()  # data da última menstruação
# ultrassom = datetime(2023, 2, 1).date()  # data do primeiro ultrassom
# idade_gestacional_ultrassom = 4*7  # idade gestacional na data do ultrassom (em dias)
#
# # criando uma instância da classe com a data da última menstruação
# ig = IdadeGestacional(dum, ultrassom, idade_gestacional_ultrassom)
#
# # calculando a idade gestacional com base na DUM
# idade_gestacional, semanas_dum, dias_dum, data_parto = ig.calcular_idade_gestacional_pela_dum()
# print(f"Idade gestacional pela DUM: {idade_gestacional}. Data prevista para o parto: {data_parto}.")
#
# # calculando a idade gestacional com base no primeiro ultrassom
# idade_gestacional, semanas_usg, dias_usg, data_parto = ig.calcular_idade_gestacional_pelo_ultrassom()
# print(f"Idade gestacional pelo ultrassom: {idade_gestacional}. Data prevista para o parto: {data_parto}.")
#
# #Vendo qual método utilizar:
# metodo, idade_final, outra_ig, outro_metodo = ig.qual_ig_usar()
# print(f"Utilizar IG({metodo}): {idade_final} / IG({outro_metodo}): {outra_ig}")