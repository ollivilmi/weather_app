$(document).ready(function() {
	
	$('#gethistory').submit(function() 
	{
		var url = Flask.url_for("gethistory")+"?loc="+$('#loc').val()+"&days="+$('#days').val();
		var results = "";

		$.getJSON(url, function(data) 
		{
			console.log(data);
			for (var i = 0; i < data.length; i++)
			{
				results += "<p>Lämpötila: "+data[i].temp+"°C, pvm: "+data[i].date+"</p>";
			}
			$('#historyresults').html(results);
		});
		return false;
		
	});
});
