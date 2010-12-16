$(function() {
	
	var $div;
	
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
		source: function( request, response ) {
			$.getJSON( "pub_autocomplete", 
				request, 
				function(data){
					response(data);
					if (data.length == 0) {
						$('.notify').show();
					}
				}
			);
		},
		minLength: 2,
		search: function(event, ui) {
			$div = $(this);
		},
        select: function(event, ui){
			var nameInputId = $(this).attr("id");
			var idInputId = nameInputId.replace("name", "id");
			$("#"+idInputId).val(ui.item.id);
        }
    });
	
	$(".primary").click(function(){
		$("form#"+$(this).attr("rel")).submit();
		return false;
	});
	
	
	$("#pubs_form").submit(function(){
		$.ajax({
			type: "POST",
			url: "pub_recommend",
			data: $("#pubs_form").serialize(),
			success: function(data){
				window.alert(data);				
			}
		});
		return false;
	});
});
