from django.shortcuts import render
from user.user_model.user_session import *
from .diagnostic_model.diagnostic_activity import *
from .diagnostic_model.diagnostic_helpers import *
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

@csrf_exempt
def load_recomendations(request):
    data = json.loads(request.body.decode())

    token = UserSession.decode_token(data.get('access'))
    if 'status' in token:
        return HttpResponse(json.dumps({}), content_type="text/plain", charset='utf-8', status=token['status'])

    email = token['user_info']['email']
    if email != 'develop@admin.com':
        return HttpResponse(json.dumps({}), content_type="text/plain", charset='utf-8', status=403)

    result = DiagnosticHelpers.load_recomendations_to_db(data.get('file_name'), data.get('diagnostic_type'))

    return HttpResponse(json.dumps({}), content_type="text/plain", charset='utf-8', status=200)

@csrf_exempt
def get_results(request):
    data = json.loads(request.body.decode())

    token = UserSession.decode_token(data.get('access'))
    if 'status' in token:
        return HttpResponse(json.dumps({}), content_type="text/plain", charset='utf-8', status=token['status'])

    result = DiagnosticActivity.get_results(user_id=token['user_info']['user_id'], 
        diagnostic_type=data.get('diagnostic_type'), answers=data.get('answers'))

    response = {}
    if 'data' in result:
        response['data'] = result['data']

    return HttpResponse(json.dumps(response,ensure_ascii=False), 
        content_type="text/plain", charset='utf-8', status=result['status'])

@csrf_exempt
def get_questions(request):
    data = json.loads(request.body.decode())

    token = UserSession.decode_token(data.get('access'))
    if 'status' in token:
        return HttpResponse(json.dumps({}), content_type="text/plain", charset='utf-8', status=token['status'])

    questions = DiagnosticActivity.get_questions(data.get('diagnostic_type'))
    response = {}
    if 'data' in questions:
        response['data'] = questions['data']
    else:
        return HttpResponse(json.dumps({}), content_type="text/plain", charset='utf-8', status=500)
        
    return HttpResponse(json.dumps(response,ensure_ascii=False), content_type="text/plain", charset='utf-8', status=questions['status'])