# Airflow using Docker-compose
---

### Getting Started 
---
Instructions: 
- Clone repository
- Install prerequisites :
    - Docker
    - Docker-Compose
- Run the service
    - `docker-compose up`

- Open http://localhost:8080


### Airflow Sub-Commands
---
Run airflow sub-commands in docker-compose:
- List dags :
    - `docker-compose run --rm webserver airflow list_dags` 
- Test specific task :     
    - `docker-compose run --rm webserver airflow test [DAG_ID] [TASK_ID] [EXECUTION_DATE]`

## Credits
---
- [Apache Airflow](https://github.com/apache/incubator-airflow)
- [docker-airflow](https://github.com/puckel/docker-airflow/tree/1.10.0-5)


 

