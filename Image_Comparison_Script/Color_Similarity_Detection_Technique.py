from PIL import Image
from skimage import color
import numpy as np
import os


"""
Class for handling image comparison using Euclidean distance in the Lab color space with a tolerance threshold.
"""
class ImageCompare:
    def __init__(self, img1_path, img2_path, tolerance):
        self.img1_path = img1_path
        self.img2_path = img2_path
        self.tolerance = tolerance
        self.img1 = self.load_image(self.img1_path)
        self.img2 = self.load_image(self.img2_path)
    
    """
    Description:
        Load an image from the provided file path.
     Args:
        image_path (str): Path to the image.
     Returns:
        PIL.Image: Loaded image object.
     """
    @staticmethod
    def load_image(image_path):
        try:
            return Image.open(image_path)
        except Exception as e:
            raise ValueError(f"Error loading image '{image_path}': {str(e)}")
        
    """
    Description:
        Ensure that both images have the same size and format.
    Raises:
        ValueError: If image sizes or formats do not match.
    """   
    def validate_images(self):
        if self.img1.size != self.img2.size:
            raise ValueError("Images have different sizes.")
        if self.img1.format != self.img2.format:
            raise ValueError(f"Image formats do not match: {self.img1.format} vs {self.img2.format}")
     
    """
    Description:
        Convert an RGB image to Lab color space.
    Args:
        image (PIL.Image): The image to convert.
    Returns:
        numpy.ndarray: Image converted to Lab color space.
    """
    @staticmethod
    def convert_to_lab(image):
        img_rgb = np.array(image) / 255.0
        return color.rgb2lab(img_rgb)
    
    """
    Description:
        Compute the pixel-wise difference between two images in Lab color space.
    Args:
        img1_lab (numpy.ndarray): First image in Lab space.
        img2_lab (numpy.ndarray): Second image in Lab space.
    Returns:
        numpy.ndarray: Euclidean difference in Lab color space.
    """
    @staticmethod
    def compute_lab_difference(img1_lab, img2_lab):
        return np.sqrt(np.sum((img1_lab - img2_lab) ** 2, axis=2))
    
    """
    Description:
        Compare the two loaded images in Lab color space and return the differences.
    Returns:
        tuple: (lab_diff, num_differences, total_pixels)
    """
    def compare_images(self):
        self.validate_images()
        img1_lab = self.convert_to_lab(self.img1)
        img2_lab = self.convert_to_lab(self.img2)

        lab_diff = self.compute_lab_difference(img1_lab, img2_lab)
        mask = lab_diff > self.tolerance

        total_pixels = np.array(self.img1).size
        num_differences = np.sum(mask)
        
        return lab_diff, num_differences, total_pixels
    
    """
    Description:
        Generates and saves the images highlighting the differences.
    Args:
        img1 (PIL.Image): First image.
        img2 (PIL.Image): Second image.
        lab_diff (numpy.ndarray): Lab differences.
        tolerance (float): Tolerance threshold.
        output_dir (str): Directory to save images.
    """
    @staticmethod
    def save_difference_images(img1, img2, lab_diff, tolerance, output_dir="output"):
        os.makedirs(output_dir, exist_ok=True)
        mask = lab_diff > tolerance
        mask_expanded = np.repeat(mask[:, :, np.newaxis], 3, axis=2)

        img1_rgb = np.array(img1)
        img2_rgb = np.array(img2)

        img1_diff = np.where(mask_expanded, img1_rgb, 0)
        img2_diff = np.where(mask_expanded, img2_rgb, 0)
        combined_diff = np.where(mask_expanded, (img1_rgb + img2_rgb) // 2, 0)

        Image.fromarray(img1_diff.astype(np.uint8)).save(f"{output_dir}/lab_diff_img1.png")
        Image.fromarray(img2_diff.astype(np.uint8)).save(f"{output_dir}/lab_diff_img2.png")
        Image.fromarray(combined_diff.astype(np.uint8)).save(f"{output_dir}/lab_combined_diff.png")
    
    """
    Description:
        Generate a report of the comparison statistics.
    Args:
        num_differences (int): Number of pixels that differ.
        total_pixels (int): Total number of pixels in the image.
        tolerance (float): Tolerance threshold.
        output_file (str): File to save the report.
    """
    @staticmethod
    def generate_report(num_differences, total_pixels, tolerance, output_file="output/comparison_report.txt"):
        diff_percentage = (num_differences / total_pixels) * 100
        report = (
            f"Image Comparison Report:\n"
            f"Total Pixels: {total_pixels}\n"
            f"Pixels Differing: {num_differences}\n"
            f"Difference Percentage: {diff_percentage:.2f}%\n"
            f"Tolerance Value: {tolerance}%"
        )
        print(report)
        with open(output_file, "w") as f:
            f.write(report)