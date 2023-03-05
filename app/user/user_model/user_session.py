from datetime import timedelta
from user.models import *
from prof_diagnostic.settings import SESSION_LIFETIME

class UserSession():
    def create_session(user: User):
        # tokens = UserHelpers.create_tokens(user=user)
        # print (tokens)
        response = {}
        timestamp = timezone.now()
        session = ActiveSession(user_id = user.id, expired = timestamp + timedelta(seconds=SESSION_LIFETIME), created_at=timestamp)
    
        if not ActiveSession.objects.filter(user_id = user.id):
            # session.save()
            response = {
                'status': 201,
                'message': 'success'
            }
        else:
            response = {
                'status': 208,
                'message': 'Already authorized'
            }
            # open_session = ActiveSession.objects.filter(user_id = user.id)[0]
            # open_session.delete()
            # session.save()

        return response

    def end_session():
        pass