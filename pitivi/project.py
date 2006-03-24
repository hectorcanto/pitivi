#!/usr/bin/python
# PiTiVi , Non-linear video editor
#
#       project.py
#
# Copyright (c) 2005, Edward Hervey <bilboed@bilboed.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

"""
Project class
"""

import os.path
import gobject
import gst
from timeline import Timeline
from sourcelist import SourceList
from bin import SmartTimelineBin
from settings import ExportSettings

class Project(gobject.GObject):
    """ The base class for PiTiVi projects """

    name = ""
    settings = None
    description = ""
    uri = None
    sources = None
    settings = None
    timeline = None
    timelinebin = None

    def __init__(self, name="", uri=None):
        """
        name : the name of the project
        uri : the uri of the project
        """
        gst.log("name:%s, uri:%s" % (name, uri))
        gobject.GObject.__init__(self)
        self.name = name
        self.uri = uri
        self.sources = SourceList(self)
        self.settings = ExportSettings()
        self._load()

    def _load(self):
        """ loads the project from a file """
        if self.timeline:
            return
        self.timeline = Timeline(self)
        if self.uri:
            raise NotImplementedError

    def getBin(self):
        """ returns the SmartTimelineBin of the project """
        if not self.timeline:
            return None
        if not self.timelinebin:
            self.timelinebin = SmartTimelineBin(self)
        return self.timelinebin

    def _save(self, filename):
        """ internal save function """
        # TODO
        pass

    def save(self):
        """ Saves the project to the project's current file """
        self._save(self.uri)

    def saveAs(self, filename):
        """ Saves the project to the given file name """
        self._save(filename)
        


def file_is_project(uri):
    """ returns True if the given uri is a PitiviProject file"""
    # TODO
    if not gst.uri_get_protocol(uri) == "file":
        raise NotImplementedError("PiTiVi doesn't yet handle non local projects")
    return os.path.isfile(gst.uri_get_location(uri))

