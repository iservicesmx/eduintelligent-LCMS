Article = {
	url: null,
	type: null,
	unload_protection_activated: false,
	inline_edit: true,
	activateUnloadProtection:  function() {
		if (this.unload_protection_activated) {
			jQuery('#pa_unload_protection_flag_' + this.type).val(1);
		}
	}
};

Proxy = {
	current: null,
	timeout: null,
	type: null,
	article_url: null
};

Proxy.move = function(widget_id, delta) {
	var widget_node = document.getElementById(widget_id);
	var parent_node = widget_node.parentNode;
	// Move node
	if (delta < 0) {
		var prev = jQuery(widget_node).prev().get(0);
		if (prev)
				parent_node.insertBefore(widget_node, prev);
	} else {
		var next = jQuery(widget_node).next().get(0);
		if (next)
			parent_node.insertBefore(next, widget_node);
	}
	Proxy.refresh(true);
};

Proxy.moveToTop = function(widget_id) {
	var widget_node = document.getElementById(widget_id);
	var parent_node = widget_node.parentNode;
	jQuery(parent_node).prepend(widget_node);
	Proxy.refresh(true);
};

Proxy.moveToBottom = function(widget_id) {
	var widget_node = document.getElementById(widget_id);
	var parent_node = widget_node.parentNode;
	parent_node.appendChild(widget_node);
	Proxy.refresh(true);
};

Proxy.onMouseDown = function(e) {
	var proxy = jQuery(this).parents('.innerContentWidget').get(0);
	Proxy.current = proxy;
	Proxy.lastTarget = null;
	Proxy.timeout = window.setTimeout(function() {
    Proxy.timeout = window.clearTimeout(Proxy.timeout);
    document.body.style.cursor = 'move !important';
    jQuery(proxy).addClass('dragging');
    jQuery(proxy.parentNode).bind('mousemove', Proxy.drag);
	}, 50);
	jQuery(document.body).bind('mouseup', Proxy.drop);
	return true;
};

Proxy.drag = function(e) {
	var e = e || fixEvent(window.event);
	e.stopPropagation();
	var proxy = Proxy.current;
	var target = e.target || e.srcElement;
	var y = e.clientY + document.documentElement.scrollTop;
	target = jQuery(target).parents('.innerContentWidget').get(0);
	if (proxy.offsetTop > target.offsetTop) {
    // dropped above target: insert before
 		proxy.parentNode.insertBefore(proxy, target);
  } else {
    //insert after target or at last position
    var next = target.nextSibling;
    if (next && next.nodeType == 3) next = next.nextSibling;
 		if (next) {
 			try {
      	proxy.parentNode.insertBefore(proxy, next);
      } catch(ex) {}
    } else {
    	proxy.parentNode.appendChild(proxy);
    }
  }
};

Proxy.drop = function(e) {
	var e = e || window.event;
	var proxy = Proxy.current;
	Proxy.current = null;
 	document.body.style.cursor = '';
 	jQuery(proxy).removeClass('dragging');
 	jQuery(proxy.parentNode).unbind('mousemove', Proxy.drag);
 	jQuery(document.body).unbind('mouseup', Proxy.drop);
	if (Proxy.timeout) {
		Proxy.timeout = window.clearTimeout(Proxy.timeout);
		return true;
	}
	var y = e.clientY + document.documentElement.scrollTop;
	var position = 0;
	jQuery('.innerContentWidget', proxy.parentNode).each(function(index) {
		if (proxy == this)
			return position = index;
	});
	Proxy.refresh(true);
};

Proxy.removeRemove = function(widget_id) {
	var widget_node = document.getElementById(widget_id);
	var parent_node = widget_node.parentNode;
	parent_node.removeChild(widget_node);
	Proxy.refresh(true);
};

Proxy.saveForm = function(closeEditWindow) {
   // unblur until onAjaxComplete
   // kss spinner visible until onAjaxComplete
   jQuery('.pField', this.container).unbind('blur');
   jQuery('#kss-spinner').show();
   var fieldset = jQuery(this.container).parents('div')[0];
   var fieldsetData = jQuery('input:not([type=submit]), textarea', fieldset).serialize();
   formData = fieldsetData + '&form.submitted=1&fieldset=' + this.field_name;
   jQuery.ajax({
       type: 'POST',
       url: Article.url + '/processForm',
       data: formData,
       complete: function() { 
           if (closeEditWindow) Proxy.replaceModelView();
           else {
               Proxy.saveonblur();
               jQuery('#kss-spinner').hide();
               }
           } });
   jQuery('#pa_unload_protection_flag_' + Article.type).val(0);
}

Proxy.sendForm = function() {
  var text_input = jQuery('#new_file')[0] || jQuery('#new_url')[0];
	if (text_input) {
    if (!text_input.value.length) {
	    alert(jQuery('#new_file_noinput').text());
	    return false ;
    }
		// Set the interface elements.
		jQuery('#new_file_waitingMessage').show();
		jQuery('#new_file_btn_ok')[0].disabled = true;
		text_input.form.submit();
		// clean only after submit (important)
		jQuery('#new_file_uploadContent').html('');
		jQuery('#new_file_uploadResult').html('');
	}
	return false;
};

Proxy.uploadCompleted = function() {
	var container = Proxy.container;
	var doc = container.ownerDocument;
	var iframe_doc = jQuery('#frmUploadWorker')[0].contentWindow.document;
	jQuery('#new_file_waitingMessage').hide();

	var inner_widgets = jQuery('div.innerContentWidget', iframe_doc);
  var widget_added = false;
	for (var i=0; i < inner_widgets.length; i++) {
	    // because of IE we just can't move the nodes from the IFRAME: it is in
	    // another tree...  thus we need to create a copy
	    var new_widget = inner_widgets[i];

	    var new_div = document.createElement("DIV");
	    new_div.setAttribute('id', new_widget.id);
	    new_div.className = new_widget.className;
	    new_div.innerHTML = new_widget.innerHTML;

	    // this convert HTML to a DOM element. Required in order to find (by
	    // script) later our new elements. Thickbox scripts will look for images
	    // in widget, for instance
	    //jQuery.clean(new_div);

	    jQuery(container).append(new_div);
	    widget_added = true;
	}

	jQuery('#new_file_uploadResult, #new_file_uploadContent', doc).empty();
	jQuery('#new_file_uploadResult', doc).html(jQuery('div#upload-status', iframe_doc).html());
	jQuery('#new_file_uploadContent', doc).html(jQuery('div#upload-informations', iframe_doc).html());

	// Reset the Upload Worker Frame.
	jQuery('#frmUploadWorker').attr('src', 'about:blank');

	// Reset the upload form
	jQuery('#frmUpload', doc)[0].reset();
	jQuery('#new_file_btn_ok', doc)[0].disabled = false;

	if (widget_added) {
    window.Proxy.refresh();
    TB_unlaunch();
    jQuery(document).ready(TB_launch);
  }
};

Proxy.toggleFullDisplay = function(widget_id) {
	var widget = jQuery('#' + widget_id);
	widget.toggleClass('closedContent');
	if (widget.hasClass('closedContent')) {
	jQuery('input[type=text]', widget[0]).each(function() {
		jQuery(this).hide();
    jQuery(this).after('<span>' + this.value + '</span>');
	});
} else {
	jQuery('input[type=text]', widget[0]).each(function() {
		jQuery(this).show();
    jQuery(this).next('span').remove();
	});
}  

};

Browser_init = function() {

  Browser.update = function(path, searchTerm, scope, replaceId, replacePath, bstart, ie_hack) {
    jQuery('.statusBar > div', Browser.window).hide().filter('#msg-loading').show();
    var aUrl = Article.url + '/pa_browser';
    var size = Browser.size();
    var bodyHeight = jQuery('#plone-browser-body')[0].offsetHeight;
  	var data = {
      field_name:  Browser.field_name,
      typeView: 	 Browser.typeView,
      path: 			 path,
      searchTerm:  searchTerm,
      scope:       scope,
      replaceId:   replaceId,
      replacePath: replacePath,
      b_start: bstart,
      onlybody:		 true
    };
    data.path = encodeURI(data.path || '');
    Browser.options = data;
  	jQuery.post(aUrl, data, function(html) {
  		jQuery('#browser-crumbs, #plone-browser-body, #plone-browser-menu').remove();
  		jQuery('#start-refresh').after(html);
  		/*if (Browser.maximized)
  		    Browser.maximize();
  		  else
  		  	Browser.size(size);*/
  		jQuery('#plone-browser-body').height(bodyHeight - 12 + 'px');
  	  jQuery('.statusBar > div', Browser.window).hide().filter('#msg-done').show();
  	  TB_unlaunch();
  		TB_launch();
      Browser.batch();
    });
  }
	
	Browser.maximize = function() {
		Browser.maximized = true;
		var size = {};
		var proxyContainer = Proxy.container;
		size.left = findPosX(proxyContainer) + 130;
		size.top = 100 ;
		arrayPageSize = getPageSize();
		var screenWidth = arrayPageSize [2];
		var screenHeight =arrayPageSize [3];
		size.width = screenWidth - size.left - 30;
		size.height = screenHeight - 110;
		Browser.size(size);
		window.scroll(0,size.top-30);
	};
	
	Browser.selectItem = function (UID) {
	    aUrl = Article.url + '/' + Browser.reference_script;
	    jQuery('.statusBar > div', Browser.window).hide().filter('#msg-loading').show();
        jQuery.post(aUrl, {uid: UID, field_name: Browser.field_name},
               function(data) {
	               var container = jQuery(Proxy.container);
	               container.append(data);
	               TB_unlaunch();
	               jQuery(document).ready(TB_launch);
	               Proxy.refresh();
	         	   jQuery('.statusBar > div', Browser.window).hide().filter('#msg-done').show();
               });
	};
	
    Browser.open = function(path, searchTerm, scope, replaceId, replacePath) {
        var aUrl = Article.url + '/pa_browser';
  	    var data = {
            field_name:  Browser.field_name,
            path : 			 path,
            type: 			 Browser.type,
            typeView: 	 Browser.typeView,
            searchTerm:  searchTerm,
            scope: 			 scope,
            replaceId: 	 replaceId,
            replacePath: replacePath
        };
        data.path = encodeURI(data.path || '');
        jQuery('.statusBar > div', Browser.window).hide().filter('#msg-loading').show();
  	    jQuery.post(aUrl, data, function(html) {
  		    Browser.close();
  		    jQuery(document.body).append(html);
  	        jQuery('#plone-browser').popup();
  		    Browser.window = jQuery('#plone-browser > .window');
  		    jQuery('#plone-browser-tab').mousedown(Browser.setMovable);
  		    jQuery('#plone-browser-corner-resize').mousedown(Browser.setResizable);
  		    if (Browser.maximized)
  		        Browser.maximize();
  		    else
  		  	    Browser.size(Browser.top, Browser.left, Browser.width, Browser.height);
            jQuery('.statusBar > div', Browser.window).hide().filter('#msg-loading').hide();
            jQuery("#plone-browser .overlay").click(Browser.close);
  		    jQuery(document).ready(TB_unlaunch);
  		    jQuery(document).ready(TB_launch);
            jQuery(window).resize(function() {Browser.maximize();});
            Browser.batch();
        });
    };
    
    Browser.maximized = true;
};

Proxy.refresh = function(saveForm) {
	jQuery(".innerContentWidget").removeClass('even').removeClass('odd');
	jQuery(".innerContentWidget:nth-child(even)", Proxy.container).addClass("even");
	jQuery(".innerContentWidget:nth-child(odd)", Proxy.container).addClass("odd");
  jQuery('.file_handle', Proxy.container).mousedown(Proxy.onMouseDown);
  if (jQuery('.innerContentWidget', Proxy.container).length == 1)
    jQuery('.emptyContainer', Proxy.container).show();
  else
    jQuery('.emptyContainer', Proxy.container).hide();
  Article.activateUnloadProtection();
  if (saveForm)
    Proxy.saveForm();
};

Proxy.saveonblur =  function() {
	jQuery('.pField', this.container).blur(function(){
      Proxy.refresh(true);
   });
}

Proxy.enablesaveonclick =  function() {
    closeButton = jQuery('#saveKss', this.node);
    closeButton.attr('href', jQuery('#model-id').val());
    if (Article.inline_edit){
        closeButton.show();
        closeButton.click(function() {
            Proxy.saveForm(true);
            return false;
            });
    }    
}

Proxy.replaceModelView = function() {
    modelview = jQuery('#saveKss', this.node).attr('href');
    pamacro = 'here/'+ modelview + '/macros/main' ;
    formData = {
               pamacro:  encodeURI(pamacro)
               };
    aUrl = Article.url + '/pa_macro_wrapper';    
    jQuery('#kss-spinner').show();
    jQuery.post(aUrl, formData, function(html) {
  		    jQuery('#pacontent').html(html);
  		    jQuery('#kss-spinner').hide();
  		    jQuery(document).ready(pamodel.__init__);
  		    jQuery(document).ready(ProxiesInlineEdit);
  		    jQuery(document).ready(TB_launch);
  		    jQuery(document).ready(activateCollapsibles);
          }
          );               
}


/* Replace edit inline kss methods by a jquery process */

loadEditMacro = function(paedittemplate, fieldName) {
    jQuery('#kss-spinner').show();
    formData = {
               paedittemplate:  paedittemplate,
               fieldName : fieldName
               };
    aUrl =  context.absolute_url() + '/pa_editfield_wrapper';          
    jQuery.post(aUrl, formData, function(html) {
  		    jQuery('#kss-menu').html(html);
  		    jQuery(document).ready(function(){
                     jQuery('#kss-spinner').hide();
                     node = jQuery('.innerContentEditWidget' )[0];
                     Field_init(node);
           } );
          }
          );	        
}


ProxiesInlineEdit = function () {
jQuery('#kss-menu li a').click( function(event) {
            var limenu = jQuery(this).parent();
            paedittemplate = jQuery('.jq-edit-template', limenu).val();
            fieldName = jQuery('.jq-fieldname', limenu).val();
            loadEditMacro(paedittemplate = paedittemplate, fieldName=fieldName);
            return false;
     });
}

jQuery(document).ready(ProxiesInlineEdit);


Proxy_init = function() {
  jQuery('.innerContentWidget.closedContent input[type=text]', Proxy.container).each(function() {
		jQuery(this).hide().after('<span>' + this.value + '</span>');
	});
	Proxy.refresh();
	Article.unload_protection_activated = true;
	Proxy.saveonblur();
};



// Field_init on formTabs click
Tabs_init = function(fieldName) {
	Article.inline_edit = false;
	node = jQuery('#editWidget_' + fieldName )[0];
	jQuery(node).show();
	Field_init(node);
}


Field_init = function(node) {
	nodeType = jQuery(jQuery('.proxy_type', node)[0]).val();
	nodeProxyContainer = jQuery('#proxyContainer_' + nodeType)[0];
	// prevent loading all widgets
  if (jQuery(nodeProxyContainer).height()){
	    Article.type = Proxy.type = nodeType;
	    Article.url = Proxy.article_url = jQuery(jQuery('.article_url', node)[0]).val();
      Proxy.container = nodeProxyContainer;
      Proxy.node = node;
      Proxy.field_name = jQuery(jQuery('.pFieldname', node)[0]).val();
      Browser.type = Browser.typeView = Proxy.type;
    	Browser.url = jQuery(jQuery('.browser_url', node)[0]).val();
      Browser.field_name = jQuery(jQuery('.pFieldname', node)[0]).val();
      Browser.reference_script = jQuery(jQuery('.pa_browser_reference_script', node)[0]).val();
      Browser_init();
      Proxy_init();
      TB_unlaunch();
      TB_launch();
      Proxy.enablesaveonclick();
  }
  /* hide all others proxy when editing inline (this script do not work at this time with multiple innercontainer editform : TODO )*/
  jQuery('.innerContentEditWidget').each(function() {
			if (jQuery(this).attr('id')!= 'editWidget_' + Proxy.field_name) {
         jQuery(this).hide();
      }
		});
  jQuery('#kss-menu .kss-menu-item').each(function() {
			if (jQuery(this).attr('id')!= 'parent-fieldname-' + Proxy.field_name) {
         jQuery(this).hide();
      }
		});		
	// hide iplayer
  // if (Proxy.field_name=='images') jQuery('#imagesPlayer').hide(); 
}





// Load the proxy field when clicking on form Tabs
// TODO : the same thing on formTabs list selection
InitPloneArticleFormTabs = function () {
    jQuery('.pFieldname').each(
        function() {
            var fieldName = jQuery(this).val();
            jQuery('#fieldsetlegend-' + fieldName).click(function() {Tabs_init(fieldName);return false;});            
        }
    );
}


// temp hack of stupid formTabs threshold for plone 3.0x
buildTabs30X = function(container, legends) {
    var threshold = 10;
    var tab_ids = [];
    var panel_ids = [];

    for (var i=0; i<legends.length; i++) {
        tab_ids[i] = legends[i].id;
        panel_ids[i] = tab_ids[i].replace(/^fieldsetlegend-/, "fieldset-")
    }

    if (legends.length > threshold) {
        var tabs = document.createElement("select");
        tabs.onchange = ploneFormTabbing._toggleFactory(container, tab_ids, panel_ids);
    } else {
        var tabs = document.createElement("ul");
    }
    tabs.className = "formTabs";

    for (var i=0; i<legends.length; i++) {
        var legend = legends[i];
        var parent = legend.parentNode;
        if (legends.length > threshold) {
            var tab = document.createElement("option");
        } else {
            var tab = document.createElement("li");
        }
        switch (i) {
            case 0: {
                tab.className = "formTab firstFormTab";
                break;
            }
            case (legends.length-1): {
                tab.className = "formTab lastFormTab";
                break;
            }
            default: {
                tab.className = "formTab";
                break;
            }
        }
        var text = document.createTextNode(getInnerTextFast(legend));
        if (legends.length > threshold) {
            tab.appendChild(text);
            tab.id = legend.id;
            tab.value = legend.id;
        } else {
            var a = document.createElement("a");
            a.id = legend.id;
            a.href = "#" + legend.id;
            a.onclick = ploneFormTabbing._toggleFactory(container, tab_ids, panel_ids);
            var span = document.createElement("span");
            span.appendChild(text);
            a.appendChild(span);
            tab.appendChild(a);
        }
        tabs.appendChild(tab);
        parent.removeChild(legend);
    }
    return tabs;
};

// temp hack of stupid formTabs threshold for plone 3.1
buildTabs31X = function(container, legends) {
    var threshold = 10;
    var tab_ids = [];
    var panel_ids = [];

    legends.each(function(i) {
        tab_ids[i] = '#' + this.id;
        panel_ids[i] = tab_ids[i].replace(/^#fieldsetlegend-/, "#fieldset-");
    });
    var handler = ploneFormTabbing._toggleFactory(
        container, tab_ids.join(','), panel_ids.join(','));

    if (legends.length > threshold) {
        var tabs = document.createElement("select");
        var tabtype = 'option';
        jq(tabs).change(handler).addClass('noUnloadProtection');
    } else {
        var tabs = document.createElement("ul");
        var tabtype = 'li';
    }
    jq(tabs).addClass('formTabs');

    legends.each(function() {
        var tab = document.createElement(tabtype);
        jq(tab).addClass('formTab');

        if (legends.length > threshold) {
            jq(tab).text(jq(this).text());
            tab.id = this.id;
            tab.value = '#' + this.id;
        } else {
            var a = document.createElement("a");
            a.id = this.id;
            a.href = "#" + this.id;
            jq(a).click(handler);
            var span = document.createElement("span");
            jq(span).text(jq(this).text());
            a.appendChild(span);
            tab.appendChild(a);
        }
        tabs.appendChild(tab);
        jq(this).remove();
    });
    
    jq(tabs).children(':first').addClass('firstFormTab');
    jq(tabs).children(':last').addClass('lastFormTab');
    
    return tabs;
};





if (typeof jq != "undefined") {
    // patch plone method ploneFormTabbing._buildTabs
    ploneFormTabbing._buildTabs = buildTabs31X ;
    jQuery(document).ready(InitPloneArticleFormTabs);
}
else {
    // patch plone method ploneFormTabbing._buildTabs
    ploneFormTabbing._buildTabs = buildTabs30X ;
    // this does not work with kupu+MSIE under plone3.0.x
    //jQuery(document).ready(InitPloneArticleFormTabs);
    registerPloneFunction(InitPloneArticleFormTabs);
}    

   
