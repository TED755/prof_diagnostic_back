from user.models import *
from .user_helpers import UserHelpers
from .user_session import UserSession
import json
import jwt

class UserActivity():
     # response: json {'status','erorr','user_id', tokens{refresh, access}, user_info}
    def login(data: json) -> json:
        _users = UserHelpers.find_user_by_email(data.get('email'))
        if not _users:
            return json.dumps({'status':'error', 'error':'Invalid email or password', 
                'user_id':{}, 'tokens':{}, 'user_info':{
                    'email':data.get('email')
                }})

        _user = _users[0]
        if not UserHelpers.check_password(_user, data.get('password')):
            return json.dumps({'status':'error', 'error':'Invalid email or password', 
                'user_id':{}, 'tokens':{}, 'user_info':{
                    'email':data.get('email')
                }})
        
        session = UserSession.create_session(user=_user)

        response = json.dumps({
            'status': 'OK',
            'error': '',
            'user_id': session.user_id,
            'tokens': {
                'access': session.access_token,
                'refresh': session.refresh_token
            },
            'user_info': UserHelpers.user_info(_user)
        }, ensure_ascii=False)
        # print(jwt.decode(session.access_token, 'secret', algorithms="HS256"))
        

        # print (f"{session.user_id}, {session.start_date}, {session.start_time}")
        # key = 'secret' # Разные для каждого пары?
        
        # return json {'user_id', tokens{refresh, access}, user_info}
        return response

    # def crypt_password(password):
    #     return password
    # def decrypt_password(password):
    #     return password

    # def find_user_by_email(email):
    #     return User.objects.filter(email=email)
    
    # def check_password(user: User, password):
    #     return UserActivity.decrypt_password(user.password) == password
    
    