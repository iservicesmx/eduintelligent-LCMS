# -*- coding: utf-8 -*-
## Copyright (C)2007 Ingeniweb

## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; see the file COPYING. If not, write to the
## Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

"""
Our view classes
$Id$
"""

from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from plone.memoize.instance import memoize

# Root view class for PloneArticle (Five.BrowseView subclass)
from Products.PloneArticle.browser.article import PloneArticleModelView

# Unregistered viws are useless ;)
from Products.PloneArticle.model import registerArticleModel

# Importing our model interfaces
from interface import IPAEduIntelligent

from eduintelligent.paeduintelligent.swfHeaderData import analyseContent
from StringIO import StringIO
from cgi import escape


import re        
link    = re.compile(r'link\((.+?)\)')
image   = re.compile(r'img\((.+?)\)')
video   = re.compile(r'video\((.+?)\)')
flash   = re.compile(r'flash\((.+?)\)')
audio   = re.compile(r'audio\((.+?)\)')

class PAEduIntelligent(PloneArticleModelView):
    """
    Allow insert tags for rich content
    """

    implements(IPAEduIntelligent)

    template_id = 'pa_model0'
    title = u'General Model'
    title_msgid = 'model0_title'
    icon = 'pa_model9.gif'
    description_msgid = 'model0_description'

    def getPages(self):
        """
        """
        return self.context.getText().split("<hr class=\"docutils\" />")

    ##############################################
    def _getFileType(self, ext, index):
        files = self.context.getFiles()
        if not files:
            return []

        filtered = [x for x in files if x.getExt() == ext]
        try: # Por si el index no se encuentra en la lista
            return filtered[index]
        except:
            return []

    def _replaceImage(self, match):
        name = match.group(1)
        align = ""
        tmp = name.split(",")
        name = tmp[0]
        if len(tmp) > 1:
            align = tmp[1]
        images = self.context.getImages()

        if not images:
            return "<b style=\"color:red;\"> La secci&oacute;n de im&aacute;genes esta vacia, (no esta la imagen %s)</b>"%(name)

        try:
            index = int(name)
        except:
            return "<b style=\"color:red;\"> El valor dentro de los parentesis debe ser el numero de la imagen</b>"

        if index > len(images):
            return "<b style=\"color:red;\">No se ha agregado la imagen %s</b>"%(index)

        image = images[index-1]
        absolute_url = image.absolute_url()
        title = image.Title()
        description = image.Description()

        params={}
        params['width']=400
        params['height']=400
        if description:
            params['title']=description
        source = image.tag(**params)

        text = "<div class=\"centerBlock photosPreview\">"
        if align.upper() == 'I':
            text = "<div class=\"leftBlock photosPreview\">"
        elif align.upper() == 'D':
            text = "<div class=\"rightBlock photosPreview\">"

        text +="<div class=\"image block\">"
        if description:
            text += "<div class=\"thickbox photoTitle\">"+title+" </div>"
        text += "<a class=\"thickbox\" target=\"_blank\" href=\""+absolute_url+"?isImage=1\" title=\""+title+"\">"
        text += source
        text += "</a></div>"
        if not description:
            text += "<div class=\"thickbox photoTitle\"> "+title+" </div>"
        if description:
            text += "<div class=\"thickbox photoTitle\"> "+description+" </div>"
        text += "</div></div>"
        return text

    def _replaceVideo(self, match):
        name = match.group(1)

        try:
            index = int(name)
        except:
            return "<b style=\"color:red;\"> El valor dentro de los parentesis debe ser el numero del video</b>"

        video = self._getFileType('flv',index-1)

        if not video:
            return "<b style=\"color:red;\"> No se han agregado videos o no esta el video %s</b>"%(name)

        title = video.Title()
        description = video.Description()
        source = self.getFilePreview(video, ext='flv')

        text = "<div align=\"center\">"
        if description:
            text += "<div class=\"photoTitle\"> "+title+" </div>"
        text += source
        if not description:
            text += "<div class=\"photoTitle\"> "+title+" </div>"
        if description:
            text += "<div class=\"photoTitle\"> "+description+" </div>"
        text += "</div>"
        return text

    def _replaceFlash(self, match):
        name = match.group(1)
        align = ""
        tmp = name.split(",")
        name = tmp[0]
        if len(tmp) > 1:
            align = tmp[1]

        try:
            index = int(name)
        except:
            return "<b style=\"color:red;\"> El valor dentro de los parentesis debe ser el numero del flash</b>"

        flash = self._getFileType('swf',index-1)

        if not flash:
            return "<b style=\"color:red;\"> No se han agregado animaciones en flash o no esta la numero %s</b>"%(name)

        title = flash.Title()
        description = flash.Description()
        source = self.getFilePreview(flash, ext='swf')

        text = "<div align=\"center\">"
        if align.upper() == 'I':
            text = "<div style=\"float: left\">"
        elif align.upper() == 'D':
            text = "<div style=\"float: right\">"

        if description:
            text += "<div class=\"photoTitle\"> "+title+" </div>"

        text += source

        if not description:
            text += "<div class=\"photoTitle\"> "+title+" </div>"
        if description:
            text += "<div class=\"photoTitle\"> "+description+" </div>"
        text += "</div>"
        return text

    def _replaceAudio(self, match):
        name = match.group(1)
        try:
            index = int(name)
        except:
            return "<b style=\"color:red;\"> El valor dentro de los parentesis debe ser el numero del audio</b>"

        audio = self._getFileType('mp3',index-1)

        if not audio:
            return "<b style=\"color:red;\"> No se han agregado audio o no esta la numero %s</b>"%(name)

        absolute_url = audio.absolute_url()
        title = audio.Title()
        description = audio.Description()
        source = self.getFilePreview(audio, ext='mp3')
        #print source

        text = "<div class=\"imagesContentBox\" align=\"center\">"
        if description:
            text += "<div class=\"discreet\"> "+title+" </div>"
        text += source
        if not description:
            text += "<div class=\"discreet\"> "+title+" </div>"
        if description:
            text += "<div class=\"discreet\"> "+description+" </div>"
        text += "</div>"
        return text

    def _replaceLink(self, match):
        name = match.group(1)
        tmp = name.split(",")
        text = ""
        if len(tmp) > 1:
            name = tmp[0]
            link = tmp[1]        
            text += "<a href=\"#\" alt=\""+link+"\" title=\""+name+"\" onClick=\"window.open('"+link+"', 'NuevaVentana', 'width=700,height=500,toolbar=yes,menubar=yes,scrollbars=yes,resizable=yes'); return false;\" >"
            text += name
            text += "</a>"
            return text

        else:
            return "<b style=\"color:red;\"> El link de %s es incorrecto o no lo puso</b>"%(name)


    @memoize
    def transform(self, text):
        if self.context.getImages():        
            text = image.sub(self._replaceImage, text)
        if self.context.getFiles():
            text = video.sub(self._replaceVideo, text)
            text = flash.sub(self._replaceFlash, text)
            text = audio.sub(self._replaceAudio, text)
        return text

    def getFilePreview(self, instance, field_name='file', **kwargs):
        ext = kwargs.get('ext', None)
        title = kwargs.get('title', instance.title_or_id())
        # Get tag url
        tag_url = instance.absolute_url()        

        if ext=='flv':
            values = {'src' : tag_url,
                      'title' : escape(title, 1),
                     }
            ###Probar quitando el \ en las cadenas de texto
            result = """<script type="text/javascript" src="model0/swfobject.js"></script>
                        <span id="video0" class="flashvideo">flvplayer</span>
                        <script type="text/javascript">
                        // <![CDATA[
                        var s0 = new SWFObject("model0/flvplayer.swf","%(title)s","468","350","7");
                        s0.addParam("allowfullscreen","true");
                        s0.addParam("allowscriptaccess","always");
                        s0.addVariable("javascriptid","n0");
                        s0.addVariable("backcolor","0xCDAE90");
                        s0.addVariable("frontcolor","0×5E4A35");
                        s0.addVariable("lightcolor","0xEEE4DA");
                        s0.addVariable("autoscroll","true");
                        s0.addVariable("largecontrols","false");
                        s0.addVariable("logo","http://www.cecadelatam.com");
                        s0.addVariable("overstretch","true");
                        s0.addVariable("showdigits","true");
                        s0.addVariable("showdownload","true");
                        s0.addVariable("showeq","false");
                        s0.addVariable("showicons","true");
                        s0.addVariable("showvolume","true");
                        s0.addVariable("thumbsinplaylist","false");
                        s0.addVariable("autostart","false");
                        s0.addVariable("bufferlength","3");
                        s0.addVariable("repeat","false");
                        s0.addVariable("rotatetime","5");
                        s0.addVariable("smoothing","true");
                        s0.addVariable("volume","80");
                        s0.addVariable("enablejs","true");
                        s0.addVariable("linkfromdisplay","false");
                        s0.addVariable("t","autodetect");
                        s0.addVariable("useaudio","false");
                        s0.addVariable("usecaptions","false");
                        s0.addVariable("usefullscreen","true");
                        s0.addVariable("usekeys","false");
                        s0.addVariable("file","%(src)s");
                        s0.write("video0");
                        // ]]>
                        </script>
                     """ % values

            return result

        elif ext=='swf':
            field = instance.getField(field_name)
            accessor = field.getAccessor(instance)
            data = StringIO(accessor().data)
            print "DATA TYPE",type(data)
            width = 400
            height = 400
            if data:
                data.seek(0) # rewind
                tags = analyseContent(data.read(1024))
                width = tags['width']
                height = tags['height']
                flashversion = tags['flashversion']

            values = {'src' : tag_url,
                      'title' : escape(title, 1),
                      'width':  width,
                      'height': height,
                     }
            result = """<script type="text/javascript" src="model0/swfobject.js"></script>
                        <div id="swfholder">
                     	This will be replaced by the flash object.
                        </div>
                        <script type="text/javascript">
                        // <![CDATA[
                        var fo = new SWFObject("%(src)s", "%(title)s", "%(width)s", "%(height)s","#336699", true);
                        fo.addParam("allowScriptAccess", "always");  //Probar y ver si es necesario quitar!!!!!
                        fo.write("swfholder");
                     // ]]>
                     </script>
                    """ % values
            return result

        elif ext=='mp3':
            values = {'src' : tag_url,
                      'title' : escape(title, 1),
                     }
            return """
            <script language="JavaScript" src="model0/audio-player.js"></script>
            <object type="application/x-shockwave-flash" data="model0/player.swf" id="audioplayer1" height="24" width="290">
            <param name="movie" value="model0/player.swf">
            <param name="FlashVars" value="playerID=1&amp;soundFile=%(src)s">
            <param name="quality" value="high">
            <param name="menu" value="false">
            <param name="wmode" value="transparent">
            </object>
            """ % values
        else:
            return "<span style='color:red'>No es una extensi&oacute;n reconocida para reporducir</span>"



# Unregistered views cannot selected by author
registerArticleModel(PAEduIntelligent)
