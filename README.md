# SquiggleDraw Inkscape Extension

> *NOTE: this repo does not yet include an installer. You can copy the .inx and .py files to your extension folder on your computer and things will work.* [(See: Inkscape Documentation on Installing Extensions)](https://inkscape-manuals.readthedocs.io/en/latest/extensions.html#installing-extensions)

**Inkscape 1.3+ "native" version of the [SquiggleDraw Processing app](https://github.com/gwygonik/SquiggleDraw/).**

This extension will convert the brightness or color intensity of a grayscale or color image into sinewave SVG paths that can then be pen plotted, laser engraved, or used for any purpose you desire! 

![SquiggleDraw output example in grayscale](./images/ss_3.png?raw=true)

There are user-editable parameters for how detailed the resulting paths are, the intensity and density of the sinewaves, and how the paths are rendered.

![SquiggleDraw UI with CMYK Example](./images/ss_1.png?raw=true)

### Features:
- Control over the number of rows and columns
- Size of the Squiggles
- Frequency of the Squiggles
- Inverting the image colors
- Path direction:
  - -> (Left-to-Right)
  - <- (Right-to-Left)
  - Connected ends (Back and forth)
- Modes:
  - Single-color mode
  - CMYK color mode

This is a complete rewrite with the new version of the primary algorithm, taking into account differences in programming language and host application.

Compared to the Processing version, this extension:
- is faster
- can handle large images with ease (memory-dependent)
- produces smoother "squiggles"
- can output CMYK color separations for use with CMY pens
- can process transparent images (makes background white)

### How to use:
1. Select the image you want to convert.
2. Go to the top menus Extensions -> Render -> SquiggleDraw
3. Enable Live preview check box (if desired)
4. Experiment with parameters until you are happy with the results
5. Click Apply 

### Notes:

- This extension has only been tested with Inkscape 1.3, but might work in previous versions.
- CMYK is actually CMY due to the way Inkscape converts RGB to CMYK (they remove K). C + M + Y will produce K when overlapping ("rich black") and with cyan, magenta, and yellow ink pens, plots should mix appropriately.
- If your image is too big and is crushing Inkscape, you can scale it down and use Inkscape's "Edit -> Make a Bitmap Copy" feature before using this extension. **Be aware that the "Make a Bitmap Copy" feature can produce unexpected or inconsistent results. It is more reliable to create and scale your bitmaps outside of Inkscape.**

---
![SquiggleDraw UI with close-up of CMYK Example](./images/ss_2.png?raw=true)
