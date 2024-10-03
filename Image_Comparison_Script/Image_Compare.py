#!/usr/bin/python3

from PIL import Image, ImageChops
import numpy as np
import os
import argparse

# Allowed image extensions for input validation
VALID_IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif')

"""
    Description:
        Check if the provided file path is valid and has a valid image extension.

    Args:
        file_path (str): The file path of the image to be validated.

    Returns:
        str: Validated file path.

    Raises:
        argparse.ArgumentTypeError: If the file does not exist or has an invalid extension.
"""
def checkImageFileFormatValidity(file_path):
    if not os.path.isfile(file_path):
        raise argparse.ArgumentTypeError(f"File '{file_path}' does not exist.")
    if not file_path.lower().endswith(VALID_IMAGE_EXTENSIONS):
        raise argparse.ArgumentTypeError(f"File '{file_path}' is not a valid image format.")
    return file_path

"""
    Description:
        Validate the tolerance value provided by the user.

    Args:
        value (float): The tolerance value as a percentage (0-100).

    Returns:
        float: Validated tolerance value.

    Raises:
        argparse.ArgumentTypeError: If the value is not a valid number or falls outside the 0-100 range.
"""
def checkToleranceValueValidity(value):
    try:
        value = float(value)  # Allow floating-point percentage values
    except ValueError:
        raise argparse.ArgumentTypeError(f"Tolerance value '{value}' is not a valid number.")
    if value < 0:
        raise argparse.ArgumentTypeError(f"Tolerance value '{value}' must be non-negative.")
    if value > 100:
        raise argparse.ArgumentTypeError(f"Tolerance value '{value}' must not exceed 100.")
    return value

"""
    Description:
        Parse command-line arguments for image file paths and tolerance value.

    Returns:
        argparse.Namespace: The parsed command-line arguments containing image paths and tolerance value.
"""
def parseArguments():
    parser = argparse.ArgumentParser(description="Compare two image files")
    parser.add_argument("--img1", type=checkImageFileFormatValidity, required=True, help="First image file to compare")
    parser.add_argument("--img2", type=checkImageFileFormatValidity, required=True, help="Second image file to compare")
    parser.add_argument("--tolerance_value", type=checkToleranceValueValidity, default=0, help="Pixels Tolerance Value")
    return parser.parse_args()

"""
    Description:
        Compare if both images have the same format (e.g., both should be JPG or PNG).

    Args:
        image1 (PIL.Image): The first image to compare.
        image2 (PIL.Image): The second image to compare.

    Returns:
        bool: True if both images have the same format.

    Raises:
        ValueError: If the images have different formats.
"""
def compareImagesFormat(image1, image2):
    if image1.format != image2.format:
        raise ValueError(f"Image formats do not match: {image1.format} vs {image2.format}")
    return True

"""
    Description:
        Save three images showing differences:
        1. Only differences from the first image.
        2. Only differences from the second image.
        3. A combined image of both differences.

    Args:
        img1_arr (numpy.ndarray): Array representing the first image's pixels.
        img2_arr (numpy.ndarray): Array representing the second image's pixels.
        tolerance_value (float): The tolerance threshold for differences.
        output_dir (str): The directory where the output images will be saved. Default is "output".
"""
def saveDiffImages(img1_arr, img2_arr, tolerance_value, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)  # Create output directory if it doesn't exist

    # Differences only in img1
    diff_img1 = np.where(np.abs(img1_arr - img2_arr) > tolerance_value, img1_arr, 0)
    Image.fromarray(diff_img1.astype(np.uint8)).save(f"{output_dir}/diff_img1.png")

    # Differences only in img2
    diff_img2 = np.where(np.abs(img2_arr - img1_arr) > tolerance_value, img2_arr, 0)
    Image.fromarray(diff_img2.astype(np.uint8)).save(f"{output_dir}/diff_img2.png")

    # Combined differences (overlay of both images' differences)
    combined_diff = np.where(np.abs(img1_arr - img2_arr) > tolerance_value, img1_arr, img2_arr)
    Image.fromarray(combined_diff.astype(np.uint8)).save(f"{output_dir}/combined_diff.png")

"""
    Description:
        Compare two images based on pixel differences, applying a tolerance percentage.

    Args:
        image1 (str): The file path of the first image.
        image2 (str): The file path of the second image.
        tolerance_percentage (float): The percentage tolerance for pixel comparison.

    Returns:
        tuple: (bool, int, int) where the first value indicates if the images are similar,
               the second is the number of differing pixels, and the third is the total number of pixels.

    Raises:
        ValueError: If the images do not have the same size.
"""
def compareImagesToleranceBased(image1, image2, tolerance_percentage):
    # Open both images
    img1 = Image.open(image1)
    img2 = Image.open(image2)

    # Ensure both images have the same size and format
    if img1.size != img2.size:
        raise ValueError("Images have different sizes.")
    compareImagesFormat(img1, img2)

    # Calculate maximum possible pixel value (255 for an 8-bit image)
    max_pixel_value = 255
    tolerance_value = (tolerance_percentage / 100) * max_pixel_value

    # Use ImageChops to compute the pixel-wise difference
    diff_image = ImageChops.difference(img1, img2)
    diff_arr = np.array(diff_image)
    print(diff_arr[21,21])

    num_differences = np.sum(diff_arr > tolerance_value)  # Count pixels where the difference exceeds the tolerance

    if num_differences == 0:
        print("Images are identical within the tolerance.")
    else:
        print(f"Images differ in {num_differences} pixels outside the tolerance.")

    # Save difference images (for input1, input2, and combined differences)
    saveDiffImages(np.array(img1), np.array(img2), tolerance_value)

    return num_differences == 0, num_differences, np.array(img1).size


"""
    Description:
        Generate a report with statistics on the image comparison.
        The report includes total pixels, differing pixels, percentage of differing pixels, and the tolerance value.

    Args:
        num_differences (int): The number of differing pixels between the two images.
        total_pixels (int): The total number of pixels in one image.
        tolerance_value (float): The tolerance percentage used in the comparison.
"""
def generateStatReport(num_differences, total_pixels, tolerance_value):
    diff_percentage = (num_differences / total_pixels) * 100
    report = (
        f"Image Comparison Report:\n"
        f"Total Pixels: {total_pixels}\n"
        f"Pixels Differing: {num_differences}\n"
        f"Difference Percentage: {diff_percentage:.2f}%\n"
        f"Tolerance Value: {tolerance_value}%"
    )
    print(report)
    # Save report to file
    with open("output/comparison_report.txt", "w") as f:
        f.write(report)


"""
    Description:
        Main function to handle argument parsing, image comparison, and report generation.

    Args:
        None

    Returns:
        None
"""
def main():
    # Parse arguments
    args = parseArguments()

    # Output the image file paths and tolerance value
    print(f"Comparing Image 1: {args.img1}")
    print(f"Comparing Image 2: {args.img2}")
    print(f"Tolerance Value: {args.tolerance_value}")

    # Compare the images and get results
    result, num_differences, total_pixels = compareImagesToleranceBased(args.img1, args.img2, args.tolerance_value)

    if result:
        print("The images are the same.")
    else:
        print("The images are different.")

    # Generate the statistical report
    generateStatReport(num_differences, total_pixels, args.tolerance_value)

# Entry point of the script
if __name__ == "__main__":
    main()


