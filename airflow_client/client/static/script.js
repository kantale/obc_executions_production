$(document).ready(function () {
		const source = new EventSource("executor_info");

		//Attribute that contains the statuses
		var total = $("#Total_num");
		var running = $("#Running_num");
		var paused = $("#Paused_num");
		var succeed = $("#Succeed_num");
		var failed = $("#Failed_num")
		//grap the data as a json
		source.onmessage = function(e) {
			data =JSON.parse(e.data)
		  	// Set the dag status in htm
		  	var m = $("#dags_info");
			total.html(data.total);
			running.html(data.running);
			paused.html(data.paused);
			succeed.html(data.succeed);
			failed.html(data.failed);
		}   

})
