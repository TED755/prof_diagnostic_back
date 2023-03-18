from datetime import datetime, timedelta
from user.models import *
from .user_helpers import *
from prof_diagnostic.settings import SESSION_LIFETIME, SECRET_KEY, JWT_ACCESS_TTL, JWT_REFRESH_TTL
import jwt

class UserSession():
    def create_session(user: User):
        # tokens = UserHelpers.create_tokens(user=user)
        # print (tokens)
        response = {}
        timestamp = timezone.now()
        session = ActiveSession(user_id = user.id, expired = timestamp + timedelta(seconds=SESSION_LIFETIME), 
                                created_at=timestamp)
    
        if not ActiveSession.objects.filter(user_id = user.id):
            session.save()
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

    def end_session(session_id: str):
        sessions = ActiveSession.objects.filter(id = session_id)
        if sessions:
            close_session = sessions[0]
            close_session.delete()
            return True

        return False

    def create_tokens(user: User):
        access_token = jwt.encode({
            'iss': 'backend-api',
            'exp': datetime.utcnow() + timedelta(seconds=JWT_ACCESS_TTL),
            'iat': datetime.utcnow(),
            'user_info': UserHelpers.user_info(user),
            'type': 'access'
        }, SECRET_KEY, algorithm='HS256')
        # print(access_token)
        # print(jwt.decode(access_token, SECRET_KEY, algorithms='HS256'))
        # print(access_token)
        # decoded = jwt.decode(access_token, key)
        # print(decoded)

        refresh_token = jwt.encode({
            'iss': 'backend-api',
            'exp': datetime.utcnow() + timedelta(seconds=JWT_REFRESH_TTL),#JWT_REFRESH_TTL,#
            'iat': datetime.utcnow(),
            'user_info': UserHelpers.user_info(user),
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
            print({'status': 403, 'message': 'Not valid token'})
            return {'status': 403, 'message': 'Not valid token'}
        except jwt.exceptions.ExpiredSignatureError:
            print({'status': 403, 'message': 'Signature has expired'})
            return {'status': 403, 'message': 'Signature has expired'}

        return token
