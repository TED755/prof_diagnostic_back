from user.models import *
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

    def get_results(user_id: str, diagnostic_type: str, data: json):
        results = DiagnosticResult(diagnostic_type=diagnostic_type, answers=[0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1])
        results.count_competence_lvl()
        results.find_recomendations_dpo()

    def start_diagnostic(user_id: str):
        pass

    def load_recomendations(file_name: str):
        result = DiagnosticHelpers.load_recomendations_to_db(file_name=file_name)