#!/usr/bin/python3

import os
import sys
import argparse
from PIL import Image
from color_similarity_detection_technique import ImageCompare  # Import the ImageCompare class

VALID_IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif')

"""
    Description:
        Parses command-line arguments for image file paths and tolerance values.
    Returns:
        argparse.Namespace: Parsed arguments for image paths and tolerance values.
"""
def parse_arguments(args=None):
    parser = argparse.ArgumentParser(description="Compare two image files pixel by pixel using a tolerance value.")
    parser.add_argument("--img1", required=True, help="First image file to compare")
    parser.add_argument("--img2", required=True, help="Second image file to compare")
    parser.add_argument("--tolerance_value", default=0, help="Tolerance value (0-100)")
    return parser.parse_args(args)

"""
    Description:
        Validates that the provided file path exists and has a valid image extension.
    Args:
        file_path (str): The file path to validate.
    Returns:
        str: The validated file path.
    Raises:
        argparse.ArgumentTypeError: If the file does not exist or the format is invalid.
"""
def check_image_file_format_validity(file_path):
    # Check if the file exists
    if not os.path.isfile(file_path):
        raise argparse.ArgumentTypeError(f"File '{file_path}' does not exist.")
    
    # Check if the file has a valid image extension
    if not file_path.lower().endswith(VALID_IMAGE_EXTENSIONS):
        raise argparse.ArgumentTypeError(f"File '{file_path}' is not a valid image format.")
    
    # Open the image to check if it's a valid image
    try:
        with Image.open(file_path) as img:
            img_format = img.format  # This can be stored or used if needed
    except Exception as e:
        raise argparse.ArgumentTypeError(f"Could not open image '{file_path}'. Error: {e}")

    # Return only the file path (not a tuple) for further processing
    return file_path
   

"""
    Description:
        Validates that the tolerance value is a valid float between 0 and 100.
    Args:
        value (str): The tolerance value provided as a string.
    Returns:
        float: The validated tolerance value.
    Raises:
        argparse.ArgumentTypeError: If the value is not a float or out of bounds (0-100).
"""
def check_tolerance_value_validity(value):
    try:
        value = float(value)  # Convert the tolerance value to float
    except ValueError:
        raise argparse.ArgumentTypeError(f"Tolerance value '{value}' is not a valid number.")
    if not (0 <= value <= 100):
        raise argparse.ArgumentTypeError(f"Tolerance value '{value}' must be between 0 and 100.")
    return value 

"""
    Description:
        Main function that handles the image comparison process using the parsed arguments.
    - Loads the images.
    - Compares the images pixel by pixel.
    - Generates difference images and a report.
"""
def main(args=None):
    if args is None:
        args = sys.argv[1:]  # Take arguments from sys.argv if no args are passed
    parsed_args = parse_arguments(args)
    
    # Validate the image paths (now returns only the paths, not a tuple)
    img1_path = check_image_file_format_validity(parsed_args.img1)
    img2_path = check_image_file_format_validity(parsed_args.img2)

    # Open images to check formats
    with Image.open(img1_path) as img1, Image.open(img2_path) as img2:
        img1_format = img1.format
        img2_format = img2.format
    
    # Check if the two image formats are the same
    if img1_format != img2_format:
        raise argparse.ArgumentTypeError(f"Image formats do not match: '{img1_format}' vs '{img2_format}'")
     
    # Check on tolerance value
    parsed_args.tolerance_value = check_tolerance_value_validity(parsed_args.tolerance_value)
    
    comparer = ImageCompare(parsed_args.img1, parsed_args.img2, parsed_args.tolerance_value)
    
    print(f"Comparing Image 1: {parsed_args.img1}")
    print(f"Comparing Image 2: {parsed_args.img2}")
    print(f"Tolerance Value: {parsed_args.tolerance_value}%")

    mask, num_differences, total_pixels = comparer.compare_images()
    comparer.save_difference_images(comparer.img1, comparer.img2, mask)
    comparer.generate_report(num_differences, total_pixels, parsed_args.tolerance_value)

if __name__ == "__main__":
    main()
