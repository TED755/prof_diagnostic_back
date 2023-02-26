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
        data = json.loads(request.body.decode())
    except ValueError:
        return HttpResponse({
            'error': 'bla bla bla',
        })

    # response: json {'user_id', tokens{refresh, access}, user_info}
    login_user = UserActivity.login(data)
    if not login_user:
        return HttpResponse(request, json.dumps({'error':'Invalid email or password'}))
    return HttpResponse(request, json.dumps({'status':'OK', 
        'data':{'name':login_user.name, 'email':login_user.email}, 'session':{}}))
    # email = data.get('email')
    # password = data.get('password')

    # if email == right_email and password == right_password:
    #     return HttpResponse(request, json.dumps({'name':'Test User One', 'email':email, 'status':'OK'}))
    # else: return HttpResponse(request, json.dumps({'email':email, 'error':'Invalid email or password'}))
