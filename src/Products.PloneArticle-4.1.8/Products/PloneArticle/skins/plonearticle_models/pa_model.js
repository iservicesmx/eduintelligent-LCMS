/* ================ */
/* models js stuff  */
/* ================ */



var context = {
    absolute_url: function() {
        return jQuery('input#absolute_url').val();
    },
    portal_url: function() {
        return jQuery('input#portal_url').val();
    }
}


var pamodel = {
    __init__: function(e) {

        /* init images & videos players */
        pamodel.paplayer.__init__();

    }

}

/* ======================= */
/* Images / videos players */
/* ======================= */

pamodel.paplayer = {
    /* vars */
    active: 0,
    current_image: 0,
    orientation: 'horizontal',
    vbuttons: 'right',
    hbuttons: 'bottom',
    images: new Array(),
    thumb_width: 0,
    thumb_height: 0,
    max_width: 0,
    max_height: 0,
    player_color: '',

    /* methodes */
    __init__: function() {
        pamodel.paplayer.images[0] = {'imgtitle': '',
                                      'imgdesc': '',
                                      'imgurl': ''};
        if (jQuery('#imagesPlayer').length) pamodel.paplayer.active=1;
        if (pamodel.paplayer.active) {
            // setPlayerStyles is important (set images sizes, orientation, etc ... do not remove)
            pamodel.paplayer.setPlayerStyle();
            jQuery('a.paplayerImages').each(function(i,link) {
                jQuery(link).click( function() { pamodel.paplayer.showCurrentImage(link); return false; } );
                jQuery(link).mouseover( function() { pamodel.paplayer.showThumbLegend(link); return false; } );
                jQuery(link).mouseout( function() { jQuery('#thumbLegend').empty(); return false; } );
                pamodel.paplayer.images[i] = {'imgtitle': jQuery('.imgtitlevalue',this).val(),
                                              'imgdesc':  jQuery('.imgdescvalue',this).val(),
                                              'imgurl': jQuery('.imgurlvalue',this).val()
                                              };
            });
            pamodel.paplayer.connect('previousImage',pamodel.paplayer.previousImage);
            pamodel.paplayer.connect('nextImage',pamodel.paplayer.nextImage);
            pamodel.paplayer.connect('firstImage',pamodel.paplayer.firstImage);
            pamodel.paplayer.connect('lastImage',pamodel.paplayer.lastImage);
            // zoom (thickbox)
            jQuery('a#paplayerImageZoom').click(pamodel.paplayer.zoomImage);
            jQuery('img#previewImg').click(pamodel.paplayer.zoomImage);
            pamodel.paplayer.current_image = 0;
            pamodel.paplayer.showImage();
        }
    },
    connect: function(id, func) {
        var button = jQuery('a#'+id);
        if (!button.length) return;
        button.click(func);
    },
    showThumbLegend: function(link) {
        var legend = link.title;
        jQuery('#thumbLegend').empty();
        jQuery('#thumbLegend').append(legend);
    },
    showCurrentImage: function(link) {
        var href = link.href;
        var legend = link.title;
        jQuery('img#previewImg').attr('src', href);
        jQuery('img#previewImg').attr('alt', legend + ' (zoom)');
        jQuery('a.paplayerImages').each(function(i,link) {
            if (href.match(link.href)) {
                jQuery(link).addClass('selected');
                pamodel.paplayer.current_image = i;
                var nMax = 3;
                if ( pamodel.paplayer.orientation=='vertical') {
                    nMax = parseInt(jQuery('#thumbs').height()/(pamodel.paplayer.thumb_height+5));
                }
                else {
                    nMax = parseInt(jQuery('#thumbs').width()/(pamodel.paplayer.thumb_width+5));
                }
                if (pamodel.paplayer.images.length > nMax) {
                    jQuery('div#thumbsInnerWrapper').css('position', 'relative');
                    // posIndex in center
                    var posIndex=1;
                    if (nMax > 2) {
                       if ( nMax/2> parseInt(nMax/2)) {
                           posIndex = parseInt(nMax/2)+1;
                       }
                       else posIndex = nMax/2;
                    }
                    pamodel.paplayer.moveThumbs(i, posIndex, pamodel.paplayer.orientation);
                }
            } else {
                jQuery(link).removeClass('selected');
            }
        });
        zoomUrl = pamodel.paplayer.images[pamodel.paplayer.current_image]['imgurl']+'?isImage=1';
        Title = pamodel.paplayer.images[pamodel.paplayer.current_image]['imgtitle'];
        Description = pamodel.paplayer.images[pamodel.paplayer.current_image]['imgdesc'];
        jQuery('a#paplayerImageZoom').each(function(i,link) {
            link.href = zoomUrl;
            link.title = Title + " (zoom)";
        });
        jQuery('#imgTitle').empty();
        jQuery('#imgDescription').empty();
        jQuery('#imgTitle').append(Title);
        jQuery('#imgDescription').append(Description);
        jQuery(document).ready(pamodel.paplayer.displayButtons);
    },
    showImage: function() {
        var image = pamodel.paplayer.images[pamodel.paplayer.current_image]['imgurl'];
        jQuery('a.paplayerImages').each(function(i,link) {
            if (link.href.match(image)) {
                jQuery(link).addClass('selected');
                pamodel.paplayer.showCurrentImage(link);
                return false;
            }
            else {
                jQuery(link).removeClass('selected');
            }
        });        
    },

    displayButtons: function() {
        if(pamodel.paplayer.current_image > 0) {
            jQuery('a#previousImage').css('visibility', 'visible');
            jQuery('a#firstImage').css('visibility', 'visible');
        }
        else {
            jQuery('a#previousImage').css('visibility', 'hidden');
            jQuery('a#firstImage').css('visibility', 'hidden');
        }
        if (pamodel.paplayer.current_image < (pamodel.paplayer.images.length-1)) {
            jQuery('a#nextImage').css('visibility', 'visible');
            jQuery('a#lastImage').css('visibility', 'visible');
        }
        else {
            jQuery('a#nextImage').css('visibility', 'hidden');
            jQuery('a#lastImage').css('visibility', 'hidden');
        }
    },

    previousImage: function(e) {
        if (pamodel.paplayer.current_image > 0) {
            pamodel.paplayer.current_image += -1;
        };
        setTimeout(pamodel.paplayer.showImage, 0); // hack ie6
    },
    nextImage: function(e) {
        if (pamodel.paplayer.current_image < (pamodel.paplayer.images.length-1)) {
            pamodel.paplayer.current_image += 1;
        };
        setTimeout(pamodel.paplayer.showImage, 0); // hack ie6
    },
    firstImage: function(e) {
        pamodel.paplayer.current_image = 0;
        pamodel.paplayer.showImage();
    },
    lastImage: function(e) {
        pamodel.paplayer.current_image = pamodel.paplayer.images.length-1;
        pamodel.paplayer.showImage();
    },
    zoomImage: function(event) {
        if (event) {
            event.preventDefault();
            event.stopPropagation();
        }
        var href = pamodel.paplayer.images[pamodel.paplayer.current_image]['imgurl']+'?isImage=1';
        var title = pamodel.paplayer.images[pamodel.paplayer.current_image]['imgtitle'];
        TB_show(title, href);
    },
    setPlayerStyle: function() {
        // global values
        pamodel.paplayer.thumb_width = parseInt(jQuery('#thumbmaxwidthvalue').val());
        pamodel.paplayer.thumb_height = parseInt(jQuery('#thumbmaxheightvalue').val());
        pamodel.paplayer.max_width = parseInt(jQuery('#maxwidthvalue').val());
        pamodel.paplayer.max_height = parseInt(jQuery('#maxheightvalue').val());
        // gruik : to make all childs inherit border-color from imagesPlayer border-color
        pamodel.paplayer.player_color = jQuery('#imagesPlayer').css('border-left-color');
        // player orientation
        pamodel.paplayer.orientation = 'horizontal';
        if (jQuery('.verticalPlayer').length) {
            pamodel.paplayer.orientation = 'vertical';
        }
        pamodel.paplayer.vbuttons = 'right';
        if (jQuery('.leftVButtons').length) {
            pamodel.paplayer.vbuttons = 'left';
        }
        pamodel.paplayer.hbuttons = 'bottom';
        if (jQuery('.topHButtons').length) {
            pamodel.paplayer.hbuttons = 'top';
        }
        //set styles
        // TODO : don't set colors when DISBALESTYLES=True in config
        jQuery('#legendWrapper').css('border-color',pamodel.paplayer.player_color);
        jQuery('#thumbsWrapper').css('border-color',pamodel.paplayer.player_color);
        jQuery('.playerButtons').css('border-color',pamodel.paplayer.player_color);
        jQuery('#thumbLegend').css('border-color',pamodel.paplayer.player_color);
        jQuery('#thumbLegend').css('color',pamodel.paplayer.player_color);
        jQuery('#imgDescription').css('color',pamodel.paplayer.player_color);

        // vertical playerOrientation
        if (pamodel.paplayer.orientation == 'vertical') {
            var controls = jQuery("#thumbsWrapper").clone();
            jQuery("#thumbsWrapper").remove();
            controls.prependTo("#imagesPlayer");
            jQuery("#thumbsWrapper").css('float', pamodel.paplayer.vbuttons);
            jQuery("#thumbsWrapper").css('border-top', 'none');
            jQuery("#thumbsWrapper").css('height', 'auto');
            if (pamodel.paplayer.vbuttons=='right') {
                jQuery("#thumbsWrapper").css('border-left-width', '1px');
                jQuery("#thumbsWrapper").css('border-left-style', 'solid');
            }
            else {
                jQuery("#thumbsWrapper").css('border-right-width', '1px');
                jQuery("#thumbsWrapper").css('border-right-style', 'solid');
            }
            jQuery('.playerButtons').css('float', 'none');
            jQuery('#thumbs').css('float', 'none');
            jQuery('.paplayerImages').css('float', 'none');
            jQuery('#playerControls').css('margin', 'auto 0');
            jQuery('.playerButtons').css('margin-top', '0');
            jQuery('#thumbs').css('margin-left', '0');
            jQuery('.paplayerImages').css('margin-left', '0');
            jQuery('.playerButtons').css('margin-bottom', '3px');
            jQuery('#thumbs').css('margin-bottom', '3px');
            jQuery('.paplayerImages').css('margin-bottom', '3px');
            jQuery('#thumbs').height(jQuery('#previewWrapper')[0].offsetHeight+jQuery('#thumbLegend')[0].offsetHeight+jQuery('#legendWrapper')[0].offsetHeight-82 + 'px');
            jQuery('#thumbs').width(pamodel.paplayer.thumb_width + 'px');
            jQuery('.playerButtons').css('margin-left', parseInt((pamodel.paplayer.thumb_width-38)/2) + 'px');
            // height must be as long as possible to contain all thumbs
            jQuery('#thumbsInnerWrapper').height(''+(pamodel.paplayer.thumb_height+5)*jQuery('a.paplayerImages').length +  'px');
            jQuery('#thumbsInnerWrapper').css('width', ''+(pamodel.paplayer.thumb_width)+'px');
            // set global width & height
            jQuery('#imagesPlayer').width(jQuery('#thumbsWrapper')[0].offsetWidth+jQuery('#imagesPlayer')[0].offsetWidth+1 +'px');
            // stop margin
        }

        // horizontal player
        else {
            // move controls at top when hbuttons = 'top'
            if (pamodel.paplayer.hbuttons == 'top') {
                var controls = jQuery("#thumbsWrapper").clone();
                jQuery("#thumbsWrapper").remove();
                controls.prependTo("#imagesPlayer");
                jQuery("#thumbsWrapper").css('border-top', 'none');
                jQuery("#thumbsWrapper").css('border-bottom-width', '1px');
                jQuery("#thumbsWrapper").css('border-bottom-style', 'solid');
            }
            jQuery('#thumbs').width(pamodel.paplayer.max_width-85 + 'px');
            jQuery('#thumbs').height(pamodel.paplayer.thumb_height+2 + 'px');
            jQuery('.playerButtons').css('margin-top', parseInt((pamodel.paplayer.thumb_height-38)/2) + 'px');
            // width must be as long as possible to contain all thumbs
            jQuery('#thumbsInnerWrapper').width(''+(pamodel.paplayer.thumb_width+5)*jQuery('a.paplayerImages').length + 'px');
        }

    },
    moveThumbs: function(i, posIndex, orientation) {
        var new_pos = 0;
        if (i < pamodel.paplayer.images.length) {
           // 5 = margins + borders width
           if (orientation == 'vertical') {
               new_pos = (pamodel.paplayer.thumb_width + 5)*(i-posIndex+1) ;
           }
           else new_pos = (pamodel.paplayer.thumb_height + 5)*(i-posIndex+1) ;
        }
        if (new_pos < 0) {
             new_pos = 0;
        }
        if (orientation == 'vertical') {
            jQuery('div#thumbsInnerWrapper').animate({top:-new_pos});
        }
        else {
            jQuery('div#thumbsInnerWrapper').animate({left:-new_pos});
        }
    }
}




jQuery(document).ready(pamodel.__init__);



