import os
import urllib
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json
import os 
from datetime import datetime
import docker

def docker_setups():
    '''
    Connect with docker api
    '''
    client = docker.from_env()
    return client
# Init app


app = Flask(__name__)

# Run server
if __name__ == '__main__':
    #debug is true for dev mode
    app.run(debug=True)
    

# Dag_directory
dag_directory = "generated_dags/"
def create_filename(name):
    '''
    create file_path
    os.path.join(path,*path)
    path : path representing a file system path
    *path: It represents the path components to be joined. 
    '''
    return name, os.path.join(dag_directory, f'{name}.py')

def get_full_path(filename):
    '''
    Get the full path of dag file 
    '''
    return f"{dag_directory}/{filename}"

def generate_dag_file(name,instructions):
    '''
    Get the data from request to generate the dag file
    name : The name of file to be generated
    instruction : The  contents of file to be generated
    return:
        generate_date: blah
        owner: blah
    '''
    
    ret={}
    filename,filename_path = create_filename(name)
    
    # Save the dag_file
    if os.path.exists(filename_path):
        print("This file exists")
        delete_dag_file(filename_path)
        with open(filename_path,'w') as dag_file:
            dag_file.write(instructions)
        ret['generate_date'] = datetime.now()
        ret['update_date']= datetime.now()
    else:
        with open(filename_path,'w') as dag_file:
            dag_file.write(instructions)
        ret['generate_date'] = datetime.now()
    # ret['owner']= 
    return ret


def delete_dag_file(filename):
    '''
    Delete selected dag file
    '''
    ret={}
    full_path = get_full_path(filename)
    if os.path.exists(full_path):
        os.remove(full_path)
        ret['generate_date'] = datetime.now()
        ret['error_msg']= "The file removed successfully"
    else:
        ret['generate_date'] = None
        ret['msg']= "The file does not exist"

    return ret
@app.route('/generate_dag', methods=['POST'])
def generate_dag():
    '''
    Get request from openBio platform
    which contains the file name, dag instructions
    request data :
    filename:blah,
    bash:blah,
    owner:blah,

    response:
        generate_date: blah
        owner: blah
        status:untriggered
    '''
    # Parse data json to dict
    gen_result={}
    data = json.loads(request.get_data().decode())     
    filename = data['filename']
    file_content = data['bash']
    owner = data['owner']
    pyfile = urllib.parse.unquote(file_content)
    gen_result['date'] = generate_dag_file(filename,pyfile)
    gen_result['owner']= owner
    gen_result['status']="untriggered"
    return gen_result

@app.route('/update_dag', methods=['PUT'])
def update_dag():
    '''
    '''
    data= json.loads(request.get_data().decode())
    filename = f"{data['filename']}.py"
    owner = data['owner']
    pyfile = urlib.parse.unquote(filename,pyfile)
    up_result["date"] = generated_dag_file(filename,pyfile) 
    up_result['owner']=owner
    up_result['status']="untriggered"
    return up_result


@app.route('/delete_dag', methods=['POST'])
def delete_dag():
    '''
    Get request from openBio platform
    which contains the file name, dag instructions
    request data :
    filename:blah,
    bash:blah,
    owner:blah,

    response:
        generate_date: blah
        owner: blah
        status:deleted
    '''
    # Parse data json to dict
    data = json.loads(request.get_data().decode())     
    filename = f"{data['filename']}.py"
    # file_content = data['bash']
    owner = data['owner']
    delete_result['date'] = delete_dag_file(filename)
    delete_result['owner']= owner
    delete_result['filename']=filename
    # gen_result['status']="deleted"
    return delete_result
def get_airflow_container():
    '''
    Trying to find the airflow container 
    and return the airflow container
    '''
    docker = docker_setups()
    list_of_containers = docker.containers.list()
    for i in range(len(list_of_containers)):
        if 'docker-airflow_airflowserver_1' == list_of_containers[i].name:
            airflow = list_of_containers[i]
    return airflow

def trigger_command(dag):
    '''
    '''
    return f"airflow trigger_dag {dag}"

def trigger_dag(dag):
    '''
    '''
    ret={}
    airflow = get_airflow_container()
    # the response of execution look like : 
    # ExecResult(exit_code=0, output=b'') 
    exec_out = airflow.exec_run(trigger_command(dag))    
    ret["status_code"]= exec_out[0]
    ret["output"]=exec_out[1]
    return ret

@app.route('/trigger_dag', methods=['POST'])
def dag_trigger():
    '''
    Trigger the dag from OpenBio
    '''
    ret = {}
    data = json.loads(request.get_data().decode())

    dag = data['dag_name']
    owner= data['owner']
    info = trigger_dag(dag)
    ret["code"]=info["status_code"]
    ret["output"]= info["output"]
    ret["status"]= "triggered"
    return ret