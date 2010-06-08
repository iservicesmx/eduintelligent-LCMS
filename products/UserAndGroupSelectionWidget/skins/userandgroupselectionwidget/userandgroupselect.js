function userandgroupselect_openBrowser(portal_url,
                                        fieldId,
                                        groupId) {
    var url = portal_url;
    url += '/userandgroupselect_popup?fieldId=';
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
    defines += 'height=550';
    
    window.open(url,
                'userandgroupselect_popup',
                defines);
}

function userandgroupselect_setEntry(id, value, fieldId, multi) {
    if (multi == 0) {
        var field = document.getElementById(fieldId);
        var field_label = document.getElementById(fieldId + '_label');
        field.value = id;
        field_label.value = value;
    } else {
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
}

function userandgroupselect_removeEntry(fieldId, multi) {
    if (multi == 0) {
        var field = document.getElementById(fieldId);
        var field_label = document.getElementById(fieldId + '_label');
        field.value = '';
        field_label.value = '';
    } else {
        var list = document.getElementById(fieldId);
        for (var x = list.length - 1; x >= 0; x--) {
            if (list[x].selected) {
                list[x] = null;
            }
        }
        // this seem not that senceful
        // for (var x = 0; x < list.length; x++) {
        //     list[x].selected = 'selected';
        // }     
    }
}