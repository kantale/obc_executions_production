# Ip which airflow in docker-compose run is 172.18.0.5:8080
# Ip which client in docker-compose run in 172.18.0.4:5000


# Check the status of airflow server 

curl --header "Content-Type: application/json" \
	--request GET \
	http://172.18.0.5:8080/api/experimental/test

# Get the statuses from workflow (step by step)


curl --header "Content-Type: application/json" --request GET http://172.18.0.5:8080/api/experimental/dags/pca_plink_and_plot__1/dag_runs

