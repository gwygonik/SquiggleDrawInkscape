# SquiggleDraw Inkscape Extension
 
Inkscape "native" version of the SquiggleDraw Processing app.

This is a complete rewrite with new version of the primary algorithm, taking into account differences in programming language and host application.

This version:
- is faster
- can handle large images with ease
- produces smoother "squiggles"
- can output CMYK color separations for use with CMY pens

Notes:

- CMYK is actually CMY due to the way Inkscape converts RGB to CMYK (they remove K). C + M + Y will produce K when overlapping ("rich black") and with cyan, magenta, and yellow ink pens, plots should mix appropriately.

- Using this extension on images created with Inkscape's "Make Bitmap Copy" feature will sometimes produce unexpected results.
