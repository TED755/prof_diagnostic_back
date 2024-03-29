from user.models import *
from diagnostic.models import *
from .user_helpers import UserHelpers
from .user_session import UserSession
from diagnostic.diagnostic_model.diagnostic_activity import DiagnosticActivity
from prof_diagnostic.settings import JWT_ACCESS_TTL, JWT_REFRESH_TTL
from datetime import datetime, timedelta
import json
import jwt

class UserActivity():
    def login(data: json) -> hash:
        _users = UserHelpers.find_user_by_email(data.get('email'))
        if not _users:
            return {'status':401, 'message':'Invalid email or password'}

        _user = _users[0]
        if not UserHelpers.check_password(_user, data.get('password')):
            return {'status':401, 'message':'Invalid email or password'}
        
        session = UserSession.get_active_session_by_user_id(user_id=_user.id)

        if session['status'] == 201:
            UserSession.end_session(session_id=session['data'].id)

        session = UserSession.create_session(user=_user)
        # tokens = UserSession.create_tokens(user=_user)

        if session['status'] == 201:
            response = {
                'status': 201,
                'message': session['message'],
                'data': {
                    'access': session['tokens']['access'],
                    'refresh': session['tokens']['refresh'],
                    'refresh_access_in': JWT_ACCESS_TTL,
                    'refresh_in': JWT_REFRESH_TTL
                }
            }
        # if session['status'] == 208:
        #     response = {
        #         'status': 200,
        #         'message': session['message'],
        #         'data': {
        #             'access': tokens['access'],
        #             'refresh': tokens['refresh'],
        #             'refresh_access_in': JWT_ACCESS_TTL,
        #             'refresh_in': JWT_REFRESH_TTL
        #         }
        #     }
        return response

    def refresh_tokens(refresh: str) -> hash:
        # token = refresh
        # try:
        #     decoded_token = jwt.decode(str(token), SECRET_KEY, algorithms=["HS256"])
        # except jwt.InvalidSignatureError:
        #     return {'status': 403, 'message': 'Not valid token'}
        # except jwt.exceptions.ExpiredSignatureError:
        #     UserSession.end_session(session_id)
        #     return {'status': 403, 'message': 'Signature has expired'}

        # print(refresh)
        users = User.objects.filter(id = refresh['user_info']['user_id'])
        if not users:
            return {'status': 401, 'message': 'User id not found'}
        # timestamp = timezone.utcnow()
        # tokens = UserSession.create_tokens(users[0])
       

        # End session
        # session = UserSession.get_session_by_user_id(user_id=users[0].id)
        session = UserSession.get_active_session_by_user_id(user_id=users[0].id, 
                                                            created_at=datetime.fromtimestamp(refresh['iat']))
        # print(session['data'].id)

        if not UserSession.end_session(session_id=session['data'].id):
            return {'status': 500, 'message':'Internal server error'}
        
        # create session
        session = UserSession.create_session(user=users[0])
        if session['status'] == 201:
            response = {
                'status': 201,
                'message': session['message'],
                'data': {
                    'access': session['tokens']['access'],
                    'refresh': session['tokens']['refresh'],
                    'refresh_access_in': JWT_ACCESS_TTL,
                    'refresh_in': JWT_REFRESH_TTL
                }
            }

        return response

    def register(data: json)->hash:
        # check email don't exist yet
        _users = UserHelpers.find_user_by_email(data.get('email'))
        if _users:
            return {'status': 400, 'message':'Email already exists'}

        # adding new user
        new_user = UserHelpers.create_user(data)
        if new_user['status'] == 400:
            return {'status': 400, 'message':new_user['message']}

        # get new user's id
        user_id = new_user['data']['user_id']
        _users = User.objects.filter(id = user_id)
        user = _users[0] # getting new user from db by id

        # Deprecated
        # new_diagnostic = DiagnosticActivity.create_diagnostic(user, data.get('diagnostic_type')) # create dignostic
        # if new_diagnostic['status'] == 400:
        #     return {'status': new_diagnostic['status'], 'message': new_diagnostic['message']}

        new_session = UserSession.create_session(user) # create session
        # if new_session['status'] == 208:
        #     return {'status': 400, 'message': 'Try uncorrect authorization'}

        # tokens = UserSession.create_tokens(user) # create tokens

        return {
            'status': 201,
            'message': new_session['message'],
            'data': {
                'access': new_session['tokens']['access'],
                'refresh': new_session['tokens']['refresh'],
                'refresh_access_in': JWT_ACCESS_TTL,
                'refresh_in': JWT_REFRESH_TTL
            }
        }

    def user_profile(user_id: str):
        pass
    