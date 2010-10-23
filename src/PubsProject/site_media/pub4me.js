$(function() {
	$("input.autocomplete").autocomplete({
        source: "pub_autocomplete",
		minLength: 2,
        select: function(event, ui){
			var nameInputId = $(this).attr("id");
			var idInputId = nameInputId.replace("name", "id");
			$("#"+idInputId).val(ui.item.id);
        }
    });
});

$(document).ready(function(){
		        
});
