from datetime import datetime, timedelta
from user.models import *
from .user_helpers import *
from prof_diagnostic.settings import SECRET_KEY, JWT_ACCESS_TTL, JWT_REFRESH_TTL
import jwt

class UserSession():
    def create_session(user: User):
        timestamp = datetime.utcnow()
        _expired = timestamp + timedelta(seconds=JWT_ACCESS_TTL)
        
        sessions = ActiveSession.objects.filter(user_id = user.id)
        if sessions:
            session = sessions[0]
            UserSession.end_session(session_id=session.id)

        
        tokens = UserSession.create_tokens(user=user, timestamp=timestamp)
        session = ActiveSession(user_id = user.id, expired = _expired, 
                            created_at=timestamp)
        session.save()

        response = {
                'status': 201,
                'message': 'success',
                'tokens': tokens
        }
        return response

    def end_session(session_id: str):
        sessions = ActiveSession.objects.filter(id = session_id)
        if sessions:
            close_session = sessions[0]
            close_session.delete()
            return True

        return False

    def create_tokens(user: User, timestamp):

        access_token = jwt.encode({
            'iss': 'backend-api',
            'exp': timestamp + timedelta(seconds=JWT_ACCESS_TTL),
            'iat': timestamp,
            'user_info': user.user_info(),
            'isDiagnosticCompleted': '',
            'type': 'access'
        }, SECRET_KEY, algorithm='HS256')

        refresh_token = jwt.encode({
            'iss': 'backend-api',
            'exp': timestamp + timedelta(seconds=JWT_REFRESH_TTL),
            'iat': timestamp,
            'user_info': user.user_info(),
            'isDiagnosticCompleted': '',
            'type': 'refresh'
        }, SECRET_KEY, algorithm='HS256')

        # print(refresh_token)
        # print(jwt.decode(refresh_token, SECRET_KEY, algorithms='HS256'))
    
        return {
            'access': access_token,
            'refresh': refresh_token
        }

    def decode_token(token: str):
        try:
            token = jwt.decode(str(token), SECRET_KEY, algorithms=["HS256"])
        except jwt.InvalidSignatureError:
            return {'status': 401, 'message': 'Not valid token'}
        except jwt.exceptions.ExpiredSignatureError:
            return {'status': 401, 'message': 'Signature has expired'}

        return token
    
    def get_session_by_user_id(user_id: str):
        sessions = ActiveSession.objects.filter(user_id=user_id)
        if not sessions:
            return {'status':401, 'messsage': 'Session not found'}
        return sessions[0]
