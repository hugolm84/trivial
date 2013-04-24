#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2011-2012 Hugo Lindström
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import urllib2
import re
from lxml.html import fromstring, tostring

class SubtitleBase(object):

    __strip_pattern = re.compile(r'\s+')
    
    def __init__(self):
        pass
    
    def getResponse(self, url):
        response = urllib2.urlopen(url)
        return fromstring(response.read())

    def strip(self, item):
        item = re.sub(self.__strip_pattern, ' ', item.text_content())
        return item

    def getSubtitle(self, query = {}):
        self.searchQuery = query.get("query")
        self.language = query.get("language") if query.get("language") else "all"
        return self.parseHtml(self.getResponse(self.buildUrl()))
        #return self.parseHtml(self.parseLocal(self.language))

    def download(self, url, rlsName = None):
        fileName = rlsName if rlsName is not None else self.searchQuery
        urllib.urlretrieve ("%s%s" % (self.baseUrl, url), "%s.%s" % (fileName, "zip"))
    
    def parseLocal(self, file):
        return fromstring(open("%s.html" % file).read());

    def parseMovieName(self):
        raise NotImplementedError( "Scraper needs to implement this!")

    def buildUrl(self):
        raise NotImplementedError( "Scraper needs to implement this!")

    def parseHtml(self, html, result = []):
        raise NotImplementedError( "Scraper needs to implement this!")
