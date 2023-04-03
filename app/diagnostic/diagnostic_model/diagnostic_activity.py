from user.models import *
from user.models import Recomendation as user_rec
from diagnostic.models import *
from .diagnostic_result import *
from .diagnostic_helpers import *
import json

class DiagnosticActivity():
    def create_diagnostic(user: User, diagnostic_type: str):
        diagnostics = Diagnostic.objects.filter(user_id = user.id, diagnostic_type = diagnostic_type)
        if diagnostics:
            return {'status': 401, 'message': 'Diagnostic already exists'}
        
        diagnostic = Diagnostic(user_id =  user.id, 
            diagnostic_type = diagnostic_type if diagnostic_type else 'standard', 
            started = timezone.now())
        diagnostic.save()
        return {'status': 201, 'message': 'succes'}
    
    def save_progress(user_id: str, diagnostic_type: str, answers: list):
        diagnostics = Diagnostic.objects.filter(user_id = user_id, diagnostic_type = diagnostic_type)

        if not diagnostics:
            return {'status': 401, 'message':'Diagnotic not found'}

        diagnostic = diagnostics[0]

        if diagnostic.ended:
            return {'status': 200, 'message':'Diagnostic was ended yet'}

        diagnostic.answers = answers
        diagnostic.save()

        return {'status':201, 'message':'success'}


    def get_diagnostic(user_id: str, diagnostic_type: str):
        diagnostics = Diagnostic.objects.filter(user_id = user_id, diagnostic_type = diagnostic_type)

        if not diagnostics:
            return {'status': 401, 'message':'Diagnotic not found'}

        diagnostic = diagnostics[0]
        
        return {'status': 200, 'message':'Success', 'data':diagnostic.diagnostic_info()}

    def get_results(user_id: str, diagnostic_type='', answers=[]):
        user_recomendations = {}
        if not user_id:
            return {'status':400, 'message':'Invalid parameters given'}

        if not (diagnostic_type and answers):
            results = user_rec.objects.filter(user_id = user_id)
            if not results:
                return {'status': 425, 'message':'Diagnostic not ended'}
            user_recomendations = DiagnosticHelpers.generate_results(results_list=results)
            
            # print(user_recomendations)
            # for res in results:
            #     user_recomendations.append(res.recomendation_info())

            return {'status':200, 'data':user_recomendations}
            

        if len(answers) < 45:
            return {'status': 425, 'message':'Diagnostic not ended'}

        if diagnostic_type:
            results = user_rec.objects.filter(user_id = user_id, diagnostic_type = diagnostic_type)
        else:
            # results = user_rec.objects.filter(user_id = user_id)
            return {'status':400, 'message':'GET-request expected'}

        if not results:
            if not diagnostic_type:
                return {'status':401, 'message': 'Diagnostic type expected'}
            DiagnosticActivity.count_results(user_id = user_id, diagnostic_type=diagnostic_type, answers=answers)
            results = user_rec.objects.filter(user_id=user_id, diagnostic_type=diagnostic_type)

            if not results:
                return {'status':500, 'message':'Internal server error'}
                
        for res in results:
                user_recomendations.append(res.recomendation_info())
# data:{"competence_lvl":"", "standard":{}, "dppsh":{}}
        return {'status':200, 'data':user_recomendations}
            

    def count_results(user_id: str, diagnostic_type: str, answers: list):
        results = DiagnosticResult(user_id=user_id, diagnostic_type=diagnostic_type, answers=answers)
        results.count_competence_lvl()
        results.find_recomendations_dpo()


    def start_diagnostic(user_id: str):
        pass

    def load_recomendations(file_name: str):
        result = DiagnosticHelpers.load_recomendations_to_db(file_name=file_name)

    def get_questions(diagnostic_type: str):
        if not diagnostic_type:
            return {'status':401, 'message': 'Diagnostic type expected'}
        questions = DiagnosticHelpers.read_quetions(diagnostic_type=diagnostic_type)
        return {'status':200, 'data':questions}
        # print(questions)
        