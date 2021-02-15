$('.acc-btn').click(function(){
	alert("aiueo")
	if ( $(this).next().is( ":hidden" ) ) {
		$('.acc-content').slideUp('selected');
		$(this).next().slideDown('selected');
	} else {
		$(this).next().slideUp('selected');
	}
});// JavaScript Document