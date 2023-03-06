# def main():
#     d = DiagnosticResult('dppsh', [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1])
#     d.count_competence_lvl()
#     print(d.competence_lvl)
#     print(list(d.competence_lvl.keys())[0])

class DiagnosticResult():
    def __init__(self, diagnostic_type: str, answers: list):
        self.diagnostic_type = diagnostic_type
        self.ansewrs = answers
        self.competence_lvl = {}

    def count_competence_lvl(self):
        if len(self.ansewrs) < 45:
            return {'Not end diagnostic'}
        competence_count = len(self.ansewrs) - self.ansewrs.count(0)
        if  competence_count in range(0, 10):
            self.competence_lvl= {1: 'ниже базового'}
        if competence_count in range (10, 21):
            self.competence_lvl= {2: 'базовый'}
        if competence_count in range (21, 45):
            self.competence_lvl= {3: 'достаточный'}
        if competence_count == 45:
            self.competence_lvl= {4: 'высокий'}

    def find_recomendations_dpo(self):
        pass
