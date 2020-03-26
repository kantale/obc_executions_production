import os
import urllib
from flask import Flask, request, Response, redirect, jsonify, send_file, send_from_directory, safe_join, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json
import os 
from datetime import datetime
import docker
import requests
import time
# This module is to make logs in zip type
import zipfile 
import shutil
import sys
#Communicate with airflow database
import pg8000
'''
SOME USEFULL VARIABLES TO WORK WITH
  OBC_USER_ID=${OBC_USER_ID}
  PUBLIC_IP=${PUBLIC_IP}
  EXECUTOR_INSTANCE=${EXECUTOR_INSTANCE}
  POSTGRES_USER=${POSTGRES_USER}
  POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
  POSTGRES_DB=${POSTGRES_DB}
  NETDATA_MONITORING_PORT=${NETDATA_MONITORING_PORT}
  OBC_EXECUTOR_PORT=${OBC_EXECUTOR_PORT}
  OBC_AIRFLOW_PORT=${OBC_AIRFLOW_PORT}
  EXECUTOR_DB_PORT=${EXECUTOR_DB_PORT}

  TODO -> FUTURE CHANGES
  EXECUTORS_VARIABLES={
    "general":{
        "NETDATA_MONITORING_PORT":"19999",
        "OBC_EXECUTOR_PORT":"5000",
        "PUBLIC_IP":"213.239.220.77"
    },
    "bcaf97d51ff173e5f6723fa55e5a0d5c":
    {
        "EXECUTOR_INSTANCE":"production",
        "POSTGRES_USER":"airflow",
        "POSTGRES_PASSWORD":"airflow",
        "POSTGRES_DB":"airflow",
        "OBC_AIRFLOW_PORT":"8080",
        "EXECUTOR_DB_PORT":"5432"
    },
    "0000000000002245f672awgb3axc2568":
    {
        "EXECUTOR_INSTANCE":"test1",
        "POSTGRES_USER":"aircow",
        "POSTGRES_PASSWORD":"aircow",
        "POSTGRES_DB":"aircow",
        "OBC_AIRFLOW_PORT":"8081",
        "EXECUTOR_DB_PORT":"5433"
    }
}
'''
def print_f(message):
    '''
    For debug scopes
    '''
    return print(message,file=sys.stderr)

def docker_setups():
    '''
    NOT USED
    Connect with docker api
    '''
    print_f("aaaa")
    client = docker.from_env()
    return client

# Init app

def connect_to_airflow_db():
    '''
    Connect to airflow Postgresql and allow us execute query from obc_client
    '''
    conn = pg8000.connect(
        database=os.environ['POSTGRES_DB'],
        user=os.environ['POSTGRES_USER'], 
        password=os.environ['POSTGRES_PASSWORD'],
        host=os.environ['PUBLIC_IP'],
        port=int(os.environ['EXECUTOR_DB_PORT']))

    return conn

def execute_query(query):
    '''
    execute the query and return the result as a list
    '''
    conn = connect_to_airflow_db()
    cursor= conn.cursor()
    result = cursor.execute(query)
    return result


app = Flask(__name__)

# Run server
if __name__ == '__main__':
    #debug is true for dev mode
    app.run(debug=True)
    

# Dag_directory
dag_directory = f"{os.environ['AIRFLOW_HOME']}/dags/"
#not fixed we use tha same dir for tool and workflows
# dag_wf_directory = "dags/wf/"
# dag_tl_directory = "dags/tool/"
compressed_logfiles = f"{os.environ['AIRFLOW_HOME']}/logs/compressed_logs/"

def create_filename(id):
    '''
    create file_path for workflows or tool
    os.path.join(path,*path)
    path : path representing a file system path
    *path: It represents the path components to be joined. 
    Name example : kitsos.py (kitsos:wf_id or tool_id)
    '''
    return f'{id}', os.path.join(dag_directory, f'{id}.py')

def get_full_path(filename):
    '''
    Get the full path of dag file 
    '''
    dag_type='workflow'
    # if dag_type == 'workflow':
    #     return f"{dag_wf_directory}/{filename}"
    # elif dag_type == 'tool':
    #     return f"{dag_tl_directory}/{filename}"
    return f"{dag_directory}{filename}.py"
def generate_file(dag_id,instructions):
    '''
    Get the data from request to generate the dag file
    name : The name of file to be generated
    instruction : The  contents of file to be generated
    return:
        generate_date: The generation date of dag file
    '''
    
    ret={}
    filename,filename_path = create_filename(dag_id)
    
    if os.path.exists(filename_path):
        print_f("This file exists")
        with open(filename_path,'w') as dag_file:
            dag_file.write(instructions)
    else:
        with open(filename_path,'w') as dag_file:
            dag_file.write(instructions)

def delete_from_airflow(dag_name):
    '''
    Delete the dag from airflow Database
    '''
    url = f"http://{os.environ['PUBLIC_IP']}:8080/{os.environ['OBC_USER_ID']}/api/experimental/dags/{dag_name}"
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
    print_f(f"File -->{full_path} \nFile exists --> {str(os.path.exists(full_path))}")
    if os.path.exists(full_path):
        print_f(f"File exist --> {full_path}")
        os.remove(full_path)
        ret['delete_date'] = datetime.now()
    else:
        ret['generate_date'] = None
        ret['msg']= "The file does not exist"
    print_f(f"{ret}")
    return ret


@app.route(f"/{os.environ['OBC_USER_ID']}/workflow/delete/<string:dag_id>", methods=['DELETE','GET'])
def delete_dag(dag_id):
    '''
    Get request from openBio platform
    which contains the file name, dag instructions
    '''
    # Parse data json to dict
    delete_result={}
    result={}
    dag_filename=f"{dag_id}.py" 
    delete_result= delete_dag_file(dag_id)
    result = delete_from_airflow(dag_id).json()
    # delete_result['status']="deleted"
    # print_f(f"{"error" in result['error']}")
    if "error" in result:
        print_f("Einai mesa")
        result["status"]="failed"
        result["dag_id"]=f"{dag_id}"
    else:
        result["status"]="failed"
        result["dag_id"]=f"{dag_id}"
        result["status"]="success"
        result["dag_id"]=f"{dag_id}"

    return result
     



def get_tool_OBC_rest(callback,tool_id, tl_name, tl_edit,tl_version):
    '''
    Send GET request to OBC REST to get the dagfile
    RETURN dag File contents
    0.0.0.0:8200 MUST BE CHANGED WITH THE MAIN OBC SERVER
    '''
    response = requests.get(f'{callback}rest/tools/{tl_name}/{tl_version}/{tl_edit}/?dag=true&tool_id={tool_id}')

    if response.status_code != 200:
        print_f(f"Error while retrieving data. ERROR_CODE : {response.status_code}")
        dag_contents['success']='false'
        dag_contents['error']=f"Error while retrieving data. ERROR_CODE : {response.status_code}"
    else:
        print_f("success")
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
        print_f(f"Error while retrieving data. ERROR_CODE : {response.status_code}")
        dag_contents['success']='false'
        dag_contents['error']=f"Error while retrieving data. ERROR_CODE : {response.status_code}"
    else:
        print_f("success")
        dag_contents=response.json()
    
    return dag_contents


def dag__trigger(id,name,edit):
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
    url = f"http://0.0.0.0:8080/{os.environ['OBC_USER_ID']}/api/experimental/dags/{id}/dag_runs"
    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache"
        }
    # TODO -> MUST BE CHANGED BETTER NOT TO USE WHILE !
    payload={} # Future changes for scheduling workflow
    effort = 0
    while True:
        effort += 1
        print_f (f'Effort: {effort}')
        response = requests.post(url,data=json.dumps(payload),headers=headers)
        print_f(f"{response.ok}")
        if response.ok == False:
            print_f (f'Response error:{response.status_code}')
            print_f (f'{json.dumps(response.json(), indent=4)}')
            time.sleep(1)
        else:
            break


    print_f("---> Response from airflow : ")
    print_f(response.json())
    return response.json()


@app.route(f"/{os.environ['OBC_USER_ID']}/run", methods=['POST'])
def run_wf():
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
    d = request.get_data()
    app.logger.info(str(d))
    data = json.loads(request.get_data())

    name = data['name']
    edit = data['edit']
    work_type = data['type']
    callback= data['callback']
    
    print_f(request.base_url)
    app.logger.info(data)
    if work_type == 'tool':
        tool_id = data['tool_id']
        version = data['version']
        dag_contents= get_tool_OBC_rest(callback,name,edit,version)
        try:
            if dag_contents['success']!='failed':
                generate_file(tool_id)
                payload['status']=dag__trigger(tool_id,name,edit)
            else:
                payload['status']='failed'
                payload['reason']=dag_contents
        except KeyError:
            print_f('Dag not found')
            payload=dag_contents
    elif work_type == 'workflow':
        workflow_id = data['workflow_id']
        dag_contents = get_workflow_OBC_rest(callback,name,edit,workflow_id)
        # try:
        if dag_contents['success']!='failed':
            generate_file(workflow_id,dag_contents['dag'])
            payload['status']=dag__trigger(workflow_id,name,edit)
        else:
            payload['status']='failed'
            payload['reason']=dag_contents
        # except KeyError:
        #     print_f('Dag not found')
        #     payload=dag_contents
    else:
        payload['status']="failed"
        payload['error']="Unknown type (worfkflow or tool)"
        # Set executor url 
    payload["executor_url"]=f"http://{os.environ['PUBLIC_IP']}:{os.environ['OBC_AIRFLOW_PORT']}/{os.environ['OBC_USER_ID']}"
    payload["monitor_url"]=f"http://{os.environ['PUBLIC_IP']}:{os.environ['OBC_EXECUTOR_PORT']}/{os.environ['OBC_USER_ID']}/monitoring"
    # print_f(f"{pa}"
    return json.dumps(payload)


@app.route(f"/{os.environ['OBC_USER_ID']}/check/id/<string:dag_id>", methods=['GET'])
def get_status_of_workflow(dag_id):
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

    url = f"http://{os.environ['PUBLIC_IP']}:8080/{os.environ['OBC_USER_ID']}/api/experimental/dags/{dag_id}/dag_runs"
    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache"
        }

    # payload={} # Future changes for scheduling workflow
    response = requests.get(url)

    

    # print_f("---> Response from airflow : ")
    # Check from database if the dag is changed! If it is ch
    paused_dags = [reg[0] for reg in execute_query("SELECT dag_id FROM dag WHERE is_paused").fetchall()]
    print_f(f"Paused dags : {paused_dags}")
    if response.ok == True:
        res=response.json()
        if dag_id in paused_dags:
            for dag in res:
                dag["state"]='paused'

        print_f(response.json())
    else:
        print_f("DAG NOT FOUND")
        res=[]    
    return json.dumps(res)



@app.route(f"/{os.environ['OBC_USER_ID']}/download/<string:dag_id>")
def downloadFile(dag_id):
    '''
        Download the result from workflow execution
        The data are seperated in three different folders TOOL,DATA,WORK

        dag_id : the id of dag that the user could take the reports
        filename : the name of file which the user want to download
        TODO -> Change in the future the filename because of replaced by compressed file that contains all results
    '''
    downloaded_path=f"{os.environ['AIRFLOW_HOME']}/REPORTS/WORK/{dag_id}.tgz"
    return send_file(downloaded_path, as_attachment=True)

def create_zipfile(content_path,zipped_path,name):
    '''
    The main usage of this function is to generate zip file containing logs from dag which they run.
    The log files are seperated into a folders, every folder was named according to the steps of dag.
    Path of logs /REPORTS/logs/<dag_id>/
    Path of compressed logs /REPORTS/logs/<dag_id>/<dag_id.zip>
    log_path = source of log folder
    zipped_path = source of zipped logs to be saved
    zipfile_name = is the name of dag (<dag_id>.zip)
    '''
    shutil.make_archive(f'{zipped_path}/{name}', 'zip', content_path)
    download_path = f"{zipped_path}/{name}.zip"
    return download_path

@app.route(f"/{os.environ['OBC_USER_ID']}/logs/<string:dag_id>")
def getLogs(dag_id):
    '''
        example:
        http://192.168.1.21:5000/d8a05e4b0d2a46b78dce482378d2c39d/logs/mitsos6

        Get the whole logs from workflow execution to zip type
        The logs of execution are seperated in different files (file per step)
        dag_id : the name of dag
    '''
    log_path= f"{os.environ['AIRFLOW_HOME']}/logs/{dag_id}" 
    destination_log_path = f"{os.environ['AIRFLOW_HOME']}/logs/compressed_logs"
    
    download_path= create_zipfile(log_path,destination_log_path,dag_id)
    return send_file(download_path, as_attachment=True)


@app.route(f"/{os.environ['OBC_USER_ID']}/workflow/<string:dag_id>/paused/<string:status>", methods=['GET'])
def pause_workfow(dag_id,status):
    '''
    ‘<string:status>’ must be a ‘true’ to pause a DAG and ‘false’ to unpause.
    '''

    url = f"http://{os.environ['PUBLIC_IP']}:8080/{os.environ['OBC_USER_ID']}/api/experimental/dags/{dag_id}/paused/{status}"
    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache"
        }

    response = requests.get(url)
    print_f("---> Response from airflow : ")
    return response.json()

def get_executor_id():
    '''
    When Netdata works as a container other containers which monitoring are with containers id
    To fix this problem we connect docker socket in executor container and we get the id of specific airflow container
    '''
    client=docker_setups()
    executor_name= f"executor_airflow_{os.environ['EXECUTOR_INSTANCE']}"
    return executor_name,client.containers.get(executor_name).id[0:12]



@app.route(f"/{os.environ['OBC_USER_ID']}/monitoring")
def monitoring_dashboard():
    """
    Landing page.
    """
    dags_info = [{'status': 'Total','out': f"{execute_query('SELECT COUNT(1) FROM dag').fetchone()[0]}"},
           {'status': 'Running','out': f"{execute_query('SELECT COUNT(1) FROM dag_run').fetchone()[0]}"},
           {'status': 'Paused','out': f"{execute_query('SELECT COUNT(1) FROM dag WHERE is_paused').fetchone()[0]}"}]
    # PUBLIC_IP=os.environ['PUBLIC_IP']
    suc_dags={'status':'Succeed', 'out':execute_query("SELECT COUNT(1) FROM dag_run WHERE state = 'success'").fetchone()[0]}
    failed_dags={'status':'Failed', 'out':execute_query("SELECT COUNT(1) FROM dag_run WHERE state = 'failed'").fetchone()[0]}
    print_f(f"{os.environ['PUBLIC_IP']}")
    executor_name, executor_id= get_executor_id()
    return render_template('index.html',
           title="OBC Executor Monitoring",
           public_ip=os.environ['PUBLIC_IP'],
           netdata_port=os.environ['NETDATA_MONITORING_PORT'], #TODO MAKE IT ENVIRONMENT VARIABLE
           executor_id=executor_id,
           executor_name=executor_name,
           failed_dags=failed_dags,
           suc_dags=suc_dags,
           dags_info=dags_info,
           obc_user_id=os.environ['OBC_USER_ID'],
           netdata_id=os.environ['NETDATA_ID']
           )


@app.route(f"/{os.environ['OBC_USER_ID']}/executor_info")
def dags_data():
    '''
    Get real time data relative of dags status
    '''
    def get_dag_data():
        while True:
            json_data= json.dumps(
                {   
                    # 'time':datetime.now(),
                    'total':execute_query('SELECT COUNT(1) FROM dag').fetchone()[0],
                    'running':execute_query('SELECT COUNT(1) FROM dag_run').fetchone()[0],
                    'paused':execute_query('SELECT COUNT(1) FROM dag WHERE is_paused').fetchone()[0],
                    'succeed':execute_query("SELECT COUNT(1) FROM dag_run WHERE state = 'success'").fetchone()[0],
                    'failed':execute_query("SELECT COUNT(1) FROM dag_run WHERE state = 'failed'").fetchone()[0]
                })
            yield f"data:{json_data}\n\n"

            time.sleep(10)
    return Response(get_dag_data(), mimetype='text/event-stream')
