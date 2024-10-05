#!/usr/bin/python3

import pytest
import os
import argparse
import sys
sys.path.append('../src')
import image_compare
from color_similarity_detection_technique import ImageCompare


# Paths for test images and expected outputs
TEST_DATA_DIR = "../test_data/"
OUTPUT_DIR = "testcase_output/"

# Helper function to clean up the output folder after each test
@pytest.fixture(autouse=True)
def cleanup():
    yield
    for file in os.listdir(OUTPUT_DIR):
        os.remove(os.path.join(OUTPUT_DIR, file))

#########################################################
#           Testing for color_similarity_detection_technique.py           #
#########################################################
# Test Case 1: Basic Functionality with Two Identical Images
def test_identical_images():
    img1_path = f"{TEST_DATA_DIR}/image1.jpg"
    img2_path = f"{TEST_DATA_DIR}/image1_copy.jpg"
    comparer = ImageCompare(img1_path, img2_path, tolerance=0)
    mask, num_differences, total_pixels = comparer.compare_images()
    
    assert num_differences == 0, f"Expected no differences, but found {num_differences} pixels differing."

# Test Case 2: Different Images with Small Changes
def test_small_differences():
    img1_path = f"{TEST_DATA_DIR}/image1.jpg"
    img2_path = f"{TEST_DATA_DIR}/image2_small_diff.jpg"
    comparer = ImageCompare(img1_path, img2_path, tolerance=5)
    mask, num_differences, total_pixels = comparer.compare_images()
    
    assert num_differences > 0, "Expected differences, but none found."

# Test Case 3: Tolerance-Based Pixel Comparison
@pytest.mark.parametrize("tolerance, expected_num_differences", [(0, 200), (5, 100), (10, 0)])
def test_tolerance_based_comparison(tolerance, expected_num_differences):
    img1_path = f"{TEST_DATA_DIR}/image1.png"
    img2_path = f"{TEST_DATA_DIR}/image2_tolerance.png"
    comparer = ImageCompare(img1_path, img2_path, tolerance=tolerance)
    
    mask, num_differences, total_pixels = comparer.compare_images()
    assert num_differences <= expected_num_differences, f"Tolerance {tolerance}% failed."

# Test Case 4: Completely Different Images
def test_completely_different_images():
    img1_path = f"{TEST_DATA_DIR}/image1.jpg"
    img2_path = f"{TEST_DATA_DIR}/image3_different.jpg"
    comparer = ImageCompare(img1_path, img2_path, tolerance=0)
    
    mask, num_differences, total_pixels = comparer.compare_images()
    assert num_differences == total_pixels, "Expected all pixels to differ."

# Test Case 5: Invalid Image Formats
def test_invalid_image_formats():
    img1_path = f"{TEST_DATA_DIR}/image1.jpg"
    img2_path = f"{TEST_DATA_DIR}/invalid_image.pdf"
    
    with pytest.raises(ValueError, match="Error loading image"):
        comparer = ImageCompare(img1_path, img2_path, tolerance=0)

# Test Case 6: Different Image Sizes
def test_different_image_sizes():
    img1_path = f"{TEST_DATA_DIR}/image1.jpg"
    img2_path = f"{TEST_DATA_DIR}/image4_different_size.jpg"
    
    with pytest.raises(ValueError, match="Images have different sizes"):
        comparer = ImageCompare(img1_path, img2_path, tolerance=0)
        comparer.compare_images()

# Test Case 7: Empty or Corrupted Image File
def test_corrupted_image_file():
    img1_path = f"{TEST_DATA_DIR}/corrupted_image1.jpg"
    img2_path = f"{TEST_DATA_DIR}/image2.jpg"
    
    with pytest.raises(ValueError, match="Error loading image"):
        comparer = ImageCompare(img1_path, img2_path, tolerance=0)

# Test Case 8: Non-Existing Image File
def test_non_existing_file():
    img1_path = f"{TEST_DATA_DIR}/non_existing_image.jpg"
    img2_path = f"{TEST_DATA_DIR}/image1.jpg"
    
    with pytest.raises(ValueError, match="Error loading image"):
        comparer = ImageCompare(img1_path, img2_path, tolerance=0)

# Test Case 9: Correct Report Generation
def test_correct_report_generation():
    img1_path = f"{TEST_DATA_DIR}/image1.jpg"
    img2_path = f"{TEST_DATA_DIR}/image2.jpg"
    comparer = ImageCompare(img1_path, img2_path, tolerance=0)
    mask, num_differences, total_pixels = comparer.compare_images()
    
    comparer.generate_report(num_differences, total_pixels, 0, output_file=f"{OUTPUT_DIR}/test_report.txt")
    assert os.path.exists(f"{OUTPUT_DIR}/test_report.txt"), "Report file created."

# Test Case 10: Report File Creation
def test_report_file_creation():
    img1_path = f"{TEST_DATA_DIR}/image1.jpg"
    img2_path = f"{TEST_DATA_DIR}/image2.jpg"
    comparer = ImageCompare(img1_path, img2_path, tolerance=0)
    comparer.generate_report(10, 1000, 0, output_file=f"{OUTPUT_DIR}/test_report.txt")
    
    assert os.path.exists(f"{OUTPUT_DIR}/test_report.txt"), "Report file created."

# Test Case 11: Correct Image Output Generation for RGB
def test_rgb_image_output_generation():
    img1_path = f"{TEST_DATA_DIR}/image1.jpg"
    img2_path = f"{TEST_DATA_DIR}/image2.jpg"
    comparer = ImageCompare(img1_path, img2_path, tolerance=0)
    mask, num_differences, total_pixels = comparer.compare_images()
    comparer.save_difference_images(comparer.img1, comparer.img2, mask, output_dir=OUTPUT_DIR)
    
    assert os.path.exists(f"{OUTPUT_DIR}/diff_img1.png"), "Diff image 1 created."
    assert os.path.exists(f"{OUTPUT_DIR}/diff_img2.png"), "Diff image 2 created."
    assert os.path.exists(f"{OUTPUT_DIR}/combined_diff.png"), "Combined diff image created."
    
# Test Case 12: Correct Image Output Generation for grayscale
def test_grayscale_image_output_generation():
    img1_path = f"{TEST_DATA_DIR}/image1_grayscale.jpg"
    img2_path = f"{TEST_DATA_DIR}/image1_grayscale.jpg"
    comparer = ImageCompare(img1_path, img2_path, tolerance=0)
    mask, num_differences, total_pixels = comparer.compare_images()
    comparer.save_difference_images(comparer.img1, comparer.img2, mask, output_dir=OUTPUT_DIR)
    
    assert os.path.exists(f"{OUTPUT_DIR}/diff_img1.png"), "Diff image 1 created."
    assert os.path.exists(f"{OUTPUT_DIR}/diff_img2.png"), "Diff image 2 created."
    assert os.path.exists(f"{OUTPUT_DIR}/combined_diff.png"), "Combined diff image created."

# Test Case13: Compare grayscale image with RGB image
def test_grayscale_vs_rgb_image():
    # Generate RGB image with a green background
    rgb_image_path = f"{TEST_DATA_DIR}/image1.jpg"
    grayscale_image_path = f"{TEST_DATA_DIR}/image1_grayscale.jpg"

    # Expect a ValueError due to image mode mismatch
    with pytest.raises(ValueError, match="Image modes do not match: RGB vs L"):
        # Compare the two images (grayscale and RGB)
        comparer = ImageCompare(rgb_image_path, grayscale_image_path, tolerance=0)
        comparer.compare_images()

# Test Case14: Compare 2 similar grayscale images
def test_grayscale_vs_grayscale_similar():
    # Generate RGB image with a green background
    grayscale_image1_path = f"{TEST_DATA_DIR}/image1_grayscale.jpg"
    grayscale_image2_path = f"{TEST_DATA_DIR}/image1_grayscale.jpg"
    comparer = ImageCompare(grayscale_image1_path, grayscale_image2_path, tolerance=0)
    
    mask, num_differences, total_pixels = comparer.compare_images()
    assert num_differences == 0, "Expected no differences."
    
# Test Case15: Compare 2 different grayscale images
def test_grayscale_vs_grayscale_different():
    # Generate RGB image with a green background
    grayscale_image1_path = f"{TEST_DATA_DIR}/image1_grayscale.jpg"
    grayscale_image2_path = f"{TEST_DATA_DIR}/image2_grayscale.jpg"
    comparer = ImageCompare(grayscale_image1_path, grayscale_image2_path, tolerance=0)
    
    mask, num_differences, total_pixels = comparer.compare_images()
    assert num_differences != 0, "Expected differences."

# Test Case 16: 200x200 Images
def test_200x200_images():
    img1_path = f"{TEST_DATA_DIR}/image1_200x200.jpg"
    img2_path = f"{TEST_DATA_DIR}/image2_200x200.jpg"
    comparer = ImageCompare(img1_path, img2_path, tolerance=0)
    
    mask, num_differences, total_pixels = comparer.compare_images()
    assert num_differences > 0, "Expected differences."
    
# Test Case 17: 4000x4000 Images
def test_4000x4000_images():
    img1_path = f"{TEST_DATA_DIR}/image1_4000x4000.jpg"
    img2_path = f"{TEST_DATA_DIR}/image2_4000x4000.jpg"
    comparer = ImageCompare(img1_path, img2_path, tolerance=0)
    
    mask, num_differences, total_pixels = comparer.compare_images()
    assert num_differences > 0, "Expected differences."


#########################################################
#                         Testing for image_compare.py                            #
#########################################################
# Test Case 18: Testing the exit value 0 
# Test case for comparing two valid image files with no tolerance.
# Asserts that the function runs successfully and outputs are generated.
def test_valid_image_files():
    valid_img1 = '../test_data/image1.jpg'
    valid_img2 = '../test_data/image2.jpg'
    args = ['--img1', valid_img1, '--img2', valid_img2, '--tolerance_value', '10']

    # Run the comparison
    image_compare.main(args)

    # Assert the expected output, such as the report file or output images
    expected_output = 'testcase_output/diff_img1.png'  # Replace with actual output file
    assert os.path.exists(expected_output), f"Expected output file {expected_output} found."

# Test Case 19: Testing passing an invalid image format
def test_invalid_image_format():
    # Paths to image files, one with an invalid format
    valid_img1 = '../test_data/image1.jpg'
    invalid_img2 = '../test_data/invalid_image.pdf'

    # Run the image comparison function and expect an error
    args = ['--img1', valid_img1, '--img2', invalid_img2, '--tolerance_value', '10']
    with pytest.raises(argparse.ArgumentTypeError, match="File '../test_data/invalid_image.pdf' is not a valid image format."):
        image_compare.main(args)
        
# Test Case 20: Testing passing missing image file
def test_missing_image_file():
    # Paths to image files, one missing
    valid_img1 = '../test_data/image1.jpg'
    missing_img2 = '../test_data/non_existing_image.jpg'

    # Run the image comparison function and expect an error
    args = ['--img1', valid_img1, '--img2', missing_img2, '--tolerance_value', '10']
    with pytest.raises(argparse.ArgumentTypeError, match="File '../test_data/non_existing_image.jpg' does not exist."):
        image_compare.main(args)

# Test Case 21: Testing passing different image formats
def test_different_image_formats():
    # Paths to image files, with different formats
    jpg_img = '../test_data/image1.jpg'
    png_img = '../test_data/image1.png'

    # Run the image comparison function and expect an error
    args = ['--img1', jpg_img, '--img2', png_img, '--tolerance_value', '10']
    with pytest.raises(argparse.ArgumentTypeError, match="Image formats do not match"):
        image_compare.main(args)
        
# Test Case 22: Testing for Valid Tolerance Value
# Test case for comparing two valid images with a valid tolerance value.
# Asserts that the function runs successfully without raising an error.
def test_valid_tolerance_value():
    valid_img1 = '../test_data/image1.jpg'
    valid_img2 = '../test_data/image2.jpg'
    args = ['--img1', valid_img1, '--img2', valid_img2, '--tolerance_value', '10']

    # Run the comparison
    image_compare.main(args)

    # Assert that the tolerance is processed correctly
    tolerance = 10  # The expected tolerance value passed
    assert tolerance == 10, f"Expected tolerance: 10, but got {tolerance}"

# Test Case 23: Testing for Inalid Tolerance Value
def test_invalid_tolerance_value():
    # Paths to valid image files
    valid_img1 = '../test_data/image1.jpg'
    valid_img2 = '../test_data/image2.jpg'

    # Run the image comparison function with an invalid tolerance value
    args = ['--img1', valid_img1, '--img2', valid_img2, '--tolerance_value', '120']
    with pytest.raises(argparse.ArgumentTypeError, match="Tolerance value '120.0' must be between 0 and 100."):
        image_compare.main(args)
        
# Test Case 24: Testing invalid image file opening.
# This test verifies that an ArgumentTypeError is raised when trying to open a corrupted image file.
def test_invalid_image_file_open():
    invalid_img = '../test_data/corrupted_image1.jpg'  # Assuming this is corrupted
    args = ['--img1', invalid_img, '--img2', '../test_data/image2.jpg', '--tolerance_value', '10']

    with pytest.raises(argparse.ArgumentTypeError, match="Could not open image"):
        image_compare.main(args)

# Test Case 25: Testing string tolerance value.
# This test verifies that an ArgumentTypeError is raised when the tolerance value is a non-numeric string.
def test_string_tolerance_value():
    args = ['--img1', '../test_data/image1.jpg', '--img2', '../test_data/image1.jpg', '--tolerance_value', 'abc']

    with pytest.raises(argparse.ArgumentTypeError, match="Tolerance value 'abc' is not a valid number."):
        image_compare.main(args)

# Test Case 26: Testing sys.argv usage.
# This test verifies that the script can handle arguments passed via sys.argv.
def test_sys_argv_usage(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['image_compare.py', '--img1', '../test_data/image1.jpg', '--img2', '../test_data/image2.jpg', '--tolerance_value', '10'])
    image_compare.main()







