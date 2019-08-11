//                           Logic Behind StateSaving
//  foo() captures user's intended changes and calls addDelta() method
// 
//      foo()  -->  addDelta()  ------ deltaObj -----> delta[] ---->  handleDeltaList()
//        |                                                                   |
//        |                                                                   |
//        V                                                                   V
//   DOM_updated_Realtime (Light)                                    JSON_updated (Heavy)

let delta = []


function addDelta(type, args) {
    if(type == "folder") {
        var folderDelta = {
            id : "",
            name : "",
            newParent : "",
            childrenOpType : "",
            children : []
        };

        //set the options
        if(args) for(arg in args) folderDelta[arg] = args[arg];

        // Update DOM
        if(folderDelta.id !== "" && folderDelta.name !== "") {
            $("#"+folderDelta.id + " .tree_item span").text(folderDelta.name);
        }

        delta.push(folderDelta)
    }
}