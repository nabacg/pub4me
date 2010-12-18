$(function() {
	
	var $div;
	
	jQuery.fn.myautocomplete = function() {
	    $(this).autocomplete({
			source: function( request, response ) {
				$.getJSON( "pub_autocomplete", request, function(data){					
					response(data);
					if (data.length == 0) $div.find('.notify').show();
					if (data.length > 0) $div.find('.notify').hide();
				});
			},
			minLength: 2,
			search: function(event, ui) {			
				$div = $(this).parent();
			},
		    select: function(event, ui){
				var nameInputId = $(this).attr("id");
				var idInputId = nameInputId.replace("name", "id");
				$("#"+idInputId).val(ui.item.id);
		    }
		});
	};
	
	$(".autocomplete").myautocomplete();	
	
	$('form.pubs div').formset({
		addText: '+ dodaj kolejną',
		addCssClass: 'addformlink',
		deleteCssClass: 'removeformlink',
		added: function (row) {
		row.find(".autocomplete").myautocomplete();
		row.find(".autocomplete").autocomplete("enable");
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
