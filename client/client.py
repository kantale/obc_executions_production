import os
import urllib
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json
import os 
from datetime import datetime
import docker
import requests

def docker_setups():
    '''
    NOT USED
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
#TODO -> Set public ip of OBC_server and OBC_Client as enviroment variable
OBC_server="192.168.1.13"
OBC_client=""

dag_directory = "generated_dags/"
#not fixed we use tha same dir for tool and workflows
dag_wf_directory = "generated_dags/wf/"
dag_tl_directory = "generated_dags/tool/"
def create_workflow_filename(name,edit):
    '''
    create file_path for workflows
    os.path.join(path,*path)
    path : path representing a file system path
    *path: It represents the path components to be joined. 
    Name example : test_1.py (test: wf_name, 1:wf_edit)
    '''
    return f'{name}_{edit}', os.path.join(dag_directory, f'{name}_{edit}.py')

def create_tool_filename(name,edit,version):
    '''
    create file_path for workflows
    os.path.join(path,*path)
    path : path representing a file system path
    *path: It represents the path components to be joined. 
    Name example : test_1.py (test: wf_name, 1:wf_edit)
    '''
    return f'{name}_{version}_{edit}', os.path.join(dag_directory, f'{name}_{version}_{edit}.py')

def get_full_path(filename):
    '''
    Get the full path of dag file 
    '''
    dag_type='workflow'
    if dag_type == 'workflow':
        return f"{dag_wf_directory}/{filename}"
    elif dag_typy == 'tool':
        return f"{dag_tl_directory}/{filename}"

def generate_workflow_file(workflow_id,name,edit,instructions):
    '''
    Get the data from request to generate the dag file
    name : The name of file to be generated
    instruction : The  contents of file to be generated
    return:
        generate_date: The generation date of dag file
    '''
    
    ret={}
    filename,filename_path = create_workflow_filename(name,edit)
    
    if os.path.exists(filename_path):
        print("This file exists")
        delete_dag_file(filename_path)
        with open(filename_path,'w') as dag_file:
            dag_file.write(instructions)
        # ret['generate_date'] = datetime.now()
        # ret['update_date']= datetime.now()
    else:
        with open(filename_path,'w') as dag_file:
            dag_file.write(instructions)
        # ret['generate_date'] = datetime.now()
    # ret['owner']= 
    # return ret

def generate_tool_file(name,version,edit,instructions):
    '''
    Get the data from request to generate the dag file
    name : The name of file to be generated
    instruction : The  contents of file to be generated
    return:
        generate_date: The generation date of dag file
    '''
    
    ret={}
    filename,filename_path = create_tool_filename(name,edit,version)
    
    if os.path.exists(filename_path):
        print("This file exists")
        delete_dag_file(filename_path)
        with open(filename_path,'w') as dag_file:
            dag_file.write(instructions)
        # ret['generate_date'] = datetime.now()
        # ret['update_date']= datetime.now()
    else:
        with open(filename_path,'w') as dag_file:
            dag_file.write(instructions)
        # ret['generate_date'] = datetime.now()
    # ret['owner']= 
    # return ret

def delete_from_airflow(dag_name):
    '''
    Delete the dag from airflow Database
    '''
    url = f'http://172.18.0.5:8080/api/experimental/dags/{dag_name}/dag_runs'
    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache"
        }

    response = requests.delete(url)

    return response

def delete_dag_file(dag_name):
    '''
    Delete selected dag file
    '''
    ret={}
    full_path = get_full_path(dag_name)
    if os.path.exists(full_path):
        os.remove(full_path)
        ret['delete_date'] = datetime.now()
    else:
        ret['generate_date'] = None
        ret['msg']= "The file does not exist"
    return ret

@app.route(f"/{os.environ['OBC_USER_ID']}/generate_dag", methods=['POST'])
def generate_dag():
    '''
    NOT USED YET
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

@app.route(f"/{os.environ['OBC_USER_ID']}/update_dag", methods=['PUT'])
def update_dag():
    '''
    NOT USED YET
    '''
    data= json.loads(request.get_data().decode())
    filename = f"{data['filename']}.py"
    owner = data['owner']
    pyfile = urllib.parse.unquote(filename,pyfile)
    up_result["date"] = generated_dag_file(filename,pyfile) 
    up_result['owner']=owner
    up_result['status']="untriggered"
    return up_result


@app.route(f"/{os.environ['OBC_USER_ID']}/delete_dag", methods=['DELETE','GET'])
def delete_dag():
    '''
    NOT USED YET
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

    delete_result={}
    data = json.loads(request.get_data())
    name = data['name']
    edit = data['edit']   
    dag_filename=f"{name}_{edit}.py" 
    dag_name=f"{name}__{edit}"
    delete_result['date'] = delete_dag_file(dag_name)
   

    # # delete_result['owner']= owner
    # delete_result['dag_name']=dag_name
    delete_result['status']="deleted"
    delete_result['output'] = delete_from_airflow(dag_name)
    print(f"delete_result = {type(delete_result)}")
    print(f"data = {type(data)}")
    
    return data
     # return data



def get_tool_OBC_rest(tl_name, tl_edit):
    '''
    Send GET request to OBC REST to get the dagfile
    RETURN dag File contents
    0.0.0.0:8200 MUST BE CHANGED WITH THE MAIN OBC SERVER
    '''
    response = requests.get(f'http://{OBC_server}:8200/platform/rest/tools/{tl_name}/{tl_version}/{tl_edit}/?dag=true')

    if response.status_code != 200:
        print(f"Error while retrieving data. ERROR_CODE : {response.status_code}")
        dag_contents['success']='false'
        dag_contents['error']=f"Error while retrieving data. ERROR_CODE : {response.status_code}"
    else:
        print("success")
        dag_contents=response.json()
    
    return dag_contents


def get_workflow_OBC_rest(callback,wf_name, wf_edit,workflow_id):
    '''
    Send GET request to OBC REST to get the dagfile
    RETURN dag File contents
    '''
    response = requests.get(f'{callback}rest/workflows/{wf_name}/{wf_edit}/?dag=true&workflow_id={workflow_id}')
    dag_contents={}
    if response.status_code != 200:
        print(f"Error while retrieving data. ERROR_CODE : {response.status_code}")
        dag_contents['success']='false'
        dag_contents['error']=f"Error while retrieving data. ERROR_CODE : {response.status_code}"
    else:
        print("success")
        dag_contents=response.json()
    
    return dag_contents


def dag_workflow_trigger(workflow_id,name,edit):
    '''
    Trigger the dag from OpenBio
    Function starts using docker between containers which didn't work
    As a result, we will use experimental api from airflow

    Request using curl :
    curl -X POST \
      http://< PUBLIC IP >:8080/api/experimental/dags/pca_plink_and_plot__1/dag_runs \
      -H 'Cache-Control: no-cache' \
      -H 'Content-Type: application/json' \
      -d '{}'

    According to docker-compose file we have create containers network 
    which communicate both airflow and OBC_client
    '''
    ret = {}
    url = f'http://172.18.0.5:8080/api/experimental/dags/{workflow_id}/dag_runs'
    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache"
        }

    payload={} # Future changes for scheduling workflow
    response = requests.post(url,data=json.dumps(payload),headers=headers)
    while "error" in response.json():
        response = requests.post(url,data=json.dumps(payload),headers=headers)
        if "error" not in response.json():
            break
    print("---> Response from airflow : ")
    print(response.json())
    return response.json()

def dag_tool_trigger(name,edit,version):
    '''
    Trigger the dag from OpenBio
    Function starts using docker between containers which didn't work
    As a result, we will use experimental api from airflow

    Request using curl :
    curl -X POST \
      http://< PUBLIC IP >:8080/api/experimental/dags/pca_plink_and_plot__1/dag_runs \
      -H 'Cache-Control: no-cache' \
      -H 'Content-Type: application/json' \
      -d '{}'

    According to docker-compose file we have create containers network 
    which communicate both airflow and OBC_client
    '''
    ret = {}
    url = f'http://172.18.0.5:8080/api/experimental/dags/{name}__{version}__{edit}/dag_runs'
    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache"
        }

    payload={} # Future changes for scheduling workflow
    response = requests.post(url,data=json.dumps(payload),headers=headers)
    print("---> Response from airflow : ")
    print(response.json())
    return "success"

@app.route(f"/{os.environ['OBC_USER_ID']}/run", methods=['POST'])
def dag_trigger():
    '''
    Trigger the dag from OpenBio
    Function starts using docker between containers which didn't work
    As a result, we will use experimental api from airflow
    -> Get request from OpenBio Platform with data below:
        1) Type : it has two different types (tool or workflow)
        2) Name : workflow name,
        3) Edit : specific version of workflow from OpenBio rest.
    -> Send request to OpenBio restAPI to get the dag file. The request must contains:
        1) Name : name of workflow (or tool) to search 
        2) Version : version of tool only to search
        3) Edit : edit of workflow (or tool to search)
                
    Get dag content from 
    Request using curl to run the generated dag:
    curl -X POST \
      http://< PUBLIC IP >:8080/api/experimental/dags/pca_plink_and_plot__1/dag_runs \
      -H 'Cache-Control: no-cache' \
      -H 'Content-Type: application/json' \
      -d '{}'

    According to docker-compose file we have create containers network 
    which communicate both airflow and OBC_client
    '''
    payload={} # Future changes for scheduling workflow
    data = json.loads(request.get_data())

    name = data['name']
    edit = data['edit']
    work_type = data['type']
    callback= data['callback']
    workflow_id= data['workflow_id']
    print(request.base_url)
    if work_type == 'tool':
        version = data['version']
        dag_contents= get_tool_OBC_rest(name,edit,version)
        try:
            if dag_contents['success']!='failed':
                generate_tool_file(name,edit,version)
                payload['status']=dag_tool_trigger(name,version,edit)
            else:
                payload['status']='failed'
                payload['reason']=dag_contents
        except KeyError:
            print('Dag not found')
            payload=dag_contents
    elif work_type == 'workflow':
        dag_contents= get_workflow_OBC_rest(callback,name,edit,workflow_id)
        try:
            if dag_contents['success']!='failed':
                generate_workflow_file(workflow_id,name,edit,dag_contents['dag'])
                payload['status']=dag_workflow_trigger(workflow_id,name,edit)
            else:
                payload['status']='failed'
                payload['reason']=dag_contents
        except KeyError:
            print('Dag not found')
            payload=dag_contents
    else:
        payload['status']="failed"
        payload['error']="Unknown type (worfkflow or tool)"
    return json.dumps(payload)


@app.route(f"/{os.environ['OBC_USER_ID']}/check", methods=['GET'])
def get_status_of_workflow():
    '''
    Get dag status from airflow
    Request using curl to get the status of running or finished dag:
    curl -X GET \
      http://< PUBLIC IP >:8080/api/experimental/dags/pca_plink_and_plot__1/dag_runs \
      -H 'Cache-Control: no-cache' \
      -H 'Content-Type: application/json' \
      -d '{
          "id":"bla bla"
      }'

    '''
