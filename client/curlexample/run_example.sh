curl --header "Content-Type: application/json" \
  --request POST \
  --data '{
	"dag_name":"pca_plink_and_plot__1", 
	"owner":"Manos"}' \
  http://139.91.81.103:5000/trigger_dag
