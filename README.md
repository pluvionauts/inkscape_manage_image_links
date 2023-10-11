# Inkscape Extensions to Manage Image Links

**NOTE: Even though the extensions might be usable, everything is still work in progress.**

Set of basic extensions to manage image links within Inkscape.

It includes:

1. Open Image Links: opens an image link into a new window so that it can be edited independently.
2. SVG Image Link -> Embeded SVG: resolves the link and import as an SVG group into the current image.
3. Embeded SVG -> SVG Image Link: reverts the action of the previous extension.

This set of extensions might be particularly useful if one needs to work with linked SVGs while having the need for snapping.

## How it works

1. Open Image Links uses the DBUS interface of Inkscape and calls the element-image-edit action that opens an Image link into a new window.
2. SVG Image Link -> Embeded SVG loads the SVGs linked to the images selected, copies their contents and paste it into the current document within new groups that contain metadata regarding the linked image. The images selected are then deleted.
3. Embeded SVG -> SVG Image Link uses the metadata of the groups selected to revert the previous extension.

## Installation

Just drop the `*.inx` and `*.py` files in your extensions folder (usually `~/.config/inkscape/extensions` on Linux or `%APPDATA%\inkscape\extensions` on Windows).

## Usage

Before applying these extensions, SVG links must be imported (**File menu > Import...**) using the **Link the SVG file in an image tag**.
The extensions can then be found in the **Extensions menu > Pluvionauts > ...**.

License
-------

Most of the Open Image Links extension is based on the [Ink Dbus](https://gitlab.com/inklinea/ink-dbus) extension by Matt Cottam and is therefore under the [GNU General Public License version 3](https://www.gnu.org/licenses/gpl-3.0.en.html) or later.
The rest is licensed under the [MIT license](LICENSE).
