$(function() {

    function createTable(data, hours) 
    {
        $('#hourvalue').html(hours + " tuntia");
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
            
            results += "<td class='curtemp'>"+data[i].cur+"&deg;C"
            +"<span class='tooltiptext'>"+data[i].date+"</span></td>"
            +"</tr>";
        }
        $('#indextable').html(results);
    }

	// Script for creating the table
    var url = Flask.url_for("getallrecords")+"?hours=24";
    var results = "";

    $.getJSON(url, function(data){
        createTable(data, 24);
    });
    
    $('#changetable').submit(function(){

        url = Flask.url_for("getallrecords")+"?hours="+$('#range').val();
        results = "";

        $.getJSON(url, function(data){
            createTable(data, $('#range').val());
        });
        return false;
    });
});