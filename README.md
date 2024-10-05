
# Image Comparison Script

This Python script compares two images by evaluating pixel-by-pixel differences with a user-defined tolerance level. It supports both grayscale and RGB images and allows for the generation of images showing differences, as well as a detailed statistical report.

## Features
- Compares two images of the same size and format.
- Applies tolerance-based comparison to account for minor pixel differences.
- Generates three images: 
  - Differences in the first image.
  - Differences in the second image.
  - Combined differences from both images.
- Provides a statistical report showing the number of differing pixels and the percentage of differences.
  
## Requirements

Before running the script, you need to install the following Python dependencies:

- `Pillow`
- `NumPy`
- `scikit-image`

You can install the dependencies using `pip`:

```bash
pip install pillow numpy scikit-image
```

### Command Line Arguments:

The script accepts two image files as input and a tolerance value (in percentage). You can use the following command to run the script:

```bash
python Image_Compare.py --img1 <path_to_image1> --img2 <path_to_image2> --tolerance_value <tolerance_percentage>
```

- `--img1`: Path to the first image file.
- `--img2`: Path to the second image file.
- `--tolerance_value`: Tolerance percentage (0-100) to allow pixel differences between images. Default is `0`. A lower tolerance detects smaller differences between images, while a higher tolerance allows for greater pixel variations before marking them as different.


### Example:

```bash
python Image_Compare.py --img1 image1.png --img2 image2.png --tolerance_value 5
```

This command compares `image1.png` and `image2.png` with a tolerance level of 5%, meaning that pixel differences within 5% of the maximum pixel value (255 for 8-bit images) will be ignored.

### Output:

1. **Difference Images**: The script saves three images in the `output/` directory:
   - `lab_diff_img1.png`: Pixels different only in the first image.
   - `lab_diff_img2.png`: Pixels different only in the second image.
   - `lab_combined_diff.png`: A combined image showing differences in both images.

2. **Statistical Report**: A `comparison_report.txt` file is generated in the `output/` directory, containing:
   - Total number of pixels.
   - Number of differing pixels.
   - Percentage of differing pixels.
   - Tolerance value used in the comparison.

## How the Script Works

1. **Image Loading and Validation**:
   - The script loads two images and ensures they have the same size and format.
   
2. **Tolerance-Based Pixel Comparison**:
   - Pixel differences are calculated and compared to a tolerance value.
   - If the difference between two pixels exceeds the tolerance, those pixels are considered different.

3. **Generating Difference Images**:
   - The script generates three images showing where the two input images differ.
   
4. **Generating Report**:
   - The report includes the total number of pixels, the number of differing pixels, the percentage of different pixels, and the tolerance level.


## Algorithm: Image Comparison with Tolerance-Based Pixel Evaluation
The image comparison algorithm implemented in this project performs pixel-by-pixel evaluation of two images, allowing for a user-defined tolerance level to account for minor differences. 
The core logic of the comparison is encapsulated in the ImageCompare class and works as follows:

### 1. **Image Loading and Validation**:
- The algorithm first loads two images using the Python Imaging Library (PIL).
- It validates that the images have the same size and mode (e.g., RGB, Grayscale). If the sizes or modes differ, the comparison process halts with an error.

### 2. **Pixel-by-Pixel Comparison**:
- The algorithm computes the absolute difference between the two images using ImageChops.difference(). This method subtracts pixel values from one image from the corresponding pixels in the other image.
- The result is a new image where each pixel represents the difference in intensity between the corresponding pixels in the input images.

### 3. **Tolerance Application**:
- A tolerance value (0-100%) is provided by the user to define how much of a pixel difference is acceptable before considering it a difference.
- For each pixel, the algorithm checks if the difference exceeds the tolerance threshold:
  - RGB Images: Each pixel contains three color channels (Red, Green, Blue). The algorithm evaluates all three channels and flags a pixel as different if any channel exceeds the tolerance.
  - Grayscale Images: Each pixel is a single value, and the algorithm checks whether the intensity difference exceeds the tolerance

### 4. **Difference Mask Generation**:
- A mask is generated that highlights the pixels where differences were detected. This mask is a boolean array where True indicates a differing pixel.
- The algorithm counts the number of differing pixels and calculates the total number of pixels, as well as the percentage of pixels that differ.

### 5. **Output Generation**:
- The algorithm saves three difference images:
  - Image 1 Differences: Highlights pixels that differ from Image 1.
  - Image 2 Differences: Highlights pixels that differ from Image 2.
  - Combined Differences: Shows all differing pixels from both images in one overlay.
- A detailed statistical report is generated, summarizing the following:
  - Total number of pixels.
  - Number and percentage of differing pixels.
  - Tolerance level used.

### 6. **Error Handling**:
- The algorithm performs extensive validation on input images and parameters, including checks for:
  - Invalid file paths or image formats.
  - Inconsistent image sizes or modes.
  - Invalid or out-of-bounds tolerance values.


## Automated Testing

This repository includes automated test cases for the image comparison script. 
Below are the instructions for setting up and running the automated tests:

Before running the tests, you need to install the following Python libraries:

- `pytest`: For running the test cases.
- `pytest-html`: For generating HTML test reports.
- `pytest-cov`: For measuring code coverage.
- `Pillow`, `NumPy`, and `scikit-image`: As required by the image comparison scripts.

You can install these libraries using `pip`:

```bash
pip install pytest pytest-html pytest-cov pillow numpy scikit-image
```

### 2. **Generating Test Data Using test_data_generator.py**:
The test data needed for the automated tests can be generated by executing the test_data_generator.py script. 
This script creates the necessary image files that will be used in the automated test cases.

To run the script:

```bash
python test_data_generator.py
```
This will generate a set of test images in the specified directory, which will be used by the test cases in the automated_test_cases.py file.

### 3. **Running the Automated Tests**:
Once the necessary test data is generated and the libraries are installed, you can execute the automated test cases located in the automated_test_cases.py file.

Here are the commands you can use to execute the tests and generate various reports:

#### 3.1 **Run the Tests and Generate an HTML Report**:
To run the test cases and generate an HTML report (test_report.html), execute the following command:

```bash
cd tests
python3 -m pytest --html=../output/test_report.html --self-contained-html automated_test_cases.py
```
This will run the tests and output the results to test_report.html, which can be opened in any web browser.

#### 3.2 **Measure Code Coverage**:
To measure the code coverage of your test cases, use the following commands:

```bash
coverage run --source=../src -m pytest automated_test_cases.py
coverage html -d ../output/coverage

```

These commands will measure the coverage and generate an HTML report. 
The resulting htmlcov folder will contain the index.html file, which displays the coverage details for each file.

### 4. **Understanding the Output Reports**:
After running the tests and generating the reports, there are a few key reports you should review:

- test_report.html: This is the HTML report generated by pytest that contains the results of all the test cases. It shows which tests passed, failed, or were skipped.
- index.html: This report is generated by the coverage tool and contains the coverage details for the image_compare.py and color_similarity_detection_technique.py files. It shows which lines of code were executed during the tests and highlights any uncovered lines.
