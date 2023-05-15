from datetime import datetime, timedelta
from django.utils import timezone
from user.models import *
from .user_helpers import *
from prof_diagnostic.settings import SECRET_KEY, JWT_ACCESS_TTL, JWT_REFRESH_TTL
import jwt

class UserSession():
    def create_session(user: User):
        timestamp = datetime.utcnow()
        # print(f"timestamp: {timestamp}")
        # return {}
        _expired = timestamp + timedelta(seconds=JWT_ACCESS_TTL)
        # print(_expired)
        
        sessions = ActiveSession.objects.filter(user_id = user.id)
        if sessions:
            session = sessions[0]
            UserSession.end_session(session_id=session.id)

        tokens = UserSession.create_tokens(user=user, timestamp=timestamp)
        timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        _expired = _expired.strftime("%Y-%m-%d %H:%M:%S")

        session = ActiveSession(user_id = user.id, expired_at = _expired, 
                            created_at=timestamp)
        # print(session.created_at)
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
            close_session.is_expired = True
            close_session.save()
            # close_session.delete()
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
        return {'status':201, 'message':'success', 'data':sessions[0]}
    
    def get_active_session_by_user_id(user_id: str, created_at:datetime = None):
        if created_at:
            # sessions = ActiveSession.objects.filter(user_id=user_id, is_expired=False, created_at=created_at)
            sessions = ActiveSession.objects.filter(user_id=user_id, created_at=created_at)
        else:
            sessions = ActiveSession.objects.filter(user_id=user_id, is_expired=False)
        if not sessions:
            return {'status':401, 'messsage': 'Active sessions not found'}
        return {'status':201, 'message':'success', 'data':sessions[0]}
    
    def session_expired(token:str):
        user_id = token['user_info']['user_id']
        # session = UserSession.get_session_by_user_id(user_id=user_id)
        session = UserSession.get_active_session_by_user_id(user_id=user_id, 
                                                            created_at=datetime.fromtimestamp(token['iat']))
        # print(session['data'].id)
        
        if 'status' not in session:
            return {'status':500, 'message':'Internal server error'}
        elif session['status'] == 401:
            return session
        
        _session = session['data']

        # print(datetime.timestamp(datetime.utcnow()))
        # print(f"Expired: {_session.is_expired}")

        if _session.is_expired:
            return {'status':401, 'message': 'Session expired', 'data':{'expired': True, 'session_id':_session.id}}
        _timedelta = datetime.timestamp(datetime.utcnow()) - datetime.timestamp(_session.expired_at) 
        # print(_timedelta)
        if _timedelta > 0:
            # print('AAAAAAAAAAAbnavlyay')
            return {'status':401, 'message': 'Session expired', 'data':{'expired': True, 'session_id':_session.id}}

        created_at = int(datetime.timestamp(_session.created_at))
        # print(f"Token {datetime.fromtimestamp(refresh_token['iat'])}")
        # print(f"Token {refresh_token['iat']}")
        # print(f"Token exp {datetime.fromtimestamp(refresh_token['exp'])}")
        # print(f"Session created_at {int(datetime.timestamp(_session.created_at))}")
        # print(f"Session exp {int(datetime.timestamp(_session.expired))}")
        # if refresh_token['iat'] == _session.created_at:
        # if refresh_token['iat'] != int(datetime.timestamp(_session.created_at)):
        # print(f"Token: {refresh_token['iat']}")
        # print(f"Session: {created_at}")
        # print(created_at != refresh_token['iat'])
        if created_at != token['iat']:
            return {'status':401, 'message': 'Session expired', 'data':{'expired': True, 'session_id':_session.id}}
        else:
            return {'status':201, 'message': 'Session not expired', 'data':False}
        
    def end_session_if_not_active(token:str):
        session_expired = UserSession.session_expired(token=token)
        print(f"Session info: {session_expired}") #For logging
        if 'data' in session_expired:
            if session_expired['data']:
                if UserSession.end_session(session_expired['data']['session_id']):
                    return True
        else:
            return True
        return False