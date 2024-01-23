# SquiggleDraw Inkscape Extension
 
Inkscape "native" version of the SquiggleDraw Processing app.

![SquiggleDraw UI with CMYK Example](./images/ss_1.png?raw=true)

This is a complete rewrite with new version of the primary algorithm, taking into account differences in programming language and host application.

This version:
- is faster
- can handle large images with ease
- produces smoother "squiggles"
- can output CMYK color separations for use with CMY pens
- can process transparent images (makes background white)

Notes:

- CMYK is actually CMY due to the way Inkscape converts RGB to CMYK (they remove K). C + M + Y will produce K when overlapping ("rich black") and with cyan, magenta, and yellow ink pens, plots should mix appropriately.

- Use of this extension on images created via Inkscape's "Make Bitmap Copy" feature will sometimes produce unexpected results. It is better to create your bitmaps outside of Inkscape.
