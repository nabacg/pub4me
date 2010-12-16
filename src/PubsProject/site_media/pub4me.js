$(function() { 
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
	
	$('form.pubs div').formset({
		addText: '+ dodaj kolejną',
		addCssClass: 'addformlink',
		deleteCssClass: 'removeformlink',
		added: function (row) {
		row.find(".autocomplete").autocomplete({
			source: "pub_autocomplete",
			minLength: 2,
			select: pubSelect
		});	
		row.find(".autocomplete").autocomplete("enable");
		}
    });
	
	$(".autocomplete").autocomplete({
        source: "pub_autocomplete",
		minLength: 2,
        select: pubSelect
    });
	
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
