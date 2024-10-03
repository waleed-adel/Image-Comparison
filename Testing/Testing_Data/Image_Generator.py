#!/usr/bin/python3

from PIL import Image
import numpy as np

# Create a new RGB image with a solid color (size: 100x100)
def create_image(color=(255, 0, 0), size=(100, 100)):
    img = Image.new("RGB", size, color)
    img.save("solid_color_image.png")
    return img

# Create an image and manipulate its pixels
def manipulate_image(img, change_color=(0, 255, 0)):
    img_arr = np.array(img)  # Convert image to NumPy array
    img_arr[20:40, 20:40] = change_color  # Change a block of pixels
    img_arr[60:80, 60:80] = change_color  # Change a block of pixels
    manipulated_img = Image.fromarray(img_arr)  # Convert back to Image
    manipulated_img.save("manipulated_image.png")
    return manipulated_img

# Test the functions
img = create_image(color=(255, 0, 0))  # Red image
manipulated_img = manipulate_image(img, change_color=(230, 15, 25))  # Add green block
