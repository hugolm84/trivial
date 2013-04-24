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

import sys
from SubtitleSearch import SubtitleSearch

def usage():
    print 'Usage: python', sys.argv[0], '<search string>'

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    Subtitles = SubtitleSearch()
    Subtitles.getSubtitles({'query' : ' '.join(sys.argv[1:]), 'language' : 'eng,swe'})
