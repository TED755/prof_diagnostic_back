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

    def get_results(user_id: str, diagnostic_type: str, answers: list):
        # answers=[0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1]
        if not (user_id and answers):
            return {'status':401, 'message':'Invalid parameters given'}

        if len(answers) < 45:
            return {'status': 401, 'message':'Diagnostic not ended'}

        if not diagnostic_type:
            results = user_rec.objects.filter(user_id = user_id)
            # return response
        else:
            results = user_rec.objects.filter(user_id = user_id, diagnostic_type = diagnostic_type)

        if results:
            result = results[0]
            # return response
        else:
            if not diagnostic_type:
                return {'status':401, 'message': 'Diagnostic type expected'}
            DiagnosticActivity.count_results(user_id = user_id, diagnostic_type=diagnostic_type, answers=answers)
            results = user_rec.objects.filter(user_id=user_id, diagnostic_type=diagnostic_type)
            for res in results:
                print(res.recomendation_info())
            # return response
        
        return {'status':200}
            

    def count_results(user_id: str, diagnostic_type: str, answers: list):
        results = DiagnosticResult(user_id=user_id, diagnostic_type=diagnostic_type, answers=answers)
        results.count_competence_lvl()
        results.find_recomendations_dpo()

        # print(results.recomendations)


    def start_diagnostic(user_id: str):
        pass

    def load_recomendations(file_name: str):
        result = DiagnosticHelpers.load_recomendations_to_db(file_name=file_name)