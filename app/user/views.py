# from django.shortcuts import render
from django.http import HttpResponse
# from .models import User
from django.views.decorators.csrf import csrf_exempt
import json
from user.user_model.user_activity import *

@csrf_exempt
def register(request):
    # try:
    data = json.loads(request.body.decode())
    # except ValueError:
    #     return HttpResponse({
    #         'error': 'bla bla bla',
    #     })
    _response = UserActivity.register(data)
    response = {}
    if 'data' in _response:
        response['data'] = _response['data']

    return HttpResponse(json.dumps(response), content_type="text/plain", charset='utf-8', status=_response['status'])

@csrf_exempt
def login(request):
    # try:
    data = json.loads(request.body.decode('utf-8'))
    # except ValueError:
    #     return HttpResponse({
    #         'error': 'bla bla bla',
    #     })

    login_user = UserActivity.login(data)

    response = {}
    if 'data' in login_user:
        response['data'] = login_user['data']

    return HttpResponse(json.dumps(response), content_type="text/plain", charset='utf-8', status=login_user['status'])

@csrf_exempt
def refresh(request):
    # try:
    data = json.loads(request.body.decode('utf-8'))
    refresh = UserActivity.refresh_tokens(data)
    # print(response)
    response = {}
    # response = {
    #     'message': refresh['message']
    # }
    if 'data' in  refresh:
        response['data'] = refresh['data']
    # except ValueError:
    #     return HttpResponse({
    #         'error': 'bla bla bla',
    #     })
    
    return HttpResponse(json.dumps(response), content_type="text/plain", charset='utf-8', status=refresh['status'])