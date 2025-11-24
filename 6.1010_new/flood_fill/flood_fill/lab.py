#!/usr/bin/env python3

"""
6.101 Lab:
Image Processing 2
"""

# NO ADDITIONAL IMPORTS!
# (except in the last part of the lab; see the lab writeup for details)
import os
# import math    # optional import
# import typing  # optional import
# import pprint  # optional import

from PIL import Image

# COPY THE FUNCTIONS THAT YOU IMPLEMENTED IN IMAGE PROCESSING PART 1 BELOW!
#!/usr/bin/env python3

"""
6.101 Lab:
Image Processing
"""

import os
import math    # optional import
# import typing  # optional import
# import pprint  # optional import

from PIL import Image

# NO ADDITIONAL IMPORTS ALLOWED!

#name change
def get_pixel(image, row, col):
    """ Returns a number representing the pixel in the intersection
    of specified row and column of an image array.
    Cannot access pixels that do not exist without considering edge effects. 
    Args:
        image: a dictionary representing the image
        row: the row of the pixel we are trying to access
        col: the column of the pixel we are trying to access
    """    
#   return image["pixels"][col, row]    
    return image["pixels"][image["width"]*row + col]


def set_pixel(image, row, col, color):
    """changes the pixel at a location specified by 'row' and 'col' in 'image' to 'color'
    """
#    image["pixels"][row, col] = color
    image["pixels"][image["width"]*row + col] = color


def apply_per_pixel(image, func):
    """ creates and returns a new image whose pixels are the outputs of
    applying 'func' to corresponding pixels in 'image'
    """
    result = {
        "height": image["height"],
        "width": image["width"], 
        "pixels": [0 for i in range(image["height"]*image["width"])]
    }
#        [0 for i in range(col*row)]
    
#    for col in range(image["height"]):
         
#        for row in range(image["width"]):
#    for row in range(image["height"]):

#        for col in range(image["width"]):
#extend            color = get_pixel(image, row, col)
    for i in range(len(result["pixels"])):
        result["pixels"][i] = func(image["pixels"][i] )
#       set_pixel(result, row, col, new_color)
#            set_pixel(result, row, col, new_color)
    return result 


def inverted(image):
    """creates and returnsba new image whose pixels are the outputs of
    applying an inversion to corresponding pixels in 'image'
    """
    return apply_per_pixel(image, lambda color: 255-color)
#256


# HELPER FUNCTIONS
#def get_kern(kernel, row, col):
#    return kernel["kerns"][row*kernel["width"] + col]
#
def get_pixel_extend(image, row, col, boundary_behavior = "zero"):
    """ Returns a number representing the pixel in the intersection of specified row and column of an image array.

    Args:
        image: a dictionary representing the image
        row: the row of the pixel we are trying to access
        col: the column of the pixel we are trying to access
        boundary_behavior: determines a pixel which we can't access directly by specifying how we approach edge effects
    """    
    assert (boundary_behavior in ["zero", "extend", "wrap"]), "boundary_behavior not known" #boundary_behavior limited to 3 options
#    row_norm = [i for i in range(image["height"])]
#    col_norm = [i for i in range(image["width"])]
    
    if boundary_behavior == "zero":
        if  row < 0 or row >= image["height"] or col < 0 or col >= image["width"]:
            return 0 
        return get_pixel(image, row, col)
#boundary_behavior for extend    
    elif boundary_behavior == "extend":
        
        row_new = min(max(0, row), image["height"] - 1)
        col_new = min(max(0, col), image["width"] - 1)
#        print(row_new, col_new)
        return get_pixel(image, row_new, col_new)
       
#boundary_behavior wrap
    else:
        return get_pixel(image, row % image["height"], col % image["width"])
            

#def get_pixel_extend_window(image, kernel, row, col, boundary_behavior = "extend"):
#    dimension = kernel["height"]
#    pixel_window = []
#    for index_row in range(-(dimension//2), dimension//2 + 1):
#        for index_col in range(-(dimension//2), dimension//2 + 1):
#            pixel_window.append(get_pixel_extend(image, row + index_row, col + index_col, boundary_behavior))     
#    return pixel_window

def apply_kernel_pixel(image, kernel, row, col, boundary_behavior = "extend"):
    """ helper function: returns the result of applying 'kernel' to a pixel specified by a 'row' and 'col' in 'image', acceses pixel in image based on 'boundary_behavior'
    """
    dimension = kernel["height"]
    total = 0
    track_kern = 0
    for row_index in range(row-(dimension//2), row + dimension//2 + 1):
        for col_index in range(col-(dimension//2), col + dimension//2 + 1):
            total += get_pixel_extend(image, row_index, col_index, boundary_behavior)*kernel["kerns"][track_kern]
            track_kern +=1 
    return total
    

def correlate(image, kernel, boundary_behavior = "extend"):
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
    KERNEL: A dictionary containing the following entries
        "width": the width of the kernel,
        "height": the height of the kernel,
        "kerns": a Python list of kernel entries stored in row-major order 
    """
    result = {
        "height": image["height"],
        "width": image["width"], 
        "pixels": [0 for i in range(image["height"]*image["width"])]
    }

    
    for row in range(image["height"]):
        for col in range(image["width"]):
            set_pixel(result, row, col, apply_kernel_pixel(image, kernel, row, col, boundary_behavior))
    return result 
    


def round_and_clip_image(image):
    """
    Create and return a new greyscale image dictionary representing the result
    of tranforming the pixel values in the given `image` into integers within
    the valid range of [0, 255].

    All values should be converted to integers using Python's `round` function.
    This process should not mutate the input image.
    """
    
#    return apply_per_pixel(image, lambda x: round(min(max(x,0), 255)))
    return apply_per_pixel(image, lambda x: min(max(round(x),0), 255))
        


# FILTERS

def blurred(image, kernel_size, boundary_behavior = "extend"):
    """
    Create and return a new greyscale image dictionary representing the result
    of applying a box blur (with the given `kernel_size`) to the given `image`.

    This process should not mutate the input image.
    """
    # first, create a representation for the appropriate n-by-n kernel
    kernel = {"height": kernel_size, "width": kernel_size, "kerns": [1/(kernel_size)**2 for i in range((kernel_size)**2)]}  

    # then compute the correlation of the input image with that kernel
    blur_correlate = correlate(image, kernel, boundary_behavior)
    

    # finally, adjust the correlated pixel values to be valid integers
    result = round_and_clip_image(blur_correlate)
    
    return result

def sharpened(image, kernel_size, boundary_behavior = "extend"):
    """Create and return a new greyscale image dictionary representing the result of
    applying an unsharp mask(with the 'given kernel size' to the given 'image')
    
    """
    #get a bulurred non rounded/clipped image
    kernel = {"height": kernel_size, "width": kernel_size, "kerns": [1/(kernel_size)**2 for i in range((kernel_size)**2)]}  

    blur_correlate = correlate(image, kernel, boundary_behavior)
    #run operation to get sharp image
    result = {
        "height": image["height"],
        "width": image["width"], 
        "pixels": [0 for i in range(image["height"]*image["width"])]
    }
    for row in range(image["height"]):
        for col in range(image["width"]):
            
            set_pixel(result, row, col, 2*get_pixel(image, row, col) - get_pixel(blur_correlate, row, col))
    return round_and_clip_image(result)

def edges(image):
    """"creates and returns a new image after applying edge effects to 'image'
    """
    kernel_1 =  {
        "height": 3,
        "width": 3, 
        "kerns": [-1, -2, -1, 0, 0, 0, 1, 2, 1]
    }     
    kernel_2 = {
        "height": 3,
        "width": 3,
        "kerns": [-1, 0, 1, -2, 0, 2, -1, 0, 1]
    }
    output_1 = correlate(image, kernel_1)
    output_2 = correlate(image, kernel_2)
    result = {
        "height": image["height"],
        "width": image["width"], 
        "pixels": [0 for i in range(image["height"]*image["width"])]
    }
    for row in range(image["height"]):
        for col in range(image["width"]):
            
            set_pixel(result, row, col, math.sqrt((get_pixel(output_1, row, col))**2 + (get_pixel(output_2, row, col))**2))
    return round_and_clip_image(result)  

# VARIOUS FILTERS


def color_filter_from_greyscale_filter(filt):
    """
    Given a filter that takes a greyscale image as input and produces a
    greyscale image as output, returns a function that takes a color image as
    input and produces the filtered color image, without modifying the input.
    """
    def output_func(image):
        output_red = filt({"height": image["height"],
        "width": image["width"], 
        "pixels": [item[0] for item in image["pixels"]]
        })
        output_green = filt({"height": image["height"],
        "width": image["width"], 
        "pixels": [item[1] for item in image["pixels"]]
        })
        output_blue = filt({"height": image["height"],
        "width": image["width"], 
        "pixels": [item[2] for item in image["pixels"]]
        })
        return {"height": image["height"],
        "width": image["width"], 
        "pixels": [(output_red["pixels"][i], output_green["pixels"][i], output_blue["pixels"][i]) for i in range(len(image["pixels"]))] 
        }
    return output_func

def make_blur_filter(kernel_size):
    def blur_filter(image):
        return blurred(image, kernel_size)
    return blur_filter

def make_sharpen_filter(kernel_size):
    def sharpen_filter(image):
        return sharpened(image, kernel_size)
    return sharpen_filter

def filter_cascade(filters):
    """
    Given a list of filters, where each filter is a function that takes an
    image as input and produces an image as output, return a function that
    takes an image as input and produces an image that results from applying
    all of the individual filter effects in order.
    """
    def final_cascade(image):
        output = image
        for i in range(len(filters)):
            output = filters[i](output)
        return output    
    return final_cascade

# SEAM CARVING

# Main Seam Carving Implementation


def seam_carving(color_image, num_cols):
    """
    Starting from the given color image, use the seam carving technique to
    remove num_cols (int) columns from the input image. Returns a new
    color image without modifying the original.
    """
    output = color_image
    for i in range(num_cols):
        grey_image = greyscale_image_from_color_image(output)
        cem = cumulative_energy_map(compute_energy(grey_image))
        output = image_without_seam(output, minimum_energy_seam(cem) )
    return output


# Optional Helper Functions for Seam Carving


def greyscale_image_from_color_image(color_image):
    """
    Given a color image, computes and returns a corresponding greyscale image.

    Returns a greyscale image dictionary without modifying the input image.
    """
    return {"height": color_image["height"],
        "width": color_image["width"], 
        "pixels": [round(0.299*item[0] + 0.587*item[1] + 0.114*item[2]) for item in color_image["pixels"]]
    }    

def compute_energy(grey_image):
    """
    Given a greyscale image, computes a measure of "energy" using the edges
    function from last week.

    Returns a greyscale image dictionary without modifying the input image.
    """
    return edges(grey_image)

def cumulative_energy_map(energy_image):
    """
    Given a greyscale energy image, computes a "cumulative energy map" (cem)
    as described in the lab 2 writeup.

    Returns a dictionary with 'height', 'width', and 'pixels' keys, but the
    values in the 'pixels' array may not necessarily be in the range [0, 255].
    """
    result = {"height": energy_image["height"],
        "width": energy_image["width"], 
        "pixels": energy_image["pixels"][:]
    }
    
    for row in range(1, energy_image["height"]):
        for col in range(0, energy_image["width"]):
            above_col =[]
            above_col.append(get_pixel(result, row - 1, col))
            if col > 0:
                above_col.append(get_pixel(result, row - 1, col - 1))
            if col < result["width"] - 1:
                above_col.append(get_pixel(result, row - 1, col + 1))
            result["pixels"][row*result["width"] + col] += min(above_col)
    return result

def minimum_energy_seam(cem):
    """
    Given a cumulative energy map (cem) dictionary, computes a set of the
    indices into the 'pixels' list that correspond to pixels contained in
    the minimum-energy seam (computed as described in the lab 2 writeup).
    """
    result = []
    bottom = cem["pixels"][cem["width"]*(cem["height"] - 1)::]
    bottom_index = bottom.index(min(bottom))
    result.append(bottom_index)
    count = 0
    for row in range(cem["height"] - 2, -1, -1):
        get_row = []
        main_col = result[count]
        count += 1
        
        for col in range(main_col - 1, main_col + 2):
            
            if (col >= 0) and (col < cem["width"]):
                get_row.append([col, get_pixel(cem, row, col)])
                          
        get_min = min([item[1] for item in get_row])
        for item in get_row:
            if item[1] == get_min:
                final_col = item[0]
                break
        result.append(final_col)
    result.reverse()
    result_final = []        
    for row in range(len(result)):
        result_final.append(cem["width"]*row + result[row])
    return set(result_final)

        
def image_without_seam(color_image, seam):
    """
    Given a color image and a set of seam indices to be removed from the image,
    return a new image that contains all the pixels from the original image
    except those corresponding to the locations in the given seam. Does not
    modify the input image.
    """
    result = { "height": color_image["height"], 
        "width": color_image["width"] - 1,
        "pixels": color_image["pixels"][:]      
    }
    for index in seam:
        result["pixels"][index] = -1
    result["pixels"] = [item for item in result["pixels"][:] if  item != -1]  
    return result   

def custom_feature(image, color, x, y, radius):
    """
    draws a circle of the given radius with defined color at the given location centred at row,col = x, y
      in 'image' if possible
      """
    
    for row in range(y - radius, y + radius):
        for  col in range(x - radius, x + radius):
            if (0 <= row < image["height"]) and (0 <= col < image["width"]):
                if (row - y) ** 2 + (col - x) ** 2 <= radius ** 2:
                    set_pixel(image, row, col, color)
    return image

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


def print_color_values(image):
    """
    Given a color image dictionary, prints a string representation of the
    image pixel values to the terminal. This function may be helpful for
    manually testing and debugging tiny image examples.

    Note that RGB values will be rounded to the nearest int.
    """
    out = f"Color image with {image['height']} rows"
    out += f" and {image['width']} columns:\n"
    space_sizes = {}
    space_vals = []

    col = 0
    for pixel in image["pixels"]:
        for color in range(3):
            val = str(round(pixel[color]))
            space_vals.append((col, color, val))
            space_sizes[(col, color)] = max(len(val), space_sizes.get((col, color), 0))
        if col == image["width"] - 1:
            col = 0
        else:
            col += 1

    for (col, color, val) in space_vals:
        space_val = val.center(space_sizes[(col, color)])
        if color == 0:
            out += f" ({space_val}"
        elif color == 1:
            out += f" {space_val} "
        else:
            out += f"{space_val})"
        if col == image["width"]-1 and color == 2:
            out += "\n"
    print(out)


def load_color_image(filename):
    """
    Loads a color image from the given file and returns a dictionary
    representing that image.

    Invoked as, for example:
       i = load_color_image('test_images/cat.png')
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img = img.convert("RGB")  # in case we were given a greyscale image
        img_data = img.getdata()
        pixels = list(img_data)
        width, height = img.size
        return {"height": height, "width": width, "pixels": pixels}


def save_color_image(image, filename, mode="PNG"):
    """
    Saves the given color image to disk or to a file-like object.  If filename
    is given as a string, the file type will be inferred from the given name.
    If filename is given as a file-like object, the file type will be
    determined by the 'mode' parameter.
    """
    # make folders if they do not exist
    directory = os.path.realpath(os.path.dirname(filename))
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    # save image in folder specified (by default the current folder)
    out = Image.new(mode="RGB", size=(image["width"], image["height"]))
    out.putdata(image["pixels"])
    if isinstance(filename, str):
        out.save(filename)
    else:
        out.save(filename, mode)
    out.close()


def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns an instance of this class
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_greyscale_image('test_images/cat.png')
    """
    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith("RGB"):
            pixels = [
                round(0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]) for p in img_data
            ]
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
    by the 'mode' parameter.
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
    #color_inverted = color_filter_from_greyscale_filter(inverted)
    #inverted_color_frog = color_inverted(load_color_image('test_images/cat.png'))
    #save_color_image(inverted_color_frog, "cat.png")
    #save_color_image(color_filter_from_greyscale_filter(make_blur_filter(9))(load_color_image('test_images/python.png')), "python.png")
    #save_color_image(color_filter_from_greyscale_filter(make_sharpen_filter(7))(load_color_image('test_images/sparrowchick.png')), "sparrowchick.png")
    #filter1 = color_filter_from_greyscale_filter(edges)
    #filter2 = color_filter_from_greyscale_filter(make_blur_filter(5))
    #filt = filter_cascade([filter1, filter1, filter2, filter1])
    #save_color_image(seam_carving((load_color_image("test_images/twocats.png")), 100), "cats.png")
    #save_color_image(custom_feature(load_color_image("test_images/twocats.png"),(255, 0, 0) ,35, 50, 20), "cats_custom.png")
    print_color_values(load_color_image("flood_input.png"))