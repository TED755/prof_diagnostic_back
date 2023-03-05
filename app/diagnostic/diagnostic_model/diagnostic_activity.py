from user.models import *
from diagnostic.models import *
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
        
    def get_diagnostic(user_id: str, diagnostic_type: str):
        pass