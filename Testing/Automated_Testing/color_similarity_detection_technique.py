from PIL import Image, ImageChops
import numpy as np
import os

"""
Class for handling image comparison using pixel-by-pixel comparison with a tolerance threshold.
"""
class ImageCompare:
    """
    Description:
        Initializes the ImageCompare class with image paths and a tolerance value.
    Args:
        img1_path (str): Path to the first image.
        img2_path (str): Path to the second image.
        tolerance (float): Tolerance percentage for pixel comparison.
    """
    def __init__(self, img1_path, img2_path, tolerance):
        self.img1_path = img1_path
        self.img2_path = img2_path
        self.tolerance = tolerance
        self.img1 = self.load_image(self.img1_path)
        self.img2 = self.load_image(self.img2_path)
    
    """
    Description:
        Loads an image from the given file path.
    Args:
        image_path (str): The path to the image file.
    Returns:
        PIL.Image: The loaded image.
    Raises:
        ValueError: If the image cannot be loaded.
    """
    @staticmethod
    def load_image(image_path):
        try:
            return Image.open(image_path)
        except Exception as e:
            raise ValueError(f"Error loading image '{image_path}': {str(e)}")
        
    """
    Description:
        Validates that the two images are compatible for comparison (same size and mode).
    Raises:
        ValueError: If the images have different sizes or modes.
    """
    def validate_images(self):
        if self.img1.size != self.img2.size:
            raise ValueError("Images have different sizes.")
        if self.img1.mode != self.img2.mode:
            raise ValueError(f"Image modes do not match: {self.img1.mode} vs {self.img2.mode}")

    """
    Description:
        Compares the two loaded images pixel by pixel, using the given tolerance value.
    Returns:
        tuple: A tuple containing a mask of the differences, the number of differing pixels,
               and the total number of pixels.
    """
    def compare_images(self):
        self.validate_images()
        
        # Calculate pixel-wise difference using ImageChops.difference()
        diff_image = ImageChops.difference(self.img1, self.img2)
    
        # Convert the difference image to a NumPy array
        diff_array = np.array(diff_image)
        
        #  Calculate tolerance value from the tolerance percentage
        tolerance_value = (self.tolerance / 100) * 255
        
        # For RGB images, the difference is in 3 channels, so we apply tolerance across all channels
        if self.img1.mode == "RGB":
            # Apply the tolerance threshold: mask the pixels where any channel exceeds the tolerance
            # Axis = -1  refers to the last axis, which in the case of an RGB image is the color channels (R, G, B)
            # This operation checks for each pixel if any of the three color channels (R, G, or B) have a difference greater than the tolerance
            mask = np.any(diff_array > tolerance_value, axis=-1)
        else:
            # For grayscale images, the difference is just 1 channel, so apply the threshold directly
            mask = diff_array > tolerance_value
    
        # Calculate the number of differing pixels and the total number of pixels
        total_pixels = np.prod(self.img1.size)
        num_differences = np.sum(mask)
    
        return mask, num_differences, total_pixels
    
    """
    Description:
        Saves the difference images that highlight the differing pixels between the two images.
        - img1_diff: Shows the original pixel values from img1 where the pixels differ from img2.
        - img2_diff: Shows the original pixel values from img2 where the pixels differ from img1.
        - combined_diff: Shows the absolute difference between img1 and img2.
    Args:
        img1 (PIL.Image): The first image.
        img2 (PIL.Image): The second image.
        mask (numpy.ndarray): A boolean mask indicating the pixels that differ.
        output_dir (str): The directory to save the output difference images.
    """
    @staticmethod
    def save_difference_images(img1, img2, mask, output_dir="output"):
        os.makedirs(output_dir, exist_ok=True)

        # Convert images to RGB mode if they are not already in RGB
        if img1.mode != 'RGB':
            img1 = img1.convert('RGB')
        if img2.mode != 'RGB':
            img2 = img2.convert('RGB')

        # Convert the images to numpy arrays for manipulation
        img1_rgb = np.array(img1)
        img2_rgb = np.array(img2)

        # Create masked images for displaying the differences
        img1_diff = np.zeros_like(img1_rgb)  # Initialize with black (or background color)
        img2_diff = np.zeros_like(img2_rgb)  # Initialize with black (or background color)

        # Only keep the differing pixels with their original values in each image
        img1_diff[mask] = img1_rgb[mask]  # Retain original pixels from img1 where differences occur
        img2_diff[mask] = img2_rgb[mask]  # Retain original pixels from img2 where differences occur

        # Combine the 2 image differences
        compined_layout_array = np.add(img1_diff, img2_diff)
        
        # Save the images
        Image.fromarray(img1_diff.astype(np.uint8)).save(f"{output_dir}/diff_img1.png")
        Image.fromarray(img2_diff.astype(np.uint8)).save(f"{output_dir}/diff_img2.png")
        Image.fromarray(compined_layout_array.astype(np.uint8)).save(f"{output_dir}/combined_diff.png")

    """
    Description:
        Generates a text report summarizing the comparison results.
    Args:
        num_differences (int): The number of differing pixels.
        total_pixels (int): The total number of pixels in the images.
        tolerance (float): The tolerance percentage used in the comparison.
        output_file (str): The path to save the report file.
    """
    @staticmethod
    def generate_report(num_differences, total_pixels, tolerance, output_file="output/comparison_report.txt"):
        diff_percentage = (num_differences / total_pixels) * 100
        Similar = "" if num_differences == 0 else "not"  # Check if the images are identical
    
        # Prepare the report string
        report = (
            f"Image Comparison Report:\n"
            f"The Images are {Similar} Similar\n"
            f"Total Pixels: {total_pixels}\n"
            f"Pixels Differing: {num_differences}\n"
            f"Difference Percentage: {diff_percentage:.2f}%\n"
            f"Tolerance Value: {tolerance}%"
        )
        
        # Print to console
        print(report)
    
        # Save to file
        with open(output_file, "w") as f:
            f.write(report)
