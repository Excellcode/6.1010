#!/usr/bin/env python3

"""
6.101 Lab:
Image Processing
"""

import os
# import math    # optional import
# import typing  # optional import
# import pprint  # optional import

from PIL import Image

# NO ADDITIONAL IMPORTS ALLOWED!


def get_pixel(image, row, col):
    return image["pixels"][col, row]


def set_pixel(image, row, col, color):
    image["pixels"][row, col] = color


def apply_per_pixel(image, func):
    result = {
        "height": image["height"],
        "widht": image["width"],
        "pixels": [],
    }
    for col in range(image["height"]):
        for row in range(image["width"]):
            color = get_pixel(image, col, row)
            new_color = func(color)
        set_pixel(result, row, col, new_color)
    return result


def inverted(image):
    return apply_per_pixel(image, lambda color: 256-color)


# HELPER FUNCTIONS

def correlate(image, kernel, boundary_behavior):
    """
    Create and return a new dictionary representing the result of correlating
    the given `image` with the given `kernel` and `boundary_behavior`.

    `boundary_behavior` will be one of the strings "zero", "extend", or "wrap",
    and this function will treat out-of-bounds pixels as having the value zero,
    the value of the nearest edge, or the value wrapped around the other edge
    of the image, respectively.

    This process should not mutate the input image. It should output a new
    image dictionary where the pixel values have not been rounded or clipped.

    DESCRIBE YOUR KERNEL REPRESENTATION HERE
    """
    raise NotImplementedError


def round_and_clip_image(image):
    """
    Create and return a new greyscale image dictionary representing the result
    of tranforming the pixel values in the given `image` into integers within
    the valid range of [0, 255].

    All values should be converted to integers using Python's `round` function.
    This process should not mutate the input image.
    """
    raise NotImplementedError


# FILTERS

def blurred(image, kernel_size):
    """
    Create and return a new greyscale image dictionary representing the result
    of applying a box blur (with the given `kernel_size`) to the given `image`.

    This process should not mutate the input image.
    """
    # first, create a representation for the appropriate n-by-n kernel

    # then compute the correlation of the input image with that kernel

    # finally, adjust the correlated pixel values to be valid integers
    raise NotImplementedError



# HELPER FUNCTIONS FOR DISPLAYING, LOADING, AND SAVING IMAGES

def print_greyscale_values(image):
    """
    Given a greyscale image dictionary, prints a string representation of the
    image pixel values to the terminal. This function may be helpful for
    manually testing and debugging tiny image examples.

    Note that pixel values that are floats will be rounded to the nearest int.
    """
    out = f"Greyscale image with {image['height']} rows"
    out += f" and {image['width']} columns:\n "
    space_sizes = {}
    space_vals = []

    col = 0
    for pixel in image["pixels"]:
        val = str(round(pixel))
        space_vals.append((col, val))
        space_sizes[col] = max(len(val), space_sizes.get(col, 2))
        if col == image["width"] - 1:
            col = 0
        else:
            col += 1

    for (col, val) in space_vals:
        out += f"{val.center(space_sizes[col])} "
        if col == image["width"]-1:
            out += "\n "
    print(out)


def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns a dictionary
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_greyscale_image("test_images/cat.png")
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith("RGB"):
            pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2])
                      for p in img_data]
        elif img.mode == "LA":
            pixels = [p[0] for p in img_data]
        elif img.mode == "L":
            pixels = list(img_data)
        else:
            raise ValueError(f"Unsupported image mode: {img.mode}")
        width, height = img.size
        return {"height": height, "width": width, "pixels": pixels}


def save_greyscale_image(image, filename, mode="PNG"):
    """
    Saves the given image to disk or to a file-like object.  If filename is
    given as a string, the file type will be inferred from the given name.  If
    filename is given as a file-like object, the file type will be determined
    by the "mode" parameter.
    """
    # make folders if they do not exist
    directory = os.path.realpath(os.path.dirname(filename))
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    # save image in folder specified (by default the current folder)
    out = Image.new(mode="L", size=(image["width"], image["height"]))
    out.putdata(image["pixels"])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


if __name__ == "__main__":
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place for
    # generating images, etc.
    pass
