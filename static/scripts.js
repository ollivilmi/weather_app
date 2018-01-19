$(document).ready(function() {
	
	$('#gethistory').submit(function() 
	{
		var url = Flask.url_for("gethistory")+"?loc="+$('#loc').val()+"&days="+$('#days').val();
		var results = "";

		$.getJSON(url, function(data) 
		{
			for (var i = 0; i < data.length; i++)
			{
				results += "<li class='list-group-item'>Lämpötila: "+data[i].temp+"°C, pvm: "+data[i].date+"</li>";
			}
			$('#historyresults').html(results);
		});
		return false;
	});
	
	$('#getlocation').submit(function()
	{
		var url = Flask.url_for("getlocation")+"?loc="+$('#location').val();
			
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
						label: "Uusimmat havainnot",
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
		url = Flask.url_for("getrecords")+"?loc="+$('#location').val();

		$.getJSON(url, function(recordquery)
		{
		$('#tempRecords').html("<li class='list-group-item'>Korkein: "+recordquery.max+"&deg;C</li>"
		+"<li class='list-group-item'> Matalin: "+recordquery.min+"&deg;C</li>"
		+"<li class='list-group-item'> Keskiarvo: " +Math.round(recordquery.avg*100)/100+"&deg;C</li>");

		});
		return false;
	});
});
