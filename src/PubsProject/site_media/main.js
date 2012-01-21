
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
		
		
$(function() {	

	$("#recommend_submit").click(function(){
		$("#pubs_form").submit();
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
