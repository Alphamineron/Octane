if (document.readyState == "loading")
	document.addEventListener("DOMContentLoaded", ready);
else ready();
// =================================================================
// 			Above Code Ensures that the JS isn't executed
// 			In case the HTML hasn't been loaded as we are
// 			Using async
// =================================================================

let folders;   // Global Variable

function ready() {
  if(treeStateAvailable()) {
    folders = getTreeState();
    main();
  }
  else {
    const endpoint = "../../../data/folderTree.json";
    fetch(endpoint)
        .then(response => response.json())
        .then(function(data) {
            folders = data;
            main();
        })
        .catch(err => console.log(err));
  }
}

function returnTreeHTML(folder) {
	// I don't like putting large strings in my funcs' logic, so I make a func
	// for the strings... <Big Brain Time>
    return `
        <li class="tree_li tree_parent" id="${folder["id"]}">
          <span class="tree_item">
            <i class="fa fa-folder tree_icon" aria-hidden="true"></i>
            <span>${folder["name"]}</span>
          </span>
          <ul class="tree_child-list">
            <li class="tree_li">
              <span class="tree_item tree_item--addBtn">
                <button class="fa fa-plus-circle"></button>
              </span>
            </li>
          </ul>
        </li>
    `;
}

function populateTree(ele, parentFolderList = folders) {
  // Remove the "Add Item" btn, so we can append data to the tree in the
  // right order without having the "Add Item" btn be the first item in tree
  var li_addBtn = ele[0].querySelector("li.tree_li > .tree_item--addBtn").parentNode
  li_addBtn.remove();

  // Loop through the current level in the folder dictionary/tree and append it in HTML
  parentFolderList.forEach(dict => {
    folder = {
      "id": dict["id"],
      "name": dict["name"],
      "children": dict["children"]
    }
    ele.append(returnTreeHTML(folder));

	// If "children" exists then go recursive by selecting the child list
    if (Array.isArray(folder["children"]) && folder["children"].length) { // children exists and is not empty
      var $childFolders = ele.children("#" + folder["id"]).children("ul.tree_child-list");
      populateTree($childFolders, folder["children"]);
    }
  });

  // Add the "Add Item" btn again after being done appending all folders in the
  // current level, in the end of the current level within the tree as much
  // deep we might be in the tree(as we are using recursion)
  ele[0].append(li_addBtn);
}

function main() {
    var $tree = $("#tree");	  // If you need this comment, You gotta learn jQuery bud (At least Google it)...
    populateTree($tree);	// Sort of Obvious what this func does

    $(".tree").add('*').off();	// Clean Tree's EListeners, to avoid attaching multiple EListeners to the same element
    addTreeEventListeners();	// Attach EListeners to the Tree's elements

    var Containers = document.querySelectorAll("ul.tree, ul.tree ul.tree_child-list");
    Containers.forEach(container => {
      drake.containers.push(container);      
    });
}
