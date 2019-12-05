const fs = require('fs');
const CHIPSFILE = "data/chips.json";
const TREEFILE = "data/folderTree.json";


let chips = JSON.parse(fs.readFileSync(CHIPSFILE));
let tree = JSON.parse(fs.readFileSync(TREEFILE));
// console.log(chips);




exports.chips = chips;
exports.tree = tree;


exports.saveChips = function (chips) {
    let data = JSON.stringify(chips, null, 4);
    fs.writeFile(CHIPSFILE, data, function (err) {
        console.log("JSON Saved!");
    });
}

exports.saveTree = function (tree) {
    let data = JSON.stringify(tree, null, 4);
    fs.writeFile(TREEFILE, data, function (err) {
        console.log("JSON Saved!");
    });
}
