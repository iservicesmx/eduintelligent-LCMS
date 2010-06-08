function removeFieldRow(node){

    // XXX replace with getParentElement
    row = node.parentNode.parentNode;
    row.parentNode.removeChild(row);

    return;
}


function handleKeyPress (e) {
    /* Dispatcher for handling the last row */

    // XXX: Generalize window.event for windows
    // Grab current node, replicate, remove listener, append
    var currnode = window.event ? window.event.srcElement : e.currentTarget;
    /* 
       XXX Should add/remove event listeners via JS, but IE has
       non-standard methods.  Not hard, but for now, just check 
       if we are the last row.  If not, bail.
    */

    var tbody = getParentElement(currnode, "TBODY");
    var tr = getParentElement(currnode, "TR");
    var rows = tbody.getElementsByTagName("TR");

    if (rows.length == (tr.rowIndex)) {
        // Add all the last row specific stuff here
        var newtr = tr.cloneNode(true);
        tr.parentNode.appendChild(newtr);
        
        // Turn on hidden "delete" image for current node
        var img = tr.getElementsByTagName("img")[0];
        img.style.display = "inline";
    } else {
        // Handle all other keypress entries, like cursor keys
    }

    return;
}


function getParentElement(currnode, tagname) {
    /* Recursive function to move up the tree to a certain parent */

    tagname = tagname.toUpperCase();
    var parent = currnode.parentNode;

    while (parent.tagName.toUpperCase() != tagname) {
        parent = parent.parentNode;
        // Next line is a safety belt
        if (parent.tagName.toUpperCase == "BODY") return null;
    }

    return parent;
}


function moveRowDown(node){
    row = getParentElement(node, "TR")
    nextRow = row.nextSibling
    var tbody = getParentElement(node, "TBODY");
    var rows = tbody.getElementsByTagName("TR");
    if (nextRow && (rows.length != (nextRow.rowIndex))){
        shiftRow(nextRow, row)
    }
}
function moveRowUp(node){
    row = getParentElement(node, "TR")
    previousRow = row.previousSibling
    if (previousRow){
    shiftRow(row, previousRow)
    }
}

function shiftRow(bottom, top){
    bottom.parentNode.insertBefore(bottom, top )   
}

