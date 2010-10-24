$(function() {
	
	$('form.pubs div').formset({
		addText: '+ dodaj kolejną',
		addCssClass: 'addformlink',
		deleteCssClass: 'removeformlink',
		added: function (row) {
		row.find(".autocomplete").autocomplete({
	        source: "pub_autocomplete",
			minLength: 2,
	        select: function(event, ui){
				var nameInputId = $(this).attr("id");
				var idInputId = nameInputId.replace("name", "id");
				$("#"+idInputId).val(ui.item.id);
	        }
	    	});	
			row.find(".autocomplete").autocomplete("enable");
		}
    });
	
	$(".autocomplete").autocomplete({
        source: "pub_autocomplete",
		minLength: 2,
        select: function(event, ui){
			var nameInputId = $(this).attr("id");
			var idInputId = nameInputId.replace("name", "id");
			$("#"+idInputId).val(ui.item.id);
        }
    });
});
