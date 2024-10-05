
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


## Automated Testing

This repository includes automated test cases for the image comparison script. Below are the instructions for setting up and running the automated tests:

### 1. **Needed Libraries and Installation**:

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
python3 -m pytest --html=test_report.html --self-contained-html automated_test_cases.py
```
This will run the tests and output the results to test_report.html, which can be opened in any web browser.

#### 3.2 **Measure Code Coverage**:
To measure the code coverage of your test cases, use the following commands:

```bash
coverage run -m pytest automated_test_cases.py
coverage html
```

These commands will measure the coverage and generate an HTML report. 
The resulting htmlcov folder will contain the index.html file, which displays the coverage details for each file.

### 4. **Understanding the Output Reports**:
After running the tests and generating the reports, there are a few key reports you should review:

- test_report.html: This is the HTML report generated by pytest that contains the results of all the test cases. It shows which tests passed, failed, or were skipped.
- image_compare_py.html: This report is generated by the coverage tool and contains the coverage details for the image_compare.py file. It shows which lines of code were executed during the tests and highlights any uncovered lines.
- color_similarity_detection_technique_py.html: This is another coverage report, specifically for the color_similarity_detection_technique.py file. It also highlights the coverage of the code and indicates which parts of the code were executed by the tests.
