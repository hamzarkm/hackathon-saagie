from django.shortcuts import render
from django.http import HttpResponse
import requests

# Create your views here.

def getToken():
    url = "https://demo-workspace.a4.saagie.io/authentication/api/open/authenticate"
    headers = {'content-type': 'application/json','Saagie-Realm':'demo'}
    r = requests.post(url, headers=headers, data={'login': 'ESTIAM_G18_manuel.dassi-kueti','password': 'QAmvjE9TSU'})
    print(r.text)


def index(request):
    getToken()
    return HttpResponse("welcome")

 