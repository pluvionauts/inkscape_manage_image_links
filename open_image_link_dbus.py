#!/usr/bin/env python
# coding=utf-8

import sys
import os

import lxml

import gi
gi.require_version("Gio", "2.0")
from gi.repository import Gio, GLib

if __name__ == '__main__':
    try:
       bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
    except BaseException:
       # print("ERROR: No DBus bus", file=sys.stderr)
       exit()
    # print ("INFO: Got DBus bus", file=sys.stderr)
    proxy = Gio.DBusProxy.new_sync(bus, Gio.DBusProxyFlags.NONE, None,
                                  'org.freedesktop.DBus',
                                  '/org/freedesktop/DBus',
                                  'org.freedesktop.DBus', None)
    names_list = proxy.call_sync('ListNames', None, Gio.DBusCallFlags.NO_AUTO_START, 500, None)
    # names_list is a GVariant, must unpack
    names = names_list.unpack()[0]
    # Look for Inkscape; names is a tuple.
    for name in names:
       if ('org.inkscape.Inkscape' in name):
           # print ("INFO: Found: " + name, file=sys.stderr)
           break

    appGroupName = "/org/inkscape/Inkscape"
    winGroupName = appGroupName + "/window/1"
    docGroupName = appGroupName + "/document/1"

    applicationGroup = Gio.DBusActionGroup.get( bus, name, appGroupName)
    windowGroup = Gio.DBusActionGroup.get(bus, name, winGroupName)
    documentGroup = Gio.DBusActionGroup.get(bus, name, docGroupName)

    applicationGroup.activate_action('element-image-edit', None)
