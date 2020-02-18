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
dag_wf_directory = "generated_dags/wf/"
dag_tl_directory = "generated_dags/tool/"
def create_wf_filename(name,edit):
    '''
    create file_path for workflows
    os.path.join(path,*path)
    path : path representing a file system path
    *path: It represents the path components to be joined. 
    Name example : test_1.py (test: wf_name, 1:wf_edit)
    '''
    return f'{name}_{edit}', os.path.join(dag_wf_directory, f'{name}_{edit}.py')

def create_tl_filename(name,version,edit):
    '''
    create file_path for workflows
    os.path.join(path,*path)
    path : path representing a file system path
    *path: It represents the path components to be joined. 
    '''
    return f'{name}_{version}_{edit}', os.path.join(dag_tl_directory, f'{name}_{version}_{edit}.py')

def get_full_path(filename,dag_type):
    '''
    Get the full path of dag file 
    '''
    if dag_type == 'workflow':
        return f"{dag_wf_directory}/{filename}"
    elif dag_typy == 'tool':
        return f"{dag_tl_directory}/{filename}"

def generate_wf_file(name,edit,instructions):
    '''
    Get the data from request to generate the dag file
    name : The name of file to be generated
    instruction : The  contents of file to be generated
    return:
        generate_date: The generation date of dag file
    '''
    
    ret={}
    filename,filename_path = create_wf_filename(name,edit)
    
    if os.path.exists(filename_path):
        print("This file exists")
        delete_dag_file(filename_path)
        with open(filename_path,'w') as dag_file:
            dag_file.write(instructions)
        ret['generate_date'] = datetime.now()
        # ret['update_date']= datetime.now()
    else:
        with open(filename_path,'w') as dag_file:
            dag_file.write(instructions)
        ret['generate_date'] = datetime.now()
    # ret['owner']= 
    return ret

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

    dag_name = request.args.get('dag')
    # file_content = data['bash']
    owner = request.args.get('owner')
    delete_result['date'] = delete_dag_file(dag_name)
    delete_result['owner']= owner
    delete_result['dag_name']=dag_name
    delete_result['status']="deleted"
    delete_result['output'] = delete_from_airflow(dag_name)
    return delete_result

def get_airflow_container():
    '''
    NOT USED
    Trying to find the airflow container 
    and return the airflow container (Not working)
    '''
    docker = docker_setups()
    list_of_containers = docker.containers.list()
    print()
    for i in range(len(list_of_containers)):
        if 'docker-airflow_airflowserver_1' == list_of_containers[i].name:
            airflow = list_of_containers[i]
    return airflow

def trigger_command(dag):
    '''
    Not working
    '''
    return f"airflow trigger_dag {dag}"





def get_wf_OBC_rest(wf_name, wf_edit):
    '''
    Send GET request to OBC REST to get the dagfile
    RETURN dag File contents
    '''
    response = requests.get(f'http://0.0.0.0:8200/platform/rest/workflows/{wf_name}/{wf_edit}/?dag=true')

    if r.status_code != 200:
        print(f"Error while retrieving data. ERROR_CODE : {r.status_code}")
    else:
        print("success")

    dag_contents=response.json()['dag']
    
    return dag_contents


def dag_wf_trigger(name,edit):
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
    url = f'http://172.18.0.5:8080/api/experimental/dags/{name}__{edit}/dag_runs'
    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache"
        }

    payload={} # Future changes for scheduling workflow
    response = requests.post(url,data=json.dumps(payload),headers=headers)
    print("---> Response from airflow : ")
    print(response.json())
    return "success"

@app.route(f"/{os.environ['OBC_USER_ID']}/run_workflow", methods=['POST'])
def dag_trigger_workflow():
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
    data = json.loads(request.get_data().decode())

    wf_name = data['name']
    wf_edit = data['edit']

    dag_contents= get_wf_OBC_rest(wf_name,wf_edit)
    wf_gen_date=generate_wf_file(wf_name,wf_edit,dag_contents)
    payload['generation_date'] = wf_gen_date

    #Trigger dag
    payload['status']=trigger_dag(wf_name,wf_edit)



    '''
    TODO --> Get the dag content from OpenBio REST via requests
    ex. http://0.0.0.0:8200/platform/rest/workflows/{workflow_name}/{workflow_version}/?dag=true
    '''


    # url = f'http://172.18.0.5:8080/api/experimental/dags/{dag}/dag_runs'
    # headers = {
        # "Content-Type": "application/json",
        # "Cache-Control": "no-cache"
        # }



    return payload.json()