#!/usr/bin/env python
# coding=utf-8

"""
This extension opens image links within Inkscape.
"""

import inkex
import sys
import os

import lxml

import subprocess

import warnings
warnings.filterwarnings("ignore")

def os_check():
    """
    Check which OS we are using
    :return: OS Name ( windows, linux, macos )
    """
    from sys import platform

    if 'linux' in platform.lower():
        return 'linux'
    elif 'darwin' in platform.lower():
        return 'macos'
    elif 'win' in platform.lower():
        return 'windows'

def call_dbus():
    if os_check() == 'windows':
        py_exe = sys.executable
        if 'pythonw.exe' in py_exe:
            py_exe = py_exe.replace('pythonw.exe', 'python.exe')

        DETACHED_PROCESS = 0x08000000
        subprocess.Popen([py_exe, 'gtk3_dbus.py', 'standalone'], creationflags=DETACHED_PROCESS)
    else:
        subprocess.Popen(['python3', 'open_image_link_dbus.py'],
                         preexec_fn=os.setpgrp, stdout=open('/dev/null', 'w'),
                         stderr=open('/dev/null', 'w'))

class OpenSvgHref(inkex.EffectExtension):
    """EffectExtension to open svg links."""
    def add_arguments(self, pars):
        pass # We don't need arguments for this extension

    def effect(self):
        if not self.svg.selection:
            inkex.utils.errormsg(_("ERROR: No image selected. This extension requires to select a single image that holds the svg link to open."))
        elif len(self.svg.selection) != 1:
            inkex.utils.errormsg(_("ERROR: Only one image that holds the svg link to open should be selected."))
        else:
            self.effect_on_element(self.svg.selection[0])

    def effect_on_element(self, element):
        if element.tag_name == "image" and element.get("xlink:href") and element.get("xlink:href").endswith(".svg"):
            call_dbus()
            sys.exit()
        else:
           inkex.utils.errormsg(_("ERROR: The object selected is not an image."))

if __name__ == '__main__':
    OpenSvgHref().run()
