#!/usr/bin/python3

import os
import argparse
from Color_Similarity_Detection_Technique import ImageCompare  # Import the ImageCompare class

# Allowed image extensions for input validation
VALID_IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif')


"""
Description:
    Parse command-line arguments.
Returns:
    argparse.Namespace: Parsed arguments including image paths and tolerance.
"""
def parse_arguments():
   
    parser = argparse.ArgumentParser(description="Compare two image files using Lab color space.")
    parser.add_argument("--img1", type=check_image_file_format_validity, required=True, help="First image file to compare")
    parser.add_argument("--img2", type=check_image_file_format_validity, required=True, help="Second image file to compare")
    parser.add_argument("--tolerance_value", type=check_tolerance_value_validity, default=0, help="Tolerance value (0-100)")
    return parser.parse_args()

"""
Description:
    Validate the image file format and check if it exists.
Args:
    file_path (str): File path to the image.
Returns:
    str: Validated file path.
Raises:
    argparse.ArgumentTypeError: If the file does not exist or is not a valid image format.
"""
def check_image_file_format_validity(file_path):
   
    if not os.path.isfile(file_path):
        raise argparse.ArgumentTypeError(f"File '{file_path}' does not exist.")
    if not file_path.lower().endswith(VALID_IMAGE_EXTENSIONS):
        raise argparse.ArgumentTypeError(f"File '{file_path}' is not a valid image format.")
    return file_path

"""
Description:
    Validate the tolerance value (must be between 0 and 100).
Args:
    value (float): Tolerance value entered by the user.
Returns:
    float: Validated tolerance value.
Raises:
    argparse.ArgumentTypeError: If the tolerance value is not a valid number or is out of range.
"""
def check_tolerance_value_validity(value):
    
    try:
        value = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Tolerance value '{value}' is not a valid number.")
    if not (0 <= value <= 100):
        raise argparse.ArgumentTypeError(f"Tolerance value '{value}' must be between 0 and 100.")
    return value


def main():
    
    args = parse_arguments()
    comparer = ImageCompare(args.img1, args.img2, args.tolerance_value)
    
    # Output the image file paths and tolerance value
    print(f"Comparing Image 1: {args.img1}")
    print(f"Comparing Image 2: {args.img2}")
    print(f"Tolerance Value: {args.tolerance_value}%")

    # Compare the images and generate difference images
    lab_diff, num_differences, total_pixels = comparer.compare_images()
    comparer.save_difference_images(comparer.img1, comparer.img2, lab_diff, args.tolerance_value)

    # Generate and print the comparison report
    comparer.generate_report(num_differences, total_pixels, args.tolerance_value)


if __name__ == "__main__":
    main()

