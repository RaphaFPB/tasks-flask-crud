from flask import Flask, request, jsonify
from models.task import Task


#__name__="__main__"

app = Flask(__name__)

#CRUD
# Create, Read, Update and Delete =  Criar, Ler, Atualizar e Deletar
#Tabela: Tarefa

tasks = []
task_id_control = 1

@app.route('/tasks', methods = ['POST'])
def create_task():
    global task_id_control #usado para pegar referencias fora do metodo, como pore exemplo variavel task id
    data = request.get_json()  #parametro abaix poderia ser também data["title"]
    new_task = Task(id=task_id_control,title = data.get("title"), description = data.get("description", ""))#string vazia para caso o cliente envie em branco
    task_id_control += 1
    tasks.append(new_task)
    print(tasks) 
    print(data)
    return jsonify({"message" : "Nova tarefa criada com sucesso", "id":new_task.id})#metodo para retornar json, padrão flask

@app.route('/tasks', methods=['GET'])
def get_tasks():
    #task_list = []
    """metodo 1->>>>>for task in tasks:
        task_list.append(task.to_dict())#ordem apresentada no response do postman n importa pois está em json"""
    #metodo 2
    task_list = [task.to_dict() for task in tasks]


    output = {
                "tasks": task_list,
                "total_tasks": len(task_list)
            }
    return jsonify(output)


@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())
        
    return jsonify({"message": "Não foi possível encontrar a tarefa!"}), 404


"""@app.route('/user/<int:user_id>')#criação de parametros de rota. Parametro será sempre string <conversor:parametro> (int:id)
def show_user(user_id):
    print(user_id)
    print(type(user_id))
    return "%s" % user_id

path=like string but also accepts slashes

uuid=accepts UUID strings"""

@app.route('/tasks/<int:id>', methods = ['PUT'])
def update_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break
      
    if task == None:
        return jsonify({"message": "Não foi possível encontrar a atividade"}), 404
    data = request.get_json()        
    task.title = data.get("title")
    task.description = data["description"]
    task.completed = data.get('completed')
    
    return jsonify({"message": "Tarefa atualizada com sucesso!"})


@app.route('/tasks/<int:id>', methods = ['DELETE'])
def delete_task(id):
    task=None
    for t in tasks:
        
        if t.id ==id:
            task=t
            break
    
    if not task:
        return jsonify({"message": "Não foi possível encontrar a atividade"}), 404
    
    tasks.remove(task)
    return jsonify({"message:": "Tarefa deletada com sucesso"})

if __name__=="__main__":
    app.run(debug=True)


