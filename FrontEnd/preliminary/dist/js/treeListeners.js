$(document).ready(function() {
  // addTreeEventListeners();
});
// =================================================================
// 			Above Code Ensures that the JS isn't executed
// 			In case the HTML hasn't been loaded as we are
// 			Using async
// =================================================================


function uuidv4() {
  return ([1e7]+1e3+4e3+8e3+1e11).replace(/[018]/g, c =>
    (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
  )
}


function addTreeEventListeners() {
  // ![DEPRECATED] Commented Event Listener (blur)
  // // Event Listener to Catch the newly typed Foldername by User
  // $(".tree_item span[contenteditable]").blur(function(e) {
  //   console.log($(this).text());
  // });

  // Event Listener to control open/closing of folder branches in Tree
  $('.tree_icon').click(function (e) {
    var $this = $(this).parent();
    $this.next().toggle(300);   // This is where the main magic happens

    $this.toggleClass('tree_item--opened');   // CSS Class that serves as a flag
    if ($this.hasClass('tree_item--opened')) {    // A flag for this shit
      $this.children('.tree_icon')                // Just changing the icon
              .addClass('fa-folder-open')
              .removeClass('fa-folder');
    } else {
      $this.children('.tree_icon')
              .addClass('fa-folder')
              .removeClass('fa-folder-open');
    }
  });


  // This part just make sure to render a selected node (Active Node)
  // This can be modified to add multi-select abilities + Drag&Drop
  // :has(ul) searches all the child elements of the found element for a <ul>
  $('.tree_li').not(':has(> .tree_item--addBtn)').find('.tree_item').click(function(event) {
    if(!event.target.classList.contains("tree_icon")) {  // Ignore any clicks on the Folder icon
      $('.tree li')   // First, Remove the Active State of any other .tree_item
                  .find('.tree_item')
                  .not(this)
                  .removeClass('tree_item--active');
      // Finally, Toggle the active state of the Target .tree_item element
      $(this).toggleClass('tree_item--active');
    }
  })


  // "Add Item" Button Click Event Listener
  $(".tree_item--addBtn").click(function() {
    const ID = "F0000" + uuidv4();
    $(this).parent().before(`
      <li class="tree_li tree_parent" id="${ID}">
        <span class="tree_item">
          <i class="fa fa-folder tree_icon" aria-hidden="true"></i>
          <span>New Folder</span>
        </span>
        <ul class="tree_child-list">
          <li class="tree_li">
            <span class="tree_item tree_item--addBtn">
              <button class="fa fa-plus-circle"></button>
            </span>
          </li>
        </ul>
      </li>
    `);

    $(".tree").add('*').off("click blur"); // Drop all Event Listeners connected to the Tree
    addTreeEventListeners();   // Call function again to add listeners to newly added folder

    // if($(this).parent().parent().attr('id') === "tree") {
    //   var PID = $(this).parent().parent().attr('id');
    // }
    // else {
    //   var PID = $(this).parent().parent().parent().attr('id');
    // }
    // addDelta({
    //   id : ID,
    //   name : "New Folder",
    //   newPID : PID,
    // });
  });
}
