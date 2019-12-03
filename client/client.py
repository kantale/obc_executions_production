import os
import urllib
from flask import Flask
from flask import request
import json
import os 
from datetime import datetime


dag_directory = "../dags"
def create_filename(name):
    return name, os.path.join(dag_directory, f'{name}.py')


def generate_dag_file(name,instructions):
    '''
    Get the data from request to generate the dag file
    name : The name of file to be generated
    instruction : The  contents of file to be generated
    '''
    ret={}
    filename,filename_path = create_filename(name)
    
    # Save the dag_file
    with open(filename_path,'w') as dag_file:
        dag_file.write(instructions)
    ret['generate_date'] = datetime.now()
    
    return "congrats"



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/generate_dag', methods=['POST'])
    def generate_dag():
        '''
        Get request from openBio platform
        which contains the file name, dag instructions
        '''
        # Parse data json to dict
        data = json.loads(request.get_data().decode())
        
        filename = data['filename']
        file_content = data['bash']
        pyfile = urllib.parse.unquote(file_content)
        gen_result = generate_dag_file(filename,pyfile)
        return gen_result

    

    return app
