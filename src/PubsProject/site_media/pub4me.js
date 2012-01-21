
//zapisuje nowa, nieaktywna knajpe o nazwie pubName i domyslnych parametrach
var pubCreate = function (pubName) {
		$.ajax({
				type: "POST",
				url: 'pub_create',
				data: {name: pubName},
				success: function(data){
					//console.log('yay!');	
				}
			});
}
	
var onblurHandler = function (e) {
		var searchInput = $(this),
		searchValue = searchInput.val();
		
		if (searchValue && !searchInput.attr('pubSelected') && searchValue != ''){
			pubCreate(searchInput.val());
		}
	}

//Jezeli wcisnieto <ENTER> i tekst wpisany do inputa nie jest pusty, to dodajemy kolejne pole
var onKeyPressHandler = function(key){
	if (key.which == 13){
		if($(this).val() != "")
			addNewRow();
	} 
}

//dodaje nowy input do wybrania knajpy
var addNewRow = function(){
	$(".addformlink").click();
} 
		
var registerAutocompleteHandlers = function(){
	$(".autocomplete").myautocomplete();
	$(".autocomplete").blur(onblurHandler);
	$(".autocomplete").keypress(onKeyPressHandler);
}
		
$(function() {	
	$('form.pubs div.pub_field').formset({
		addText: '+ dodaj kolejną',
		addCssClass: 'addformlink',
		deleteCssClass: 'removeformlink',
		added: function (row) {
			registerAutocompleteHandlers();
			row.find(".autocomplete").autocomplete("enable");
			row.find(".autocomplete").focus();
		}
    });
	
	registerAutocompleteHandlers();
	
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
