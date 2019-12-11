curl --header "Content-Type: application/json" \
  --request POST \
  --data '{
	"dag_name":"pca_plink_and_plot__1", 
	"owner":"Manos"}' \
  http://0.0.0.0:5000/trigger_dag
