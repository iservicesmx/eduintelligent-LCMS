/* Thickbox Plus - One resizing box to rule them all.
 * Based on original Thickbox script by Cody Lindley (http://www.codylindley.com)
 * Modified by Christian Montoya (http://www.christianmontoya.com)
 * For information, visit http://lab.christianmontoya.com/thickbox-plus/
 * Under an Attribution, Share Alike License
 * Thickbox is built on top of the very light weight jquery library.
 * Modifications must keep attribution for both Christian Montoya and Cody Lindley.
 */

//jQuery(document).ready(TB_launch); 

// function for adding Thickbox to elements of class .thickbox
// wrapped by Christian Montoya for uses other than jQuery(document).ready
function TB_launch() {
jQuery("a.thickbox").click(function(){
  var t = this.title || this.innerHTML || this.href;
  TB_show(t,this.href);
  this.blur();
  return false;
});
}

//addon Ingeniweb for Plone
jQuery(document).ready(TB_launch);

//addon Ingeniweb for desactive-reactive thickbox onclick from ajax container or another thickbox container
function TB_unlaunch() {
jQuery("a.thickbox").unbind('click');
}

function TB_show(caption, url) { //function called when the user clicks on a thickbox link
	try {
	  // MSIE fix
	  hideSelectBoxes();
		var queryString = url.replace(/^[^\?]+\??/,'');
		var params = parseQuery( queryString );	
		var urlString = /.jpg|.jpeg|.png|.gif|.html|.htm/g;
		var urlType = url.match(urlString);
		var urlIsImage = (urlType == '.jpg' || urlType == '.jpeg' || urlType == '.png' || urlType == '.gif' || params['isImage']);	  
		jQuery("body").append("<div id='TB_overlay'></div>");
		if (params['field_name']) jQuery("body").append("<div id='TB_window' class='proxyAction'></div>");
    else jQuery("body").append("<div id='TB_window'></div>");   
		//addon ingeniweb
		TB_overlay_position();
		jQuery("#TB_overlay").css("opacity","0.5");
		jQuery("#TB_overlay").css("filter","alpha(opacity=50)");
		jQuery("#TB_overlay").css("-moz-opacity","0.5");
		jQuery("#TB_overlay").click(TB_remove);
		jQuery(window).resize(TB_position);
		jQuery("body").append("<div id='TB_load'><div id='TB_loadContent'><img src='circle_animation.gif' /></div></div>");
		jQuery("#TB_overlay").show();		
 
		if (urlIsImage) {//code to show images
			var imgPreloader = new Image();
			imgPreloader.onload = function(){

			// Resizing large images added by Christian Montoya
			var de = document.documentElement;
			var x = (self.innerWidth || (de&&de.clientWidth) || document.body.clientWidth) - 50;
			var y = (self.innerHeight || (de&&de.clientHeight) || document.body.clientHeight) - 80;
			if(imgPreloader.width > x) { 
				imgPreloader.height = imgPreloader.height * (x/imgPreloader.width); 
				imgPreloader.width = x; 
				if(imgPreloader.height > y) { 
					imgPreloader.width = imgPreloader.width * (y/imgPreloader.height); 
					imgPreloader.height = y; 
				}
			} 
			else if(imgPreloader.height > y) { 
				imgPreloader.width = imgPreloader.width * (y/imgPreloader.height); 
				imgPreloader.height = y; 
				if(imgPreloader.width > x) { 
					imgPreloader.height = imgPreloader.height * (x/imgPreloader.width); 
					imgPreloader.width = x;
				}
			}
			// End Resizing
			
			TB_WIDTH = imgPreloader.width;
			TB_HEIGHT = imgPreloader.height + 20;					

			jQuery("#TB_window").append("<a href='#' id='TB_closeWindow'><span id='TB_closeWindowButton'>X</span></a>"
                 + "<img id='TB_Image' src='"+url+"' width='"+imgPreloader.width+"' height='"+imgPreloader.height+"' alt='"+caption+"'/>"
			           + "<div id='TB_caption'>"+caption+"</div>"); 
			jQuery("#TB_closeWindow").click(TB_remove);
			jQuery("#TB_Image").click(TB_remove);
			jQuery("#TB_Image").bind('mouseover', function(){
          jQuery('#TB_caption').slideDown('fast');
          });
			jQuery("#TB_Image").bind('mouseout', function(){
          jQuery('#TB_caption').slideUp('slow');
          });          
			TB_position();
			jQuery("#TB_load").remove();
			jQuery("#TB_window").slideDown("normal");
			}
	  
			imgPreloader.src = url;
		}
		
		if(urlType == '.htm' || urlType == '.html' || !urlIsImage){//code to show html pages
			
			TB_WIDTH = (params['width']*1) + 30;
			TB_HEIGHT = (params['height']*1) + 40;
			ajaxContentW = TB_WIDTH - 30;
			ajaxContentH = TB_HEIGHT - 45;
			jQuery("#TB_window").append("<div id='TB_closeAjaxWindow'><a href='#' id='TB_closeWindowButton'>close</a></div><div id='TB_ajaxContent' style='width:"+ajaxContentW+"px;height:"+ajaxContentH+"px;'></div>");
			jQuery("#TB_closeWindowButton").click(TB_remove);
			jQuery("#TB_ajaxContent").load(url, function(){TB_position();
                                          			jQuery("#TB_load").remove();
                                          			jQuery("#TB_window").slideDown("normal");
                                                /* addons Ingeniweb
                                                   we can add closeWindow buttons everywhere in ajax content*/
                                          			jQuery(".TB_closeWindow").click(TB_remove);  
                                                highlightSearchTermsInPreview();                                   			
                                          			});
		}
		
	} catch(e) {
		alert( e );
	}
}

//helper functions below

function TB_remove() {
  // addon Ingeniweb 
  showSelectBoxes();
	// #TB_load removal added by Christian Montoya; solves bug when overlay is closed before image loads
	jQuery("#TB_window").fadeOut("fast",function(){jQuery('#TB_window,#TB_overlay,#TB_load').remove();}); 
	return false;
}


function TB_overlay_position() {  
  arrayPageSize = getPageSize();
  jQuery("#TB_overlay").css("height",arrayPageSize[1] +"px");
}

function TB_position() {
	var arrayPageSize = getPageSize();
	var arrayPageScroll = getPageScroll();
	var w = arrayPageSize[2];
	var h = arrayPageSize[3];
	var yScroll = arrayPageScroll[1];
  var boxTop = yScroll + (h - TB_HEIGHT)/2;
	jQuery("#TB_window").css({width:TB_WIDTH+"px",height:TB_HEIGHT+"px", left: ((w - TB_WIDTH)/2)+"px", top: boxTop +"px" });
	//jQuery("#TB_window").css({left: ((w - TB_WIDTH)/2)+"px", top: boxTop +"px" });
	TB_overlay_position();
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

// Addon : fix problem with select boxes - Ingeniweb

function showSelectBoxes(){
	selects = document.getElementsByTagName("select");
	for (i = 0; i != selects.length; i++) {
		selects[i].style.visibility = "visible";
	}
}

function hideSelectBoxes(){
	selects = document.getElementsByTagName("select");
	for (i = 0; i != selects.length; i++) {
		selects[i].style.visibility = "hidden";
	}
}

// Adon preview PloneArticle
function highlightSearchTermsInPreview() {        
        // search-term-highlighter function --  Geir Bækholt
        var terms = getSearchTermsFromURI(window.location.search);
        var contentarea = document.getElementById('preview-container');
        if (contentarea) {
            highlightSearchTerms(terms, contentarea);
            }
        }
      

//
