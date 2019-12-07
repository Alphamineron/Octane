function hidePlaceholder($target) {
	if($target.val() !== "") {
		$target.nextAll(".placeholder").first().addClass("focused");
		$target.nextAll(".urlIcon").first().addClass("focused");
	}
	else {
		$target.nextAll(".placeholder").first().removeClass("focused");
		$target.nextAll(".urlIcon").first().removeClass("focused");
	}
}

function addFocusEventListeners(targetclass) {
		$(targetclass).on("focusout", function(e) {
                hidePlaceholder($(e.target));
		});
	
		$(targetclass).on("focusin", function(e) {
				$(e.target).nextAll(".placeholder").first().addClass("focused");
				$(e.target).nextAll(".urlIcon").first().addClass("focused");
		});
}

$(document).ready(function() {
	// console.log( "ready!" );
	// const array = [".txtBox", ".txtArea"];
	// array.forEach(function (item) {
	// 	addFocusEventListeners(item);
	// });
});

