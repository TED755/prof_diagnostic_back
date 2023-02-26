from datetime import datetime
from user.models import *
from .user_helpers import UserHelpers

class UserSession():
    def create_session(user: User)->ActiveSession:
        tokens = UserHelpers.create_tokens(user=user)
        # print (tokens)

        session = ActiveSession(user_id = user.id, access_token=tokens['access'], 
            refresh_token=tokens['refresh'], started_at=datetime.utcnow())
        
        if not ActiveSession.objects.filter(user_id = user.id):
            session.save()
        return session

    def end_session():
        pass