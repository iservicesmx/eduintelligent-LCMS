
jQuery.fn.changeClass = function(c1,c2) {
    return this.each(function() {
        this_class=jQuery(this).attr('class');
        if (this_class){
          if (this_class.indexOf(c1)>=0) {
              jQuery(this).removeClass(c1);
              jQuery(this).addClass(c2);
          }
        }                    
    });
};


jQuery.fn.center = function() {
	return this.each(function() {
		var content = this;
	  hh = window.innerHeight || document.documentElement.clientHeight;
	  ww = window.innerWidth || document.documentElement.clientWidth;         
	  hscroll = document.documentElement.scrollTop || document.body.scrollTop;
	  wscroll = document.documentElement.scrollLeft || document.body.scrollLeft;
	  if (content.offsetHeight > hh)
	  	var top = 50;
	  else
	  	var top = (hscroll + (hh / 2) - (content.offsetHeight / 2));
	  jQuery(content).css({
	  	top: 			top  + "px",
	  	left: 		(wscroll + (ww / 2) - (content.offsetWidth / 2)) + "px",
	  	position: 'absolute'
	  });
	  /*jQuery(window).resize(function() {jQuery(this).center();});*/
	});
}

jQuery.fn.fullsize = function() {
  /* give an element the full page dimension */
	return this.each ( function() {
		var content = this;        
		arrayPageSize = getPageSize();
		var w = arrayPageSize[0];
		var h = arrayPageSize[1];
		/* we need to find browser-corner-bottom position
       otherwhise xScroll and yScroll can't be found when 
       browser is moved outside original page's frame */
    corner = document.getElementById('plone-browser-corner-resize');
    maxX = findPosX(corner);
    maxY = findPosY(corner); 
  	if (maxX > w) w = maxX+30 ;
  	if (maxY > h) h = maxY+30 ;    
	  jQuery(content).css({
	  	width: 	w  + "px",
	  	height: h + "px"
	  });
	});
}

jQuery.fn.popup = function() {
	return this.each(function() {
		var popup = this;
		jQuery('> .window', popup).center();
	});
}

String.prototype.capitalize = function(){ //v1.0
    return this.replace(/\w+/g, function(a){
        return a.charAt(0).toUpperCase() + a.substr(1).toLowerCase();
    });
};
function findPosX(obj) {
  var curleft = 0;
  if (obj && obj.offsetParent) {
    while (obj.offsetParent) {
      curleft += obj.offsetLeft;
      obj = obj.offsetParent;
    }
  } else if (obj && obj.x) curleft += obj.x;
  return curleft;
}
function findPosY(obj) {
  var curtop = 0;
  if (obj && obj.offsetParent) {
    while (obj.offsetParent) {
      curtop += obj.offsetTop;
      obj = obj.offsetParent;
    }
  } else if (obj && obj.y) curtop += obj.y;
  return curtop;
}

function getPageScroll(){

	var yScroll;

	if (self.pageYOffset) {
		xScroll = self.pageXOffset;
		yScroll = self.pageYOffset;
	} else if (document.documentElement && document.documentElement.scrollTop){	 // Explorer 6 Strict
		xScroll = document.documentElement.scrollLeft;
    yScroll = document.documentElement.scrollTop;
	} else if (document.body) {// all other Explorers
		xScroll = document.body.scrollLeft;
    yScroll = document.body.scrollTop;
	}

	arrayPageScroll = new Array(xScroll,yScroll) 
	return arrayPageScroll;
}


function getPageSize(){
	
	var xScroll, yScroll;
	
	if (window.innerHeight && window.scrollMaxY) {	
  	yScroll = window.innerHeight + window.scrollMaxY;
  	xScroll = window.innerWidth + window.scrollMaxX;
  	var deff = document.documentElement;
  	var wff = (deff&&deff.clientWidth) || document.body.clientWidth || window.innerWidth || self.innerWidth;
  	var hff = (deff&&deff.clientHeight) || document.body.clientHeight || window.innerHeight || self.innerHeight;
  	xScroll -= (window.innerWidth - wff);
  	yScroll -= (window.innerHeight - hff);
	} else if (document.body.scrollHeight > document.body.offsetHeight || document.body.scrollWidth > document.body.offsetWidth){ // all but Explorer Mac
		xScroll = document.body.scrollWidth;
		yScroll = document.body.scrollHeight;
	} else { // Explorer Mac...would also work in Explorer 6 Strict, Mozilla and Safari
		xScroll = document.body.offsetWidth;
		yScroll = document.body.offsetHeight;
	}
	
	var windowWidth, windowHeight;
	if (self.innerHeight) {	// all except Explorer
		windowWidth = self.innerWidth;
		windowHeight = self.innerHeight;
	} else if (document.documentElement && document.documentElement.clientHeight) { // Explorer 6 Strict Mode
		windowWidth = document.documentElement.clientWidth;
		windowHeight = document.documentElement.clientHeight;
	} else if (document.body) { // other Explorers
		windowWidth = document.body.clientWidth;
		windowHeight = document.body.clientHeight;
	}	
	
	// for small pages with total height less then height of the viewport
	if(yScroll < windowHeight){
		pageHeight = windowHeight;
	} else { 
		pageHeight = yScroll;
	}

	// for small pages with total width less then width of the viewport
	if(xScroll < windowWidth){	
		pageWidth = windowWidth;
	} else {
		pageWidth = xScroll;
	}


	arrayPageSize = new Array(pageWidth,pageHeight,windowWidth,windowHeight) 
	return arrayPageSize;
}


var Browser = {
	maximized: false,
	url: null,
	field_name: null,
	reference_script: null,
	options: null,
	typeView: 'image',
	left: 0,
	top: 0,
	width: 450,
	height: 300,
	fixedHeight: 0
};


Browser.init = function() {}

Browser.fixHeight = function() {
	return Browser.fixedHeight || (Browser.fixedHeight = (
		jQuery('#plone-browser-body')[0].offsetTop
	  + parseInt(jQuery('#plone-browser-body').css('marginBottom'))
	  + parseInt(jQuery('#plone-browser-body').css('marginTop'))
	  + parseInt(jQuery('.statusBar', Browser.window).css('height'))
	  + parseInt(jQuery('#plone-browser-body').css('borderTopWidth'))
	  + parseInt(jQuery('#plone-browser-body').css('borderBottomWidth'))	  
	  + 15
	));
}

Browser.close = function() {
  jQuery('#plone-browser-overlay, #plone-browser').remove();
  Browser.window = null;
  jQuery(window).unbind('resize');
}

Browser.maximize = function() {
	var screenWidth = document.documentElement.clientWidth;
	Browser.width = screenWidth - Browser.left - 10;
	var screenHeight = document.documentElement.clientHeight;
	Browser.height = screenHeight - Browser.top - 100;
	Browser.size({width: Browser.width, height: Browser.height});
	Browser.window.center();
};

Browser.size = function(top, left, width, height) {
	if (!arguments[0]) {
		var wnd = Browser.window.get(0);
		Browser.left = wnd.offsetLeft;
		Browser.top = wnd.offsetTop;
		Browser.width = wnd.offsetWidth;
		Browser.height = wnd.offsetHeight;
		return { left: Browser.left, top: Browser.top, 
						 width: Browser.width, height: Browser.height };	
	} else if (typeof arguments[0] == 'string')
		return Browser.window.get(0)['offset' + arguments[0].capitalize()];
	if (arguments.length == 4) {
		Browser.left = left; Browser.top = top;
		Browser.width = width; Browser.height = height;
	} else if (arguments.length == 1) {
		var size = arguments[0];
		for (attr in Browser.size())
			Browser[attr] = size[attr] != undefined ? size[attr] : Browser[attr];
	}
	/* Settle a minimal size */
	Browser.width = 	Browser.width < 380 ? 380 : Browser.width;
	Browser.height = 	Browser.height < 220 ? 220 : Browser.height; 
	
	Browser.window
	    .css({ top:Browser.top + 'px', left:Browser.left + 'px' })
		.width(Browser.width + 'px')
		.height(Browser.height + 'px');
	
	/* Compute browser-body-height, as it's the one which impact height */
	if (height || arguments[0]['height']) {
		var bodyHeight = Browser.height;
		bodyHeight -= Browser.fixHeight();
		bodyHeight -= 8;
		jQuery('#plone-browser-body').height(bodyHeight + 'px');
	}	
  jQuery('#plone-browser .overlay').fullsize();
};

Browser.setView = function(typeView) {
	Browser.typeView = typeView;
	if (typeView == 'file')
		jQuery('#plone-browser-body .floatContainer')
			.changeClass('floatContainer','listContainer')
			.changeClass('portrait','portrait_icon')
			.changeClass('landscape','landscape_icon');		
	else
		jQuery('#plone-browser-body .listContainer')
			.changeClass('listContainer','floatContainer')
			.changeClass('portrait_icon','portrait')
			.changeClass('landscape_icon','landscape');			
	jQuery('#menuViews a').removeClass('selected');
	jQuery('#menuViews a.' + typeView + 'View').addClass('selected');
};

Browser.open = function(path, searchTerm, scope, replaceId, replacePath) {
  var aUrl = 'pa_browser';
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
  Browser.options = data;
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
    TB_unlaunch();
		TB_launch();		
	  jQuery(window).resize(function() {Browser.maximize();});	  
	  Browser.batch();
  });
};

Browser.update = function(path, searchTerm, scope, replaceId, replacePath, bstart, ie_hack) {
  jQuery('.statusBar > div', Browser.window).hide().filter('#msg-loading').show();
  var aUrl = 'pa_browser';
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

Browser.setResizable = function(e) {
		Browser.maximized = false;
		Browser.size();
		Browser.start_width = Browser.width;
		Browser.start_height = Browser.height;
		Browser.start_width -= e.clientX + document.documentElement.scrollLeft;
		Browser.start_height -= e.clientY + document.documentElement.scrollTop;
		document.body.style.cursor = 'se-resize';
		jQuery(document.body).mousemove(Browser.resize).mouseup(Browser.drop);
		return false;
};

Browser.resize = function(e) {
	var x = e.clientX + document.documentElement.scrollLeft;
	var y = e.clientY + document.documentElement.scrollTop;
	var browserWidth = (Browser.start_width + x);
	var browserHeight = (Browser.start_height + y);	
	browserHeight -= 10;
	Browser.size({ width: browserWidth, height:  browserHeight});
	return false;	
};

Browser.setMovable = function(e) {
		var e = e || window.event;
		Browser.maximized = false;
		Browser.start_x = Browser.size().left;
		Browser.start_y = Browser.size().top;
		Browser.start_x -= e.clientX + document.documentElement.scrollLeft;
		Browser.start_y -= e.clientY + document.documentElement.scrollTop;		
		jQuery(document.body).mousemove(Browser.move).mouseup(Browser.drop);
		return false;
};

Browser.move = function(e) {
	var e = e || window.event;
	var x = e.clientX + document.documentElement.scrollLeft;
	var y = e.clientY + document.documentElement.scrollTop;
	Browser.size({left: (Browser.start_x + x), top: (Browser.start_y + y)});
	return false;
}


Browser.drop = function(e) {
	document.body.style.cursor = '';	
	jQuery(document.body)
	    .unbind('mousemove', Browser.resize)
	    .unbind('mousemove', Browser.move)
	    .unbind('mouseup', Browser.drop);
		
		//.unmousemove(Browser.resize)
		//.unmousemove(Browser.move)
		//.unmouseup(Browser.drop);
};

Browser.search = function(url, path, type, typeView, replaceId, replacePath) {
  var searchTerm = jQuery('#searchTerm').val();
  var scope = jQuery('#scope').val();
  Browser.open(path, searchTerm, scope, replaceId, replacePath);	
};

Browser.selectItem = function (UID) {
	alert("Selected: " + UID);
};


Browser.batch = function() {
  jQuery('#plone-browser-body .listingBar a').click (
    function(){
      var batchUrl = this.href;
      var queryString = batchUrl.replace(/^[^\?]+\??/,'');
      var params = parseQuery( queryString );
      Browser.update (params['path'], params['searchTerm'], params['scope'],params['replaceId'],params['replacePath'], params['b_start:int']);
      this.blur();
      return false;
    }
  );
}

function parseQuery ( query ) {
   var Params = new Object ();
   if ( ! query ) return Params; // return empty object
   var Pairs = query.split(/[;&]/);
   for ( var i = 0; i < Pairs.length; i++ ) {
      var KeyVal = Pairs[i].split('=');
      if ( ! KeyVal || KeyVal.length != 2 ) continue;
      var key = unescape( KeyVal[0] );
      var val = unescape( KeyVal[1] );
      val = val.replace(/\+/g, ' ');
      Params[key] = val;
   }
   return Params;
}

