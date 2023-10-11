#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2023 Rémi MONTHILLER, remi.monthiller@gmail.com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
"""
This extension resolves svg links so that they become editable svgs.
"""

import inkex
import sys
import os

import lxml

class UnresolveSvgHref(inkex.EffectExtension):
    """EffectExtension to unresolve svg links: Converts back resolved svg links into linked images."""
    def add_arguments(self, pars):
        pass # We don't need arguments for this extension

    def effect(self):
        if not self.svg.selection:
            inkex.utils.errormsg(_("ERROR: No objects selected. This extension requires to select the objects that hold the links to resolve."))
        else:
            for element in self.svg.selection:
                self.effect_on_element(element)

    def effect_on_element(self, element):
        if element.tag_name == "g" and element.get("svglink:href"):
            # update the link if necessary
            if element.get("inkscape:label") != "svglink:{}".format(element.get("svglink:href")) and os.path.exists(self.svg_path() + "/" + element.get("inkscape:label")[len("svglink:"):]):
                print("INFO: The link {} has been changed to {}.".format(element.get("svglink:href"), element.get("inkscape:label")[len("svglink:"):]), file=sys.stderr)
                element.set("svglink:href", element.get("inkscape:label")[len("svglink:"):])
            # create new element
            new_element = lxml.etree.SubElement(element.getparent(), "image")
            new_element.set("x", element.get("svglink:origin:x"))
            new_element.set("y", element.get("svglink:origin:y"))
            new_element.set("inkscape:svg-dpi", element.get("svglink:image-svg-dpi"))
            new_element.set("height", element.get("svglink:image-height"))
            new_element.set("width", element.get("svglink:image-width"))
            new_element.set("xlink:href", element.get("svglink:href"))
            if element.get("transform"):
                new_element.set("transform", element.get("transform"))
            # remove old element
            element.getparent().remove(element)
        else:
            # otherwise try to process children
            for child in element:
                self.effect_on_element(child)

if __name__ == '__main__':
    UnresolveSvgHref().run()
