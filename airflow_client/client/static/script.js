
// //Set the source which collect the data 
// var source = new EventSource('executor_info');

// function lineChartGen(name,xName,yName){
// 	const config = {
//             type: 'line',
//             data: {
//                 labels: [],
//                 datasets: [{
//                     label: "Random Dataset",
//                     backgroundColor: 'rgb(255, 99, 132)',
//                     borderColor: 'rgb(255, 99, 132)',
//                     data: [],
//                     fill: false,
//                 }],
//             },
//             options: {
//                 responsive: true,
//                 title: {
//                     display: true,
//                     text: name
//                 },
//                 tooltips: {
//                     mode: 'index',
//                     intersect: false,
//                 },
//                 hover: {
//                     mode: 'nearest',
//                     intersect: true
//                 },
//                 scales: {
//                     xAxes: [{
//                         display: true,
//                         scaleLabel: {
//                             display: true,
//                             labelString: xName
//                         }
//                     }],
//                     yAxes: [{
//                         display: true,
//                         scaleLabel: {
//                             display: true,
//                             labelString: yName
//                         }
//                     }]
//                 }
//             }
//         };

//     return config;

// }
$(document).ready(function () {
// 		// CPU CHART
//         const config = lineChartGen("name","Time","Percentage")
//         // console.log(config)

//         const context = document.getElementById('cpu_canvas').getContext('2d');

//         const lineChart = new Chart(context, config);

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
		  	// console.log(data.time);
		  	// Set the dag status in htm
		  	var m = $("#dags_info");
			total.html(data.total);
			running.html(data.running);
			paused.html(data.paused);
			succeed.html(data.succeed);
			failed.html(data.failed);

			// // Set the chart
			// if (config.data.labels.length === 20) {
   //              config.data.labels.shift();
   //              config.data.datasets[0].data.shift();
   //          }
   //          config.data.labels.push(new Date(data.cpu.last_entry).toLocaleTimeString().substring(0,8));
   //          config.data.datasets[0].data.push(data.value);
   //          lineChart.update();
		}   

})

// function LoadCharts(){
// 	var url="http://213.239.220.77:19999/api/v1/data?chart=cgroup_d1054903d245.cpu&after=-60&format=datasource&options=nonzero"
// 	google.charts.load('visualization', {'packages':['corechart']});
// 	google.charts.setOnLoadCallback(drawChart);
// 	function drawChart() {

// 		var query = new google.visualization.Query(url, {sendMethod: 'auto'});

// 		var chart = new google.visualization.AreaChart(document.getElementById('chart_div'));

// 		var options = {
// 		  title: 'test',
// 		  isStacked: 'absolute',
// 		  vAxis: {minValue: 100}
// 		};

// 		setInterval(function() {
// 		  query.send(function(data) {
// 		  	chart.draw(data.getDataTable(), options);
// 		    });
// 		}, 1000);
// 	}	
// }


// LoadCharts();