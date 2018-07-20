
$( document ).ready(function() {

	var ajaxDone; //create a global variable called ajaxDone
	$(document).ajaxStart(function() {
	    ajaxDone = false; //by default, set the ajax as not completed each time the ajax request is sent
	    setTimeout(function() { 
	        if(!ajaxDone) $("img#loading").show();
	    }, 500);

	}).ajaxSuccess(function() {
	    ajaxDone=true;//When the ajax request finishes, it sets ajaxDone to true
	    $("img#loading").hide();
	});

	$(".navLinkButton").click(function() {
	  	$(".nav.navbar-nav .navLinkButton").removeClass("active");
	  	$(this).addClass("active");
	});


});