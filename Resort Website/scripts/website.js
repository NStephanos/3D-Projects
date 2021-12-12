

$(document).ready(function() {


	$("#slideshow > div:gt(0)").hide();

	setInterval(function() { 
	 	$('#slideshow > div:first')
	 		.fadeOut(1000)
			.next()
			.fadeIn(1000)
			.end()
			.appendTo('#slideshow');
	}, 3000);

	function datecheck(){

		let startdate = Date.parse($("#tripstart").val());
		let enddate = Date.parse($("#tripend").val());

		let datetrue = enddate - startdate;

		if (datetrue > 0) {
			return true;
		};
		return false;

	};

	$( "#bookform" ).submit(function( event ) {
	  $( "#hidden" ).hide();
	  if (datecheck() == true) {

	  	alert( 'Booking Successful!' );
	    $( "#hidden" ).text( "Dates Booked" ).show();
	    event.preventDefault();
	    return;
	  };
	 
	  $( "#hidden" ).text( "Invalid Dates..." ).show();
	  event.preventDefault();
	});

});

	function initMap() {
	// The location of Uluru
	const resort = { lat: 69, lng: 69 };
	// The map, centered at Uluru
	const map = new google.maps.Map(document.getElementById("map"), {
	  zoom: 5,
	  center: resort,
	});
	// The marker, positioned at Uluru
	const marker = new google.maps.Marker({
	  position: resort,
	  map: map,
	});
}

