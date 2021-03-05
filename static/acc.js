$(document).on("click",'.acc-btn',function(){
	if ( $(this).next().is( ":hidden" ) ) {
		$('.acc-content').slideUp('selected');
		$(".acc-btn").removeClass("active");
		$(this).next().slideDown('selected');
		$(this).toggleClass("active");
	} else {
		$(this).next().slideUp('selected');
		$(this).removeClass("active");
	}
});// JavaScript Document