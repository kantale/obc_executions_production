# Import python dependencies for WF

import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime,timedelta
# Default arguments
'''
start_date: Allows you to specify certain tasks to start at a different time from the main DAG. 
end_date: Allows you to specify certain taskas to end at a different time from the main DAG.
depends_on_past: when set to True, keeps a task from getting triggered if the previous schedule for the task hasn't succeded.
'''


default_args = {
        'owner': 'airflow',
        'start_date': datetime.now(),
        'depends_on_past': True,
        'email': ['airflow@example.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        # If a task fails, retry it once after waiting at least 5 minutes
        # 'retries': 1,
        #'retry_delay': timedelta(minutes=5),
}


# Instantiate a DAG
'''
Give a DAG name, configure the schedule, and set the DAG setting
schedule_interval: Schedule you workflow according to when you want it.
(
    Presets: None, @once, @hourly, @daily, @weekly, @monthly, @yearly,
                         ( 0**** )( 00*** )( 00**0 )( 001** )( 0011* )
)
'''
dag= DAG(
        'example',             # dag name
        default_args=default_args,  # set the arguments in dag
        description= 'My first fantastic example',
        schedule_interval= '@once',
)


# Task
'''
This step is to lay out all the tasks in the workflow

t1,t2 and t3 are examples of tasks created by instantiating operators

We use BashOperator to execute commands in a Bash shell
t1 -> generate a test.txt file
'''
t1= BashOperator(
        task_id='generate_file',
        bash_command='echo $(pwd)',
        dag=dag,
)

t2= BashOperator(
        task_id='edit_file',
        bash_command= 'echo i write inside >> test.txt',
        dag=dag,
)

t3= BashOperator(
        task_id='wait',
        bash_command= 'sleep 5',
        dag=dag,
)
# we could use a variable which contains the commands.Also we could use and Jinja Template adding parameters as below:
command_template="""
{% for i in range(1) %}
    echo "{{ params.my_param }}"
    echo "{{ ds }}"
{% endfor %}
"""

t4= BashOperator(
        task_id= 'templated',
        #depend_on_past=False,
        bash_command=command_template,
        params={'my_param': 'This fantastic param passed in successfully'},
        dag=dag,
)

# Setting up Dependencies
'''
Set the dependencies or the order in which the tasks should be executed.
Here are a few ways you can define dependencies between them:
'''

# This means that t2 will depend on t1
# running successfully to run.
# t1.set_downstream(t2)
# similas to above where t3 will depend on t1
# t3.set_upstream(t1)


# The bit shift operator can also be used to chain operations:
t1 >> t2 >> t3 >> t4

# And the upstream dependency with the bit shift operator:
# t2 << t1

# A list of tasks can also be set as
# dependencies. These operations
# all have the same effect:
# t1.set_downstream([t2, t3])
# t1 >> [t2, t3]
# [t2, t3] << t1



