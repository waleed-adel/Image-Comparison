#!/usr/bin/python3

import os
import argparse
from color_similarity_detection_technique import ImageCompare  # Import the ImageCompare class

VALID_IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif')

"""
    Description:
        Parses command-line arguments for image file paths and tolerance values.
    Returns:
        argparse.Namespace: Parsed arguments for image paths and tolerance values.
"""
def parse_arguments():
    parser = argparse.ArgumentParser(description="Compare two image files pixel by pixel using a tolerance value.")
    parser.add_argument("--img1", type=check_image_file_format_validity, required=True, help="First image file to compare")
    parser.add_argument("--img2", type=check_image_file_format_validity, required=True, help="Second image file to compare")
    parser.add_argument("--tolerance_value", type=check_tolerance_value_validity, default=0, help="Tolerance value (0-100)")
    return parser.parse_args()

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
    if not os.path.isfile(file_path):
        raise argparse.ArgumentTypeError(f"File '{file_path}' does not exist.")
    if not file_path.lower().endswith(VALID_IMAGE_EXTENSIONS):
        raise argparse.ArgumentTypeError(f"File '{file_path}' is not a valid image format.")
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
        value = float(value)
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
def main():
    args = parse_arguments()
    comparer = ImageCompare(args.img1, args.img2, args.tolerance_value)
    
    print(f"Comparing Image 1: {args.img1}")
    print(f"Comparing Image 2: {args.img2}")
    print(f"Tolerance Value: {args.tolerance_value}%")

    mask, num_differences, total_pixels = comparer.compare_images()
    comparer.save_difference_images(comparer.img1, comparer.img2, mask)
    comparer.generate_report(num_differences, total_pixels, args.tolerance_value)

if __name__ == "__main__":
    main()
