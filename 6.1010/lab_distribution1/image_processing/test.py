#!/usr/bin/env python3

import os
import pickle
import hashlib

import lab
import pytest

TEST_DIRECTORY = os.path.dirname(__file__)


def object_hash(x):
    return hashlib.sha512(pickle.dumps(x)).hexdigest()


def compare_images(result, expected):
    assert set(result.keys()) == {'height', 'width', 'pixels'}, f'Incorrect keys in dictionary'
    assert result['height'] == expected['height'], 'Heights must match'
    assert result['width'] == expected['width'], 'Widths must match'
    assert len(result['pixels']) == result['height']*result['width'], f"Incorrect number of pixels, exp_image {result['height']*result['width']}"
    num_incorrect_val = 0
    first_incorrect_val = None
    num_bad_type = 0
    first_bad_type = None
    num_bad_range = 0
    first_bad_range = None

    row, col = 0, 0
    correct_image = True
    for index, (res, exp) in enumerate(zip(result['pixels'], expected['pixels'])):
        if not isinstance(res, int):
            correct_image = False
            num_bad_type += 1
            if not first_bad_type:
                first_bad_type = f'Pixels must all be integers!'
                first_bad_type += f'\nPixel had value {res} at index {index} (row {row}, col {col}).'
        if res < 0 or res > 255:
            num_bad_range += 1
            correct_image = False
            if not first_bad_range:
                first_bad_range = f'Pixels must all be in the range from [0, 255]!'
                first_bad_range += f'\nPixel had value {res} at index {index} (row {row}, col {col}).'
        if res != exp:
            correct_image = False
            num_incorrect_val += 1
            if not first_incorrect_val:
                first_incorrect_val = f'Pixels must match'
                first_incorrect_val += f'\nPixel had value {res} but exp_image {exp} at index {index} (row {row}, col {col}).'

        if col + 1 == result["width"]:
            col = 0
            row += 1
        else:
            col += 1

    msg = "Image is correct!"
    if first_bad_type:
        msg = first_bad_type + f"\n{num_bad_type} pixel{'s'*int(num_bad_type>1)} had this problem."
    elif first_bad_range:
        msg = first_bad_range + f"\n{num_bad_range} pixel{'s'*int(num_bad_range>1)} had this problem."
    elif first_incorrect_val:
        msg = first_incorrect_val + f"\n{num_incorrect_val} pixel{'s'*int(num_incorrect_val>1)} had incorrect value{'s'*int(num_incorrect_val>1)}."

    assert correct_image, msg


def test_load():
    result_image = lab.load_greyscale_image(os.path.join(TEST_DIRECTORY, 'test_images', 'centered_pixel.png'))
    exp_image = {
        'height': 11,
        'width': 11,
        'pixels': [0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0,   0, 0, 0, 0, 0, 0],
    }
    compare_images(result_image, exp_image)


def test_inverted_1():
    input_fname = os.path.join(TEST_DIRECTORY, 'test_images', 'centered_pixel.png')
    input_image = lab.load_greyscale_image(input_fname)
    input_hash = object_hash(input_image)
    result_image = lab.inverted(input_image)
    exp_image = {
        'height': 11,
        'width': 11,
        'pixels': [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255,   0, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
                   255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    }
    compare_images(result_image, exp_image)
    assert object_hash(input_image) == input_hash, 'Be careful not to modify the original image!'

def test_inverted_2():
    inp = {"height": 1,
    "width": 4,
    "pixels": [27, 73, 146, 214]}
    inp2 = inp.copy()
    out = inp.copy()
    out["pixels"] = [228, 182, 109, 41]
    compare_images(lab.inverted(inp), out)
    assert inp == inp2, 'be careful not to modify the inputs!'

@pytest.mark.parametrize("fname", ['mushroom', 'twocats', 'chess'])
def test_inverted_images(fname):
    input_fname = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
    exp_fname = os.path.join(TEST_DIRECTORY, 'test_results', '%s_invert.png' % fname)
    input_image = lab.load_greyscale_image(input_fname)
    input_hash = object_hash(input_image)
    result_image = lab.inverted(input_image)
    exp_image = lab.load_greyscale_image(exp_fname)
    compare_images(result_image, exp_image)
    assert object_hash(input_image) == input_hash, "Be careful not to modify the original image!"


@pytest.mark.parametrize("kernsize", [1, 3, 7])
@pytest.mark.parametrize("fname", ['mushroom', 'twocats', 'chess'])
def test_blurred_images(kernsize, fname):
    input_fname = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
    exp_fname = os.path.join(TEST_DIRECTORY, 'test_results', '%s_blur_%02d.png' % (fname, kernsize))
    input_image = lab.load_greyscale_image(input_fname)
    input_hash = object_hash(input_image)
    result_image = lab.blurred(input_image, kernsize)
    exp_image = lab.load_greyscale_image(exp_fname)
    compare_images(result_image, exp_image)
    assert object_hash(input_image) == input_hash, "Be careful not to modify the original image!"

def test_blurred_black_image():
    # REPLACE THIS with your 1st test case from section 5.1
  #REPLACE THIS with your 1st test case from section 5.1
    
    inp = {
        "height": 6,
        "width": 5,
        "pixels": [0 for i in range(30)]
    }
    inp2 = inp.copy()
    compare_images(lab.blurred(inp, 3), inp)
    compare_images(lab.blurred(inp, 5), inp)
    assert inp == inp2, "Be careful not to modify the input" 
   
def test_blurred_centered_pixel():
    # REPLACE THIS with your 2nd test case from section 5.1
   
   
    # REPLACE THIS with your 2nd test case from section 5.1
    inp = lab.load_greyscale_image("test_images/centered_pixel.png")
    inp2 = inp.copy()
    result_1 = {"height": inp["height"],
    "width": inp["width"],
    "pixels": [0 for i in range(inp["height"]*inp["width"])]
    }
    result_2 = {"height": inp["height"],
    "width": inp["width"],
    "pixels": [0 for i in range(inp["height"]*inp["width"])]
    }
    
    for row in range(inp["width"]//2 - 1, inp["width"]//2 + 2):
        for col in range(inp["height"]//2 - 1, inp["height"]//2 + 2):
            result_1["pixels"][result_1["width"]*row + col] = round(255/9)
    for row in range(inp["width"]//2 - 2, inp["width"]//2 + 3):
        for col in range(inp["height"]//2 - 2, inp["height"]//2 + 3):
            result_2["pixels"][result_2["width"]*row + col] = round(255/25)
    x = lab.blurred(inp, 3)
    lab.print_greyscale_values(x)
    compare_images(x, result_1)
    compare_images(lab.blurred(inp, 5), result_2)
    assert inp == inp2, "do not modify the original image"

    

@pytest.mark.parametrize("kernsize", [1, 3, 9])
@pytest.mark.parametrize("fname", ['mushroom', 'twocats', 'chess'])
def test_sharpened_images(kernsize, fname):
    input_fname = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
    exp_fname = os.path.join(TEST_DIRECTORY, 'test_results', '%s_sharp_%02d.png' % (fname, kernsize))
    input_image = lab.load_greyscale_image(input_fname)
    input_hash = object_hash(input_image)
    result_image = lab.sharpened(input_image, kernsize)
    exp_image = lab.load_greyscale_image(exp_fname)
    compare_images(result_image, exp_image)
    assert object_hash(input_image) == input_hash, "Be careful not to modify the original image!"


@pytest.mark.parametrize("fname", ['mushroom', 'twocats', 'chess'])
def test_edges_images(fname):
    input_fname = os.path.join(TEST_DIRECTORY, 'test_images', '%s.png' % fname)
    exp_fname = os.path.join(TEST_DIRECTORY, 'test_results', '%s_edges.png' % fname)
    input_image = lab.load_greyscale_image(input_fname)
    input_hash = object_hash(input_image)
    result_image = lab.edges(input_image)
    exp_image = lab.load_greyscale_image(exp_fname)
    compare_images(result_image, exp_image)
    assert object_hash(input_image) == input_hash, "Be careful not to modify the original image!"

def test_edges_centered_pixel():
    # REPLACE THIS with your test case from section 6
    
    inp = lab.load_greyscale_image("test_images/centered_pixel.png")
    inp2 = inp.copy()
    result= {"height": inp["height"],
    "width": inp["width"],
    "pixels": [0 for i in range(inp["height"]*inp["width"])]
    }
    
    for row in range(inp["width"]//2 - 1, inp["width"]//2 + 2):
        for col in range(inp["height"]//2 - 1, inp["height"]//2 + 2):
            result["pixels"][result["width"]*row + col] = 255
    result["pixels"][result["width"]*(result["height"]//2) + result["width"]//2 ] = 0
    compare_images(lab.edges(inp), result)
    assert inp == inp2, "do not modify the original image"
