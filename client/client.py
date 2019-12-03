import os
import urllib
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json
import os 
from datetime import datetime


# Init app
app = Flask(__name__)


# Run server
if __name__ == '__main__':
    #debug is true for dev mode
    app.run(debug=True)


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
