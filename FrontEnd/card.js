let $recentTarget, tags;

function catchTargetCard($target) {
    if($target.is(".card-btn")) $recentTarget = $target.parent();
    else $recentTarget = $target.parent().parent();
}

function renderCardContextMenu(event) {

        if(event.target.matches('.card-btn, .card-btn i')) {
            catchTargetCard($(event.target));
            event.preventDefault();

            $(".card-menu").finish().toggle(100).css({
                top: event.pageY + "px",
                left: event.pageX + "px"
            });
        }
}

function editCard() {
	console.log($recentTarget.attr('id'));
	$(".card-img, .card-info").hide(150);
	$(".card").append(`
		<div class="txtInput">
			<input type="text" class="txtBox">
			<label id="name" class="placeholder">Name</label>
		</div>

		<div class="txtInput">
			<input type="text" class="txtBox">
			<label id="folder" class="placeholder">Folder</label>
		</div>

		<div class="txtInput urlInput">
			<input type="text" class="txtBox" name="other3" id="other3">
			<div class="urlIcon">http://</div>
			<label for="other3" class="placeholder">Other Link</label>
		</div>

		<div class="txtInput">
			<label>Phase</label>
			<select id="Phase" class="txtBox">
				<option>Unassigned</option>
				<option>Phase 1</option>
				<option>Phase 2</option>
				<option>Phase 3</option>
				<option>Phase 4</option>
				<option>Phase 5</option>
				<option>Phase 6</option>
			</select>
		</div>

		<div class="txtInput">
			<label>Status</label>
			<select id="status" class="txtBox">
				<option>Unassigned</option>
				<option>ToDo</option>
				<option>InProgress</option>
				<option>Done</option>
			</select>
		</div>

		<input class="taggedTemp" type="text" placeholder="_______"/>

		<div class="txtInput">
			<textarea type="text" class="txtArea"></textarea>
			<label id="description" class="placeholder">Description</label>
		</div>
	`);
	var tagsTemp = new Tags('.taggedTemp');
	tagsTemp.addTags(tags.getTags());

	const array = [".txtBox", ".txtArea"];
	array.forEach(function (item) {
		addFocusEventListeners(item);
	});

}

function removeCard() {
	var result = confirm("Delete this card permanently?");
	if (result) {
		console.log($recentTarget.attr('id'));
		$recentTarget.remove();
	}
}


$(document).ready(function() {
    $(document).bind("click", renderCardContextMenu);	// Bubbling Events up the DOM tree to avoid add many eventlisteners


    $(document).bind("mousedown", function (e) {
        if (!$(e.target).parents(".card-menu").length > 0) {
            $(".card-menu").hide(100);  // Runs when clicking anywhere but the contextmenu
        }
    });


    const menu = document.querySelectorAll(".card-menu li");
    menu.forEach(element => {
        element.addEventListener("click", function(){

            switch($(this).attr("data-action")) {

                case "edit":    editCard();
                                break;
                case "remove":  removeCard();
                                break;
            }

            $(".card-menu").hide(100);
        });
	});
});


document.addEventListener("DOMContentLoaded", function(event) {
    tags = new Tags('.tagged');
	tags.addTags(['Tag1', 'Tag2', 'Tag3']);

	$('.card-img').bind("click", addStar);
});


function addStar(){
    this.classList.toggle('card-starred');
}



