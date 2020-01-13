curl --header "Content-Type: application/json" \
  --request POST \
  --data '{
	"dag_name":"pca_plink_and_plot__1", 
	"owner":"Manos"}' \
  http://172.18.0.4:5000/trigger_dag
