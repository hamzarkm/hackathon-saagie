from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from string import Template
import requests

# Create your views here.

def getToken():
    url = "https://demo-workspace.a4.saagie.io/authentication/api/open/authenticate"
    headers = {'content-type': 'application/json','Saagie-Realm':'demo'}
    r = requests.post(url, headers=headers, json={'login': 'ESTIAM_G18_manuel.dassi-kueti','password': 'QAmvjE9TSU'})
    return r.text


def getProject(token):
    url = "https://demo-workspace.a4.saagie.io/projects/api/platform/2/graphql"
    headers =  {'content-type': 'application/json','Authorization':'Bearer ' + token}
    query = """query {
    project(id:"c185250d-bf87-484f-ae6f-4377b19f7176"){
		id
		name
		status
		creator
		description
		jobsCount
		apps{
			id
		}
		pipelines{
			id
		}
		volumes{
			id
        }
	}
    rights(projectId:"c185250d-bf87-484f-ae6f-4377b19f7176"){
		name
		role
	}
    }"""
    r = requests.post(url, headers=headers, json={'query': query})
    return r.json()


def getTechnologies(token):
    url = "https://demo-workspace.a4.saagie.io/gateway/api/graphiql"
    headers =  {'content-type': 'application/json','Authorization':'Bearer ' + token}
    query = """query {
    technology(id:"526b740f-007d-4582-b9e8-0ca64aff68f0"){
		description
		label
		available
		icon
	}
    }"""
    r = requests.post(url, headers=headers, json={'query': query})
    return r.json()


def copyProject(token, name, description):
    url = "https://demo-workspace.a4.saagie.io/gateway/api/graphiql"
    headers =  {'content-type': 'application/json','Authorization':'Bearer ' + token}
    mutation = Template("""mutation {
    createProject(project: {
		name:$projectName,
		description: $projectDescription,
		appTechnologies: [],
		authorizedGroups: []
	}){
		id
	}
    }""")
    r = requests.post(url, headers=headers, json={'mutation': mutation.substitute(projectName=name, projectDescription=description)})
    return r.text
    

def index(request):
    token = getToken()
    project = getProject(token)
    technologies = getTechnologies(token)
    response = {
        'info': project,
        'technologies': technologies 
    }

    newProject = copyProject(token, project["data"]["project"]["name"], project["data"]["project"]["description"])
    print(newProject)

    return  JsonResponse(response)



 