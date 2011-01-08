jQuery.fn.myautocomplete = function() {
	var $div;
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
	    select: pubSelect
	});
};
var pubSelect = function (event, ui) {
		var nameInputId = $(this).attr("id");
		var idInputId = nameInputId.replace("name", "id");
		$("#"+idInputId).val(ui.item.id);
		$.ajax({
				type: "POST",
				url: 'pub_selected',
				data: ui.item,
				success: function(data){
					console.log('yay!');	
				}
			});
	}

$(function() {	
	$('form.pubs div.pub_field').formset({
		addText: '+ dodaj kolejną',
		addCssClass: 'addformlink',
		deleteCssClass: 'removeformlink',
		added: function (row) {
			$(".autocomplete").myautocomplete();	
			row.find(".autocomplete").autocomplete("enable");
		}
    });
	
	$(".autocomplete").myautocomplete();

	$(".primary").click(function(){
		$("form#"+$(this).attr("rel")).submit();
		return false;
	});
	
	
	$("#pubs_form").submit(function(){
		var recommendList = $("#recommendList");
		
		$.ajax({
			type: "POST",
			url: "pub_recommend",
			data: $("#pubs_form").serialize(),
			success: function(data){
				recommendList.empty();
				var data = eval('(' + data + ')');
				for(var i = 0; i < data.length; i++)
				{
					var pub = $('<li></li>').text(data[i]);
					pub.appendTo(recommendList);
				}				
			}
		});
		return false;
	});
});
