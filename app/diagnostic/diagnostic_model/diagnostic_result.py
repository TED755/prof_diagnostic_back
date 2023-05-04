from diagnostic.models import Recomendation as rec
from user.models import Recomendation as user_rec
from diagnostic.diagnostic_model.diagnostic_helpers import DiagnosticHelpers

class DiagnosticResult():
    def __init__(self, user_id: str, diagnostic_type: str, answers: list):
        if len(answers) < 45:
            return {'Not end diagnostic'}
        self.user_id = user_id
        self.diagnostic_type = diagnostic_type
        self.answers = answers
        self.competence_lvl = ''
        self.recomendations = []

    def count_competence_lvl(self):
        competence_count = len(self.answers) - self.answers.count(0)
        if  competence_count in range(0, 10):
            self.competence_lvl = 'ниже базового'
        if competence_count in range (10, 21):
            self.competence_lvl = 'базовый'
        if competence_count in range (21, 45):
            self.competence_lvl = 'достаточный'
        if competence_count == 45:
            self.competence_lvl = 'высокий'

    def get_competence_lvl(self):
        competence_count = len(self.answers) - self.answers.count(0)
        if  competence_count in range(0, 10):
            return 1
        if competence_count in range (10, 21):
            return 2
        if competence_count in range (21, 45):
            return 3
        if competence_count == 45:
            return 4

    def find_recomendations_dpo(self):
        # recomendations = rec.objects.filter(diagnostic_type=self.diagnostic_type).order_by('id')
        recomendations = DiagnosticHelpers.read_recomendations(diagnostic_type=self.diagnostic_type)
        
        if not recomendations:
            return {'status': 500, 'message':'Internal server error. Recomendations reading failed'}

        user_recomendation = ''
        growpoint = ''
        
        for index, answer in enumerate(self.answers):
            if answer == 0:
                recomendation = recomendations[index]

                if self.get_competence_lvl() == 1:
                    user_recomendation = recomendation.level_1
                elif self.get_competence_lvl() == 2:
                    user_recomendation = recomendation.level_2
                elif self.get_competence_lvl() == 3:
                    user_recomendation = recomendation.level_3

                if recomendation.competence_lvl < self.get_competence_lvl():
                    growpoint = 'Дефицит'
                else:
                    growpoint = 'Перспектива'

                user_rec(user_id=self.user_id, diagnostic_type=self.diagnostic_type, 
                    index=index + 1, competence_lvl=self.competence_lvl, 
                    recomendation=user_recomendation, growpoint=growpoint).save()     
