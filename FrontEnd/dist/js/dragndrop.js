var drake = dragula({
    revertOnSpill: false,
    invalid: function (el, handle) {
        if(el.classList.contains("tree_li") && el.children[0].classList.contains("tree_item--addBtn"))
            return true;
        return el.classList.contains("tree_item--addBtn");
    }
});

// drake.containers.push(container);