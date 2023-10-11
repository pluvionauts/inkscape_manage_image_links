#!/usr/bin/env python
# coding=utf-8

"""
This extension resolves svg links so that they become editable svgs.
"""

import inkex
import sys
import os

import lxml

class ResolveSvgHref(inkex.EffectExtension):
    """EffectExtension to resolve svg links."""
    def add_arguments(self, pars):
        pass # We don't need arguments for this extension

    def effect(self):
        if not self.svg.selection:
            inkex.utils.errormsg(_("ERROR: No objects selected. This extension requires to select the objects that hold the links to resolve."))
        else:
            for element in self.svg.selection:
                self.effect_on_element(element)

    def effect_on_element(self, element):
        if element.tag_name == "image" and element.get("xlink:href") and element.get("xlink:href").endswith(".svg"):
            # create new element
            new_element = lxml.etree.SubElement(element.getparent(), "g")
            link_path = element.get("xlink:href")
            if link_path.startswith("file://"):
                link_path = os.path.relpath(link_path[len("file://"):], self.svg_path())
            new_element.set("inkscape:label", "svglink:{}".format(link_path))
            new_element.set("svglink:href", link_path)
            if element.get("x") and element.get("y"):
                new_element.set("svglink:origin:x", element.get("x"))           
                new_element.set("svglink:origin:y", element.get("y"))
            new_element.set("svglink:image-svg-dpi", element.get("inkscape:svg-dpi"))
            new_element.set("svglink:image-height", element.get("height"))
            new_element.set("svglink:image-width", element.get("width"))
            if element.get("transform"):
                new_element.set("transform", element.get("transform"))
            # load linked svg
            loaded_svg_tree = self.load(element.get("xlink:href"))
            loaded_root = loaded_svg_tree.getroot()
            for child in loaded_root:
                new_element.append(child)
                if element.get("x") and element.get("y"):
                    if child.get("transform"):
                        child.set("transform", child.get("transform") + " translate({x}, {y})".format(x=element.get("x"), y=element.get("y")))
                    else:
                        child.set("transform", "translate({x}, {y})".format(x=element.get("x"), y=element.get("y")))
            element.getparent().remove(element)
        elif element.tag_name == "g" and element.get("svglink:href"):
            # update the link if necessary
            if element.get("inkscape:label") != "svglink:{}".format(element.get("svglink:href")) and os.path.exists(self.svg_path() + "/" + element.get("inkscape:label")[len("svglink:"):]):
                print("INFO: The link {} has been changed to {}.".format(element.get("svglink:href"), element.get("inkscape:label")[len("svglink:"):]), file=sys.stderr)
                element.set("svglink:href", element.get("inkscape:label")[len("svglink:"):])
            # create new element
            new_element = lxml.etree.SubElement(element.getparent(), "g")
            ## copy attributes
            for key in element.attrib:
                new_element.attrib[key] = element.attrib[key]
            # load linked svg
            loaded_svg_tree = self.load("file://" + self.svg_path() + "/" + element.get("svglink:href"))
            loaded_root = loaded_svg_tree.getroot()
            for child in loaded_root:
                new_element.append(child)
                if element.get("svglink:origin:x") and element.get("svglink:origin:y"):
                    if child.get("transform"):
                        child.set("transform", child.get("transform") + " translate({x}, {y})".format(x=element.get("svglink:origin:x"), y=element.get("svglink:origin:y")))
                    else:
                        child.set("transform", "translate({x}, {y})".format(x=element.get("svglink:origin:x"), y=element.get("svglink:origin:y")))
            element.getparent().remove(element)
        else:
            # otherwise try to process children
            for child in element:
                self.effect_on_element(child)

if __name__ == '__main__':
    ResolveSvgHref().run()
