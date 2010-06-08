
function searchuser_openBrowser(portal_url,
                                        fieldId,
                                        groupId) {
    var url = portal_url;
    url += '/message_searchuser?fieldId=';
    url += fieldId;
    url += '&selectgroup=';
    url += groupId;

    var defines = 'dependent=yes,';
    defines += 'toolbar=no,';
    defines += 'location=no,';
    defines += 'status=no,';
    defines += 'menubar=no,';
    defines += 'scrollbars=yes,';
    defines += 'resizable=yes,';
    defines += 'width=500,';
    defines += 'height=550,';
    defines += 'left=300'; 
    
    window.open(url,
                'message_searchuser',
                defines);
}

function searchuser_setEntry(id, value, fieldId) {
        var list = document.getElementById(fieldId);
        // check if the item isn't already in the list
        for (var x = 0; x < list.length; x++) {
            if (list[x].value == id) {
                return false;
            }
        }         
        // now add the new item
        var len = list.length;
        list[len] = new Option(value);
        list[len].selected = 'selected';
        list[len].value = id;
}

function searchuser_removeEntry(fieldId, multi) {
        var list = document.getElementById(fieldId);
        for (var x = list.length - 1; x >= 0; x--) {
            if (list[x].selected) {
                list[x] = null;
            }
        // this seem not that senceful
        for (var x = 0; x < list.length; x++) {
            list[x].selected = 'selected';
        }     
    }
}
