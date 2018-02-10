$(document).ready(function() {
	
	// Builds a list from TempHistory filtered by amount of days selected by the user.
	$('#gethistory').submit(function() 
	{
		var url = Flask.url_for("gethistory")+"?loc="+$('#loc').val()+"&days="+$('#slidervalue').val();
		var results = "";

		$.getJSON(url, function(data) 
		{
			for (var i = 0; i < data.length; i++)
			{
				results += "<li class='list-group-item'>"
				+"<h5>Päivämäärä: "+data[i].date+"</h5>"
				+"<p>Max: "+data[i].max+"</p>"
				+"<p>Min: "+data[i].min+"</p>"
				+"<p>Keskiarvo: "+data[i].avg+"</p></li>";
			}
			$('#historyresults').html(results);
		});
		return false;
	});
	
	// AJAX1 - Gets the last 10 results for the location to build a temperature graph
	// AJAX2 - Gets all time max/min/avg temperatures for the location
	$('#getlocation').submit(function()
	{
		var url = Flask.url_for("getlocation")+"?loc="+$('#loc').val()+"&lim="+$('#slidervalue').val();
		$('#locrecords').css("display", "block");
		
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
						label: "Viimeiset havainnot (max "+$('#slidervalue').val()+")",
						fill: false,
						borderColor: 'rgb(220,53,69)',
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
		url = Flask.url_for("getrecords")+"?loc="+$('#loc').val()+"&lim="+$('#slidervalue').val();
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
