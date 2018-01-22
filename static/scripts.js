$(document).ready(function() {
	
	// Builds a list from TempHistory filtered by amount of days selected by the user.
	$('#gethistory').submit(function() 
	{
		var url = Flask.url_for("gethistory")+"?loc="+$('#loc').val()+"&days="+$('#range').val();
		var results = "";

		$.getJSON(url, function(data) 
		{
			for (var i = 0; i < data.length; i++)
			{
				results += "<li class='list-group-item'>"
				+"<h5>Lämpötila: <span class='label label-default'>"+data[i].temp+"°C</span></h5>"
				+"<h5>Päivämäärä: <span class='label label-default'>"+data[i].date+"</span></h5>";
			}
			$('#historyresults').html(results);
		});
		return false;
	});
	
	// AJAX1 - Gets the last 10 results for the location to build a temperature graph
	// AJAX2 - Gets all time max/min/avg temperatures for the location
	$('#getlocation').submit(function()
	{
		var url = Flask.url_for("getlocation")+"?loc="+$('#loc').val()+"&lim="+$('#range').val();
			
		$.getJSON(url, function(tempquery)
		{
			var dates = [];
			var temps = [];

			var ctx = document.getElementById('tempChart').getContext('2d');
			
			for (var i = 0; i < tempquery.length; i++)
			{
				dates.push(tempquery[i].date);
				temps.push(tempquery[i].temp);
			}

			var tempChart = new Chart(ctx,{
				type: 'line',
				data: {
					labels: dates.reverse(),
					datasets: [{
						label: "Viimeiset havainnot (max "+$('#range').val()+")",
						fill: false,
						borderColor: 'rgb(173,216,230)',
						data: temps.reverse(),
					}]
				},
				options: {
					scales:
					{
						xAxes: [{
							display: false
						}]
					}
				}
			});
			
		});
		url = Flask.url_for("getrecords")+"?loc="+$('#loc').val()+"&lim="+$('#range').val();
		console.log(url);

		$.getJSON(url, function(recordquery)
		{
			if (recordquery.max != null)
			{
				$('#tempRecords').html("<div class='list-group'>"

				+"<li class='list-group-item'>"
				+"<h4 class='list-group-item-heading'>Uusin havainto</h4>"
				+"<p class='list-group-item-text'>"+recordquery.new+"&deg;C</p>" 
				+"</li>"

				+"<li class='list-group-item'>"
				+"<h4 class='list-group-item-heading'>Korkein lämpötila</h4>"
				+"<p class='list-group-item-text'>"+recordquery.max+"&deg;C</p>" 
				+"</li>"

				+"<li class='list-group-item'>"
				+"<h4 class='list-group-item-heading'>Matalin lämpötila</h4>"
				+"<p class='list-group-item-text'>"+recordquery.min+"&deg;C</p>"
				+"</li>"

				+"</div>");
			}
			else $('#tempRecords').html("");
		});
		return false;
	});
});
