# from django.shortcuts import render
from django.http import HttpResponse
# from .models import User
from django.views.decorators.csrf import csrf_exempt
import json
from user.user_model.user_activity import *
import jwt

@csrf_exempt
def register(request):
    # try:
    # data = json.loads(request.body.decode())
    # except ValueError:
    #     return HttpResponse({
    #         'error': 'bla bla bla',
    #     })

    # print(data.get('email'))
    # activity = Activity(request)
    # activity.register_user()
    # activity.register_user()
    # print (activity)
    return HttpResponse(json.dumps({}), content_type="text/plain", charset='utf-8', status=200)

@csrf_exempt
def login(request):
    # try:
    data = json.loads(request.body.decode('utf-8'))
    # except ValueError:
    #     return HttpResponse({
    #         'error': 'bla bla bla',
    #     })

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

@csrf_exempt
def refresh(request):
    # try:
    data = json.loads(request.body.decode('utf-8'))
    # except ValueError:
    #     return HttpResponse({
    #         'error': 'bla bla bla',
    #     })
    token = data.get('refresh')
    # print(token)

    try:
        decoded_token = jwt.decode(token, 'Ij3q78Wm+yTs4hHtq7Xjw2bL1OW+YtFwGOLiC5jUCuk', algorithms='HS256')
    except jwt.InvalidSignatureError:
        print("LOH!")
        # return error
    print(decoded_token)
    return HttpResponse(json.dumps({}), content_type="text/plain", charset='utf-8', status=200)