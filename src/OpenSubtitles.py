#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2011-2013 Hugo Lindström
# Copyright (C) 2011-2013 Martin Törnqvist
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

from SubtitleBase import SubtitleBase
import urllib
#from bs4 import UnicodeDammit

class OpenSubtitles(SubtitleBase):
    baseUrl = "http://www.opensubtitles.org"
    searchUrl = "/en/search2/sublanguageid"
    col9Headers = ["title", "lang", "cds", "uploaded", "download", "rating", "comments", "imdb", "uploader" ]
    subtitleTypes = ["hearing_impaired", "hd", "from_trusted"]

    def buildUrl(self):
        return "%s%s-%s/moviename-%s" % (self.baseUrl, self.searchUrl, self.language, urllib.quote_plus(self.searchQuery))

    def parseHtml(self, html, movies = []):
        table = html.xpath("//tr[contains(@id, 'name')]")    
        if len(table) is 0:
            movies.append(self.parseSingleItem(html))
            return movies
    
        for idx, item in enumerate(table):
            numCols = len(item.getchildren())
            if numCols is 9: 
                data = self.parse9ColTd(item)
                if len(data) : movies.append(data)
            if numCols is 5:
                self.parseHtml(self.getResponse("%s%s" % (self.baseUrl , item.xpath(".//a[@class='bnone']")[0].attrib["href"])), movies)
    
        return movies;

    def parseSingleItem(self, html):
        item = html.xpath("//h1/a[@title='Download']");
        return {"title" : item[0].text_content(), "download" : item[0].attrib["href"]};   

    def parseMovieName(self, item):
        movieItem = item.find("strong")[0]
        movieUrl = movieItem.attrib["href"]
        movieName = self.strip(movieItem)
        types = {}
        rlsName = item.text_content()
        for element in item.iterchildren():
            try:
                for type in self.subtitleTypes:
                    if element.attrib["src"].find(type):
                        types[type] = True
            except KeyError:
                pass
            rlsName = rlsName.replace(element.text_content(), "")
        
        if rlsName.find(self.searchQuery) or movieName.find(self.searchQuery):
            return {"title" : movieName, "url" : movieUrl, "rls" : rlsName, "types" : types}
        return {}
    
    def parse9ColTd(self, item):
        data = {}
        for idx, td in enumerate(item.iterchildren()):
            if idx is 0:
                data = self.parseMovieName(td)
            elif idx is 1:
                data[self.col9Headers[idx]] = td[0].attrib["title"]
            elif idx is 4:
                data[self.col9Headers[idx]] = td[0].attrib["href"]
            else:
                data[self.col9Headers[idx]] = self.strip(td)
        
        return data if "title" in data else {}
