$(document).ready(function() {
	
	$('#gethistory').submit(function() {
		
		$.getJSON(Flask.url_for("gethistory")+"?h="+$('#loc').val()
		.done(function(data, textStatus, jqXHR) {
			
		});
	});
	}
}
