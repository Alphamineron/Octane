$(function() {
    addSidebarListeners();
});


function addSidebarListeners() {
    // Button Event Listeners

    $("#menu-toggle").click(function(e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
    });

    $("#tree-refresh").click(function(e) {
        console.log("Refresh Init");
        e.preventDefault();
        fetchTreeFromJSON = true;   // Toggle Boolean Flag
        refreshTree();
    });
}