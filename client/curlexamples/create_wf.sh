curl --header "Content-Type: application/json" \
  --request POST \
  --data '{
        "name":"test",
	"edit":"1",
	"type":"workflow",
        "callback":"http://192.168.1.21:8200/platform/",
        "workflow_id":"test"}' \
  http://192.168.1.21:5000/d8a05e4b0d2a46b78dce482378d2c39d/run
