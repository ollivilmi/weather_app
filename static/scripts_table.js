$(function() {

	// Script for creating the table
    var url = Flask.url_for("getallrecords")+"?hours=24";
    var results = "";

    $.getJSON(url, function(data) 
    {
        for (var i = 0; i < data.length; i++)
        {
            results += "<tr>"
            +"<th scope='row'>"+data[i].loc+"</th>";
            
            if (data[i].max != null)
                results += "<td>"+data[i].max+"&deg;C</td>";
            else
                results += "<td> - </td>";
            
            if (data[i].min != null)
                results += "<td>"+data[i].min+"&deg;C</td>";
            else
                results += "<td> - </td>";

            if (data[i].avg != null)
                results += "<td>"+data[i].avg+"&deg;C</td>";
            else
                results += "<td> - </td>";              
            
            results += "<td>"+data[i].cur+"&deg;C</td>"    
            +"<td>"+data[i].date+"</td>"
            +"</tr>";
        }
        $('#indextable').html(results);
    });
    return false;
});