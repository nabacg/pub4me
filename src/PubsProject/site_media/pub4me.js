$(function() {
	$("input.autocomplete").autocomplete({
        source: "pub_autocomplete",
		minLength: 2,
        select: function(event, ui){
			var nameInputId = $(this).attr("id");
			var idInputId = nameInputId.replace("name", "id");
			$("#"+idInputId).val(ui.item.id);
			$(".more").show();			
        }
    });
});

$(document).ready(function(){
		
	var $pubInput;
	
	var $last = $("input.autocomplete").last();
	        
    $(".more").click(function(){
    	$pubInput = $("input.autocomplete").eq(0).clone();
    	$(".primary").before($pubInput);   	
    	// $(".more").hide();
    	$("input.autocomplete").autocomplete({
            source: "pub_autocomplete",
    		minLength: 2,
            select: function(event, ui){  
        	//  $(".more").show();
            }
        });
    });
    
/*    
    $("#add_place_submit").click(function(){
        $(this).hide();
        $("#second_place_name").show();
        return false;
    });
    
    $("#second_place_name_submit").click(function(){
        $(this).hide();
        $("#second_place_name").hide();
        $("#result").show();
        return false;
    });
    
    $("#next").add("#been").click(function(){
        $("#result").hide('slow').find("#result_place").text('Betel');
        $("#result").show('slow');
        return false;
    });
*/
    
});
