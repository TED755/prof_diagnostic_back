from django.shortcuts import render
from user.user_model.user_session import *
from .diagnostic_model.diagnostic_activity import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

@csrf_exempt
def save_progress(request):
    data = json.loads(request.body.decode())

    token = UserSession.decode_token(data.get('access'))
    if 'status' in token:
        return HttpResponse(json.dumps({}), content_type="text/plain", charset='utf-8', status=token['status'])

    # print(token)
    response = DiagnosticActivity.save_progress(user_id=token['user_info']['user_id'], 
        diagnostic_type=data.get('diagnostic_type'), answers=data.get('answers'))

    if 'status' not in response:
        return HttpResponse(json.dumps({'message':'Internal server error'}), 
            content_type="text/plain", charset='utf-8', status=500)

    return HttpResponse(json.dumps({}), content_type="text/plain", charset='utf-8', status=response['status'])

@csrf_exempt
def get_diagnostic(request):
    data = json.loads(request.body.decode())
    response = {}

    token = UserSession.decode_token(data.get('access'))
    if 'status' in token:
        return HttpResponse(json.dumps({}), content_type="text/plain", charset='utf-8', status=token['status'])

    response = DiagnosticActivity.get_diagnostic(user_id=token['user_info']['user_id'], 
        diagnostic_type=data.get('diagnostic_type'))

    if 'status' not in response:
        return HttpResponse(json.dumps({'message':'Internal server error'}), 
            content_type="text/plain", charset='utf-8', status=500)

    return HttpResponse(json.dumps(response['data']), content_type="text/plain", charset='utf-8', status=response['status'])