from django.shortcuts import render
from django.http import HttpResponse
# from .models import User
from django.views.decorators.csrf import csrf_exempt
import json
from user.user_model.user_activity import *

# @csrf_exempt
# def register(request):
#     try:
#         data = json.loads(request.body.decode())
#     except ValueError:
#         return HttpResponse({
#             'error': 'bla bla bla',
#         })

#     print(data.get('email'))
#     # activity = Activity(request)
#     # activity.register_user()
#     # activity.register_user()
#     # print (activity)
#     return HttpResponse(request, {'email': data.get('email'), 'password': data.get('password')})

@csrf_exempt
def login(request):
    # right_email = 'test_user1@test.com'
    # right_password = '123'
    try:
        data = json.loads(request.body.decode('utf-8'))
    except ValueError:
        return HttpResponse({
            'error': 'bla bla bla',
        })

    # response: json {'status','erorr','user_id', tokens{refresh, access}, user_info}
    login_user = UserActivity.login(data)

    response = {
        'message': login_user['message'],
    }
    if 'data' in login_user:
        response['data'] = login_user['data']

    return HttpResponse(json.dumps(response), content_type="text/plain", charset='utf-8', status=login_user['status'])

    # if login_user['message'] == 'Invalid email or password':
    #     return HttpResponse(json.dumps(login_user), content_type="text/plain", charset='utf-8', status=401)
    # return HttpResponse(json.dumps(login_user), content_type="text/plain", charset='utf-8', status=201)

    # if not login_user:
    #     return HttpResponse(request, json.dumps({'error':'Invalid email or password'}))
    # return HttpResponse(request, json.dumps({'status':'OK', 
    #     'data':{'name':login_user.name, 'email':login_user.email}, 'session':{}}))


    # email = data.get('email')
    # password = data.get('password')

    # if email == right_email and password == right_password:
    #     return HttpResponse(request, json.dumps({'name':'Test User One', 'email':email, 'status':'OK'}))
    # else: return HttpResponse(request, json.dumps({'email':email, 'error':'Invalid email or password'}))
