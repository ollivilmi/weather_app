$(document).ready(function() {
	
	$('#gethistory').submit(function() 
	{
		var url = Flask.url_for("gethistory")+"?loc="+$('#loc').val()+"&days="+$('#days').val();
		var results = "";

		$.getJSON(url, function(data) 
		{
			for (var i = 0; i < data.length; i++)
			{
				results += "<p>Lämpötila: "+data[i].temp+"°C, pvm: "+data[i].date+"</p>";
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
						label: "Latest temperatures",
						backgroundColor: 'rgb(255, 99, 132)',
						borderColor: 'rgb(255, 99, 132)',
						data: temps.reverse(),
					}]
				},
			});
			
		});
		return false;
	});
});
