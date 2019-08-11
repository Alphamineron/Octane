window.addEventListener("beforeunload", function(e){
    updateTreeState();      // Save Tree State before the page reloads or closes
}, false);


//                      Logic Behind JS-Based StateSaving
//  foo() captures user's intended changes and calls addDelta() method
// 
//      foo()  -->  addDelta()  ------ deltaObj -----> delta[] ---->  handleDeltaList()
//        |                                                                   |
//        |                                                                   |
//        V                                                                   V
//   DOM_updated_Realtime (Light)                                    JSON_updated (Heavy)

let delta = []  // For Later implementation of "undo"


function addDelta(type, args) {
    if(type == "folder") {
        var Delta = {
            type : "folder",
            id : "",
            name : "",
            newPID : "",
            children : [],
            // childAdded : false,
            removed : false
        };
    }
    // Collect data from args
    if(args) for(arg in args) Delta[arg] = args[arg];
    delta.push(Delta);
    handleDeltaList();
}


function handleDeltaList() {   }


let TreeState = [];

function fetchTreeState(parentNode = $("#tree"), treePos = TreeState) {
    // if (parentNode.hasClass("tree")) {  // When at the Root Level
        parentNode.children().each(function () {   // Iterate through children
            if(!($(this).children().hasClass("tree_item--addBtn"))) {

                var id =  $(this).attr('id');
                var name = $(this).find("> span.tree_item > span").text();

                var len = treePos.push({
                    id : id,
                    name : name,
                    children : []
                });
                fetchTreeState($(this).find("> ul.tree_child-list"), treePos[len-1].children);
            }
        });
    // }
}

function updateTreeState() {
    TreeState = [];  // Resetting to avoid duplications
    fetchTreeState();   // Fetch DOM Structure and parse that into the TreeFolderStructure
    
    if (typeof(Storage) !== "undefined")
        localStorage.setItem('TreeState', JSON.stringify(TreeState));
    else
        alert("No Web Storage support found! \nNOTE: Unable to save state of elements, all data edits will be lost on reload.")
}

function getTreeState() {
    return JSON.parse(localStorage.getItem('TreeState'));
}

function treeStateAvailable() {
    return (!(localStorage.getItem('TreeState') === null));
}

function clearTreeState() {
    localStorage.removeItem('TreeState');
}
