from user.models import *
from user.models import Recomendation as user_rec
from diagnostic.models import *
from .diagnostic_result import *
from .diagnostic_helpers import *
# import json
from datetime import datetime

class DiagnosticActivity():
    def create_diagnostic(user: User, diagnostic_type: str):
        diagnostics = Diagnostic.objects.filter(user_id = user.id, diagnostic_type = diagnostic_type)
        if diagnostics:
            return {'status': 400, 'message': 'Diagnostic already exists'}
        
        diagnostic = Diagnostic(user_id =  user.id, 
            diagnostic_type = diagnostic_type if diagnostic_type else 'standard', 
            started = timezone.now())
        diagnostic.save()
        return {'status': 201, 'message': 'succes'}
    
    def save_progress(user_id: str, diagnostic_type: str, answers: list):
        diagnostics = Diagnostic.objects.filter(user_id = user_id, diagnostic_type = diagnostic_type)

        if not diagnostics:
            return {'status': 404, 'message':'Diagnotic not found'}

        diagnostic = diagnostics[0]

        if diagnostic.ended:
            return {'status': 201, 'message':'Diagnostic was ended yet'}

        diagnostic.answers = answers
        diagnostic.save()

        return {'status':201, 'message':'success'}

    def get_progress(user_id: str, diagnostic_type: str):
        progress = Diagnostic.objects.filter(user_id=user_id, diagnostic_type=diagnostic_type)
        if not progress:
            return {'status': 404, 'message':'No user progress'}

        
        _progress = progress[0]
        return {'status':200, 'data':_progress.answers}


    def get_diagnostic(user_id: str, diagnostic_type: str):
        diagnostics = Diagnostic.objects.filter(user_id = user_id, diagnostic_type = diagnostic_type)

        if not diagnostics:
            return {'status': 404, 'message':'Diagnotic not found'}

        diagnostic = diagnostics[0]
        
        return {'status': 200, 'message':'Success', 'data':diagnostic.diagnostic_info()}

    def get_results(user_id: str, diagnostic_type='', answers=[]):
        user_recomendations = {}
        if not user_id:
            return {'status':400, 'message':'Invalid parameters given'}

        if not (diagnostic_type and answers):
            results = user_rec.objects.filter(user_id = user_id)
            if not results:
                # return {'status': 400, 'message':'Diagnostic not ended'}
                user_recomendations = DiagnosticHelpers.generate_results(results_list=results)
                return {'status':200, 'data':user_recomendations}
            

        if len(answers) < 45:
            return {'status': 400, 'message':'Diagnostic not ended'}

        if diagnostic_type:
            results = user_rec.objects.filter(user_id = user_id, diagnostic_type = diagnostic_type)
        else:
            # results = user_rec.objects.filter(user_id = user_id)
            return {'status':400, 'message':'GET-request expected'}

        if not results:
            if not diagnostic_type:
                return {'status':400, 'message': 'Diagnostic type expected'}
            DiagnosticActivity.end_diagnostic(user_id=user_id, diagnostic_type=diagnostic_type, answers=answers)
            # DiagnosticActivity.save_progress(user_id=user_id, diagnostic_type=diagnostic_type, answers=answers)
            # DiagnosticActivity.count_results(user_id = user_id, diagnostic_type=diagnostic_type, answers=answers)
            results = user_rec.objects.filter(user_id=user_id, diagnostic_type=diagnostic_type)

            if not results:
                return {'status':500, 'message':'Internal server error'}

        user_recomendations = DiagnosticHelpers.generate_results(results_list=results)

        return {'status':200, 'data':user_recomendations}
            
    def end_diagnostic(user_id:str, diagnostic_type:str, answers:list):
        DiagnosticActivity.save_progress(user_id=user_id, diagnostic_type=diagnostic_type, answers=answers)
        DiagnosticActivity.count_results(user_id=user_id, diagnostic_type=diagnostic_type, answers=answers)
        DiagnosticActivity.set_timestamp(user_id=user_id, diagnostic_type=diagnostic_type, answers=answers)

    def count_results(user_id: str, diagnostic_type: str, answers: list):
        results = DiagnosticResult(user_id=user_id, diagnostic_type=diagnostic_type, answers=answers)
        results.count_competence_lvl()
        results.find_recomendations_dpo()

    def set_timestamp(user_id:str, diagnostic_type:str, answers:list):
        diagnostics = Diagnostic.objects.filter(user_id = user_id, diagnostic_type = diagnostic_type)

        timestamp = datetime.utcnow()
        if not diagnostics:
            return {'status': 404, 'message':'Diagnotic not found'}

        diagnostic = diagnostics[0]

        if diagnostic.ended:
            return {'status': 201, 'message':'Diagnostic was ended yet'}

        diagnostic.ended = timestamp
        diagnostic.save()

        return {'status':200, 'message':'success'}

    def start_diagnostic(user_id: str):
        pass

    def load_recomendations(file_name: str):
        result = DiagnosticHelpers.load_recomendations_to_db(file_name=file_name)

    def get_questions(diagnostic_type: str):
        if not diagnostic_type:
            return {'status':400, 'message': 'Diagnostic type expected'}
        questions = DiagnosticHelpers.read_quetions(diagnostic_type=diagnostic_type)
        return {'status':200, 'data':questions}
        