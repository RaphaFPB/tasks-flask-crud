import pytest
import requests

#CRUD
BASE_URL = 'http://127.0.0.1:5000'
tasks = []

def test_create_task():
    new_task_data = {
        "title": "Nova tarefa",
        "description": "Descrição da nova tarefa"
    }
    response = requests.post(f"{BASE_URL}/tasks", json=new_task_data)
    assert response.status_code == 200#STAUTS           /validar, caso contrário quebra o teste
    response_json = response.json()
    assert "message" in response_json #se msg existe logo TTrue
    assert "id" in response_json #verifica se id existe
    tasks.append(response_json['id'])


def test_get_tasks():
    response = requests.get(f"{BASE_URL}/tasks")#não precisa passa json pois não possui body
    assert response.status_code == 200
    response_json = response.json()#trás o corpo da resposta
    assert "tasks" in response_json
    assert "total_tasks" in response_json

def teste_get_task():
    if tasks:
        task_id = tasks[0]
        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200
        response_json = response.json()
        assert task_id == response_json['id']


def test_update_task():
    if tasks:
        task_id = tasks[0]
        payload = {
            "completed": True,
            "description": "Descrição da nova tarefa de teste",
            "title": "Nova tarefa de teste"
}
        response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=payload)
        response.status_code == 200
        response_json = response.json()
        assert "message" in response_json
        
        #Nova requisição a tarefa especifica
        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200
        response_json = response.json()
        assert  payload["title"]== response_json['title']
        assert payload["description"]== response_json['description']
        assert  payload["completed"]== response_json['completed']
     
def test_delete_task():
    if tasks:
        task_id=tasks[0]
        response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
        response.status_code == 200

        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 404 #refaz a requisição para verificar se foi apagado
        

