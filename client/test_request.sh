curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"filename":"malakia","file":"the text for the generated file"}' \
  http://127.0.0.1:5000/generate_dag
