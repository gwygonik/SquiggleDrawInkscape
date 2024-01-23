import sys
import random
import base64

import inkex
from inkex import PathElement, Transform

import numpy as np

from io import BytesIO
from lxml import etree
from PIL import Image, ImageFilter, ImageOps

import colorsys


def process_selected_image(self, embedded_image, rows, cols, display_width, display_height, invert):
    # convert embedded image to PIL image
    my_href = embedded_image.get('xlink:href')
    base64_string = my_href.split('base64,')[1]
    img_stream = BytesIO()
    img_stream.write(base64.b64decode(base64_string))
    im = Image.open(img_stream)
    im.save(img_stream, format='PNG')

    # convert to grayscale and blur it
    im = im.convert('L')
    if invert == 'true':
        im = ImageOps.invert(im)
    im = im.filter(ImageFilter.GaussianBlur)
    tmp_im = im.resize((cols,rows))
    im = tmp_im.resize((display_width+1, display_height+1), Image.LANCZOS)

    return im

def process_selected_image_CMYK(self, embedded_image, rows, cols, display_width, display_height, invert):
    # convert embedded image to PIL image
    my_href = embedded_image.get('xlink:href')
    base64_string = my_href.split('base64,')[1]
    img_stream = BytesIO()
    img_stream.write(base64.b64decode(base64_string))
    im = Image.open(img_stream)
    im.save(img_stream, format='PNG')

    # convert to CMYK and split image
    im = im.convert('CMYK')
    c,m,y,k = im.split()
    if invert == 'true':
        c = ImageOps.invert(c)
        m = ImageOps.invert(m)
        y = ImageOps.invert(y)
        k = ImageOps.invert(k)
    # invert (possibly again) to make sure color separations are correct (white = empty, black = 100% color channel)
    c = ImageOps.invert(c.convert('L'))
    m = ImageOps.invert(m.convert('L'))
    y = ImageOps.invert(y.convert('L'))
    k = ImageOps.invert(k.convert('L'))

    tmp_im = c.resize((cols,rows))
    c = tmp_im.resize((display_width+1, display_height+1), Image.LANCZOS)

    tmp_im = m.resize((cols,rows))
    m = tmp_im.resize((display_width+1, display_height+1), Image.LANCZOS)

    tmp_im = y.resize((cols,rows))
    y = tmp_im.resize((display_width+1, display_height+1), Image.LANCZOS)

    tmp_im = k.resize((cols,rows))
    k = tmp_im.resize((display_width+1, display_height+1), Image.LANCZOS)

    im = None
    tmp_im = None
    del im
    del tmp_im
    
    return c,m,y,k

def get_attributes_long(self):
    """ Returns a string containing all object attributes
            - One attribute per line
    """
    attribute_string = ''
    for att in dir(self):
        try:
            attname, attribute = (att, getattr(self, att))
            attribute_string = attribute_string + str(attname) + '\t\t'  + str(attribute) + '\n'
        except:
            None
    return attribute_string

def get_attributes(self):
    for att in dir(self):
        try:
            inkex.errormsg((att, getattr(self, att)))
        except:
            None

class SquiggleDraw(inkex.GenerateExtension):
    container_label = 'Squiggles'
    container_layer = True

    working_image = None
    image_bounds = None
    start_x = 0
    start_y = 0
    sq_width = 0
    sq_height = 0
    divisors = [128, 64, 32, 16, 8]
    bidi = 'false'
    connect_ends = 'false'
    transform_orig = None
    transform_reset = None
    has_starting_transform = False

    def add_arguments(self, pars):
        pars.add_argument("--rows", type=int, default=10, help="Number of Rows")
        pars.add_argument("--cols", type=int, default=10, help="Number of Columns")
        pars.add_argument("--freq", type=int, default=2, help="Squiggle Frequency")
        pars.add_argument("--amp", type=int, default=2, help="Squiggle Amplitude")
        pars.add_argument("--invert", type=str, help="Invert Colors")
        pars.add_argument("--path_type", type=str, dest='path_type', default='uni', help="Bidirectional Paths")
        pars.add_argument("--color_mode", type=str, dest="color_mode", default='gray', help="Color Seperation Type")
        #
        pars.add_argument("--squiggledraw_notebook", type=str, dest="squiggledraw_notebook", default=0)        

    def generate(self):

        if self.options.path_type == 'bidi':
            self.bidi = 'true'
            self.connect_ends = 'false'
        elif self.options.path_type == 'join':
            self.bidi = 'true'
            self.connect_ends = 'true'
        else:
            self.bidi = 'false'
            self.connect_ends = 'false'

        if len(self.svg.selected) > 0:
            selected_image = self.svg.selected[0]

            if selected_image.transform:
                self.has_starting_transform = True
                self.transform_orig = selected_image.transform

            self.transform_reset = Transform(((1.0, 0.0, 0.0), (0.0, 1.0, 0.0)))
            selected_image.transform = self.transform_reset
            image_bounds = selected_image.bounding_box()

            out_style = {}
            out_label = ''

            if selected_image.TAG == 'image':
                if self.options.color_mode == 'gray':
                    # grayscale

                    out_style = {'fill' : 'none', 'stroke' : '#000000', 'stroke-width' : '0.25'}
                    self.working_image = process_selected_image(self, selected_image, self.options.rows, self.options.cols, round(float(image_bounds.width)), round(float(image_bounds.height)), self.options.invert)
                    self.start_x = float(image_bounds.left)
                    self.start_y = float(image_bounds.top)
                    self.sq_width = float(image_bounds.width)
                    self.sq_height = float(image_bounds.height)
                    out_label = 'gray'
                    yield self.create_squiggles(self.options.freq, out_style, out_label)
                    selected_image.style['display'] = 'none'
                else:
                    # CMYK

                    c,m,y,k = process_selected_image_CMYK(self, selected_image, self.options.rows, self.options.cols, round(float(image_bounds.width)), round(float(image_bounds.height)), self.options.invert)
                    im_cmy = [c,m,y]
                    idx = 0
                    for im in im_cmy:
                        self.working_image = im
                        self.start_x = float(image_bounds.left)
                        self.start_y = float(image_bounds.top)
                        self.sq_width = float(image_bounds.width)
                        self.sq_height = float(image_bounds.height)
                        if idx == 0:
                            out_style = {'fill' : 'none', 'stroke' : '#00ffff', 'stroke-width' : '0.25', 'mix-blend-mode' : 'darken'}
                            out_label = 'cyan'
                        elif idx == 1:
                            out_style = {'fill' : 'none', 'stroke' : '#ff00ff', 'stroke-width' : '0.25', 'mix-blend-mode' : 'darken'}
                            out_label = 'magenta'
                        elif idx == 2:
                            out_style = {'fill' : 'none', 'stroke' : '#ffff00', 'stroke-width' : '0.25', 'mix-blend-mode' : 'darken'}
                            out_label = 'yellow'
                        idx += 1
                        yield self.create_squiggles(self.options.freq, out_style, out_label)
                    selected_image.style['display'] = 'none'

            else:
                inkex.errormsg('Please Select an Image')

            if self.has_starting_transform == True:
                selected_image.transform = self.transform_orig

        else:
            inkex.errormsg('Please Select an Image')

    def create_squiggles(self, freq, in_style, in_label):
        el = PathElement()
        currentCurve = ""
        sq_divisor = self.divisors[self.options.amp]
        sq_max = 256 / sq_divisor;
        for y in range(0, self.options.rows):
            cx = self.start_x 
            cy = self.start_y + (self.sq_height/self.options.rows*(y+1)) - (self.sq_height/self.options.rows/2)
            xinc = (self.sq_width / (self.options.cols-1))

            startX = 0
            endX = self.options.cols-1
            stepX = 1

            if self.bidi == 'true' and y % 2 != 0:
                cx = self.start_x + self.sq_width
                startX = self.options.cols-2
                endX = -1
                xinc *= -1
                stepX = -1

            if self.connect_ends != 'true':
                currentCurve += f"M {cx},{cy} "
            else:
                if y == 0 or self.bidi != 'true':
                    currentCurve += f"M {cx},{cy} "

            for x in range(startX, endX, stepX):
                sq_amp = sq_max - self.working_image.getpixel((x * (self.sq_width / self.options.cols), y * (self.sq_height/self.options.rows)))/sq_divisor
                if self.bidi == 'true' and y % 2 != 0:
                    sq_amp *= -1
                for sq in range(0,self.options.freq):
                    currentCurve += f'q {xinc/4/self.options.freq},{sq_amp/2} {xinc/2/self.options.freq},0 t {xinc/2/self.options.freq} 0 '

            if self.connect_ends == 'true' and y < self.options.rows-1:
                currentCurve += f'q {xinc/2},0 {xinc/2},{self.sq_height/self.options.rows/2} t {-xinc/2} {self.sq_height/self.options.rows/2} '

        el.set('d', currentCurve)
        el.style = in_style
        el.set('inkscape:label', f'squiggle_{in_label}')
        el.transform = self.transform_orig
        return el

if __name__ == '__main__':
    SquiggleDraw().run()