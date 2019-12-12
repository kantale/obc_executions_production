#  Openbio Executor 
#  using Docker-compose
---

### Getting Started 
---
Instructions: 
- Clone repository
- Install prerequisites :
    - Docker
    - Docker-Compose
    - Install prerequisites simply running the file `install.sh`
- Run the service
    - `docker-compose up` with logging or `docker-compose up -d` without logging

- Open http://localhost:8080


### Airflow Sub-Commands
---
Run airflow sub-commands in docker-compose:
- List dags :
    - `docker-compose run --rm webserver airflow list_dags` 
- Test specific task :     
    - `docker-compose run --rm webserver airflow test [DAG_ID] [TASK_ID] [EXECUTION_DATE]`
- Run shell of airflow container : 
    - `docker exec -it docker-airflow_airflowserver_1 bash`

### Client 
---
OpenBioC Client (Flask): 
- Dag generation remotely via requests


