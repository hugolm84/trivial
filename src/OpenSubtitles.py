#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2011-2012 Hugo Lindström
# Copyright (C) 2011-2012 Martin Törnqvist
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


# Open urls

import urllib
import urllib2
import re
from lxml.html import fromstring

class OpenSubtitles():
    langs = ["eng", "swe"]
    baseUrl = "http://www.opensubtitles.org/en/search2/sublanguageid"
    dlUrl ="http://www.opensubtitles.org"
    pattern = re.compile(r'\s+')
    searchResults = {}
    
    def __init__(self):
        pass
    
    def getSubtitle(self, movieName, language ):
        self.movieName = movieName
        self.language = language
        html = self.getResponse(self.__buildUrl())
        self.parseHtml(html)
        
    def parseHtml(self, html):
        movies = []
        results = html.xpath("//table[contains(@id, 'search_results')]")
        try:
            if results[0] :
                table = html.xpath("//td[contains(@id, 'main')]")
                for idx, item in enumerate(table):
                    movie = item.xpath(".//a[@class='bnone']")
                    movieName = movie[0].text_content()
                    movieName = re.sub(self.pattern, '', movieName)
                    movieUrl = movie[0].attrib["href"]
                    result = self.doUrlStuff("%s%s" % (self.baseUrl , movieUrl), movieName)
                    movies.append(result)
        except IndexError:
            download = html.xpath("//h1/a[@title='Download']")
            movies.append({"title" : download[0].text_content(), "downloadUrl" : download[0].attrib["href"] });                 
        
        for idx, movie in enumerate(movies):
            print "%d. %s" % (idx, movie["title"])
            
        choice = raw_input("Choose movie: ")
        try:
            self.download(movies[int(choice)]["downloadUrl"], movies[int(choice)]["title"])
        except Exception, e: 
            print "Error"
            print e
        
    def download(self, url, title):
        urllib.urlretrieve ("%s%s" % (self.dlUrl, url), "%s.%s" % (title, "zip"))

    def doUrlStuff(self, url, movieName = None):
        html = self.getResponse(url)
        row = html.xpath("//tr[contains(@id, 'name')]//td")
        result = {}
        for idx, item in enumerate(row):
            if idx is 0:
                if not movieName :
                    movieName = item.text_content()
                    movieName = re.sub(self.pattern, '', movieName);
                result["title"] = movieName
            if idx is 1:
                lang = item.xpath(".//a")
                result["language"] = lang[0].attrib["title"]
            elif idx is 4:
                downloadUrl = item[0].attrib["href"];
                result["downloadUrl"] = downloadUrl
            elif idx is 7:
                result["imdb"] = item.text_content()
        return result;
    
    def __buildUrl(self):
        movie = urllib.quote_plus(self.movieName)
        url = "%s-%s/moviename-%s" % (self.baseUrl, self.language, movie)
        return url

    def getResponse(self, url):
        response = urllib2.urlopen(url)
        return fromstring(response.read())