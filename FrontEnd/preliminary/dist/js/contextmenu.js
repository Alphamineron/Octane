let $recentTarget;
function catchTargetFolder($target) {
    // Since we limit the rendering of the contextmenu, only need these two situations
    if($target.is("span.tree_item")) $recentTarget = $target.parent(); 
    else $recentTarget = $target.parent().parent(); 
}

$(document).ready(function() {
    // Trigger action when the contextmenu is about to be shown
    $(document).bind("contextmenu", function(event) {
        let clickableElements = document.querySelectorAll(".tree_item *, .tree_item");
        clickableElements.forEach(element => {

            var x = event.clientX, y = event.clientY,                   // Check if elementMouseIsOver is
            elementMouseIsOver = document.elementFromPoint(x, y);       // one of the allowed ones or not
            if(elementMouseIsOver == element && !elementMouseIsOver.classList.contains("tree_item--addBtn")) {
                // Update $recentTarget for use by the menu options
                catchTargetFolder($(event.target)); 
                // Avoid the Browser's Default ContextMenu
                event.preventDefault();
                // Show contextmenu at the mouse position
                $(".tree_menu").finish().toggle(100).css({
                    top: event.pageY + "px",
                    left: event.pageX + "px"
                });
            }
        });
    });


    // To hide contextmenu for when the document is clicked somewhere
    $(document).bind("mousedown", function (e) {
        // If the clicked element is not the menu
        if (!$(e.target).parents(".tree_menu").length > 0) {
            $(".tree_menu").hide(100);  // Runs when clicking anywhere but the Treecontextmenu
            // $recentTarget = null;  // This interferes with saveState.js functions, hence commented out
        }
    });


    // To Handle the menu options (JQuery Implementation was working for some reasons...)
    const menu = document.querySelectorAll(".tree_menu li");
    menu.forEach(element => {
        element.addEventListener("click", function(){
            // This is the triggered action name
            switch($(this).attr("data-action")) {
                
                // A case for each action. Your actions here
                case "edit": break;   // Edit's Functionality is handled in the modal.js
                case "remove": $recentTarget.remove(); updateTreeState(); break;
            }
            // Hide it AFTER the action was triggered
            $(".tree_menu").hide(100);
        });
    });
});