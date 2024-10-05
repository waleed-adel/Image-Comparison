#!/usr/bin/python3

from PIL import Image, ImageDraw
import numpy as np
import os

# Directory to save the test images
TEST_DATA_DIR = "test_data"
os.makedirs(TEST_DATA_DIR, exist_ok=True)

# Create a simple image
def create_image(path, color=(255, 255, 255), size=(100, 100), format="JPEG"):
    img = Image.new('RGB', size, color)
    img.save(path, format=format)
    print(f"Created {path}")

# Create an image with a small difference (e.g., a small red square)
def create_image_with_difference(path, color=(255, 0, 0), size=(100, 100)):
    img = Image.new('RGB', size, (0, 255, 0))  # green background
    draw = ImageDraw.Draw(img)
    draw.rectangle([10, 10, 20, 20], fill=color)  # small red square at (10,10)
    img.save(path)
    print(f"Created {path} with a small difference")

# Create an image with different size
def create_image_with_different_size(path, size=(150, 150)):
    img = Image.new('RGB', size, (255, 255, 255))  # white background
    img.save(path)
    print(f"Created {path} with a different size")

# Create a corrupted image file (empty file)
def create_corrupted_image(path):
    with open(path, 'w') as f:
        f.write("")  # empty file
    print(f"Created corrupted image {path}")

# Create an image with a slight tolerance-based difference
def create_image_for_tolerance_test(path,background=(0, 255, 0), size=(100, 100)):
    img = Image.new('RGB', size, background)  # green background
    img_arr = np.array(img)  # Convert image to NumPy array
    img_arr[20:30, 20:30] = (12, 255, 12)  # Change a block of pixels 10x10 (this block is under the 5% tolerance)
    img_arr[30:40, 30:40] = (25, 255, 25)  # Change a block of pixels 10x10 (this block is above 5% and below 10% tolerance)
    img = Image.fromarray(img_arr)  # Convert back to Image
    img.save(path)
    print(f"Created {path} for tolerance-based testing")

# Create a completely different image
def create_completely_different_image(path, color=(255, 0, 0), size=(100, 100)):
    img = Image.new('RGB', size, color)  # Completely red image
    img.save(path)
    print(f"Created {path} which is completely different")
    
# Create a grayscale image
def create_grayscale_image(path, intensity=255, size=(100, 100)):
    # Create a grayscale image with the specified intensity and size
    img = Image.new('L', size, color=intensity)  # 'L' mode is for grayscale (0-255)
    # Save the image to the specified path
    img.save(path)
    print(f"Created grayscale image with intensity {intensity} at {path}")


# Create images
create_image(f"{TEST_DATA_DIR}/image1.jpg", color=(0, 255, 0))  # Base image (green)
create_image(f"{TEST_DATA_DIR}/image1.png", color=(0, 255, 0), format="PNG")  # Base image (green) PNG format
create_image(f"{TEST_DATA_DIR}/image1_copy.jpg", color=(0, 255, 0))  # Identical image (copy)
create_image_with_difference(f"{TEST_DATA_DIR}/image2_small_diff.jpg")  # Small difference than image 1 (red square)
create_image_with_different_size(f"{TEST_DATA_DIR}/image4_different_size.jpg",size=(150, 150))  # Different size
create_corrupted_image(f"{TEST_DATA_DIR}/corrupted_image1.jpg")  # Corrupted image
create_image_for_tolerance_test(f"{TEST_DATA_DIR}/image2_tolerance.png")  # Image for tolerance testing
create_completely_different_image(f"{TEST_DATA_DIR}/image3_different.jpg")  # Completely different image
create_image(f"{TEST_DATA_DIR}/image2.jpg", color=(0, 128, 0))  # Another image to compare with image1
create_grayscale_image(f"{TEST_DATA_DIR}/image1_grayscale.jpg")  # grayscale image1
create_grayscale_image(f"{TEST_DATA_DIR}/image2_grayscale.jpg", intensity=250)  # grayscale image2

# Create large images for performance testing
create_image(f"{TEST_DATA_DIR}/image1_200x200.jpg", color=(0, 255, 0),size=(200, 200))  # 200x200 image1 (green)
create_image(f"{TEST_DATA_DIR}/image2_200x200.jpg", color=(1, 255, 0),size=(200, 200))  # 200x200 image2 but with slight difference(green)
create_image(f"{TEST_DATA_DIR}/image1_500x500.jpg", color=(0, 255, 0),size=(500, 500))  # 500x500 image1 (green)
create_image(f"{TEST_DATA_DIR}/image2_500x500.jpg", color=(1, 255, 0),size=(500, 500))  # 500x500 image2 but with slight difference(green)
create_image(f"{TEST_DATA_DIR}/image1_4000x4000.jpg", color=(0, 0, 255),size=(4000, 4000))  # 4000x4000 blue image1
create_image(f"{TEST_DATA_DIR}/image2_4000x4000.jpg", color=(0, 1, 255),size=(4000, 4000))  # 4000x4000 blue image2 but with slight difference

# Create an invalid file (not an image) for invalid format testing
with open(f"{TEST_DATA_DIR}/invalid_image.pdf", 'w') as f:
    f.write("%PDF-1.4\n%")  # Just some content to simulate a PDF file
print("Created invalid image invalid_image.pdf")

print("All test images created successfully!")
