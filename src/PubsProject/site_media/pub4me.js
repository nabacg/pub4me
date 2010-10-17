$(document).ready(function(){
    $("input.autocomplete").autocomplete({
        source: "pub_autocomplete",
		minLength: 2,
        select: function(event, ui){
            $("#first_place").replaceWith('<p class="place_result">Lubisz: ' + ui.item.value + '</p>');
            $("#second_place").show(500);

            $("input#second_place_name").autocomplete({
                source: "pub_autocomplete",
				minLength: 2,
                select: function(event, ui){
                    $(".info").hide();
                    $("#second_place_name").replaceWith('<p class="place_result">Lubisz: ' + ui.item.value + '</p>');
                }
            });
        }
    });
    
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
    
});
