# CellAr

- [Interface](#user-interface)
- [Calculations](#calculations)
    - [Equations](#equations)
    - [Methods](#explanation-of-methods)

### Cell Area Calculator 

This project uses image processing techniques to detect and quantify the area of cells in an image. Users can upload an image, and the application will process the image, detect cells, calculate their areas, and display the processed image with the detected cells.

## User Interface

The user interface consists of a form for users to upload images and specify parameters for the image processing algorithm.

### Image Upload

Users can upload an image using the "Image file" input field or select a previously uploaded image from the dropdown menu. The selected image will be processed when the user clicks the "Submit" button.

### Threshold

The "Threshold" input field allows users to specify a threshold value that the image processing algorithm uses to distinguish between cells and the background. The value must be between 0 and 255. By default, the value is 130.

### Minimum Size

The "Minimum size" input field allows users to specify the minimum size of an object (in pixels) that the image processing algorithm should consider as a cell. The value must be between 1 and 100,000. By default, the value is 5000.

### Radial Contrast (Scale Factor)

The "Radial Contrast" (previously "Scale Factor") input field allows users to specify a factor that adjusts the intensity of the center-weighted thresholding. The value must be between 0.01 and 1. By default, the value is 0.35.

### Global Brightness (Offset)

The "Global Brightness" (previously "Offset") input field allows users to specify an offset that adjusts the base threshold of the center-weighted thresholding. The value must be between 0.01 and 1. By default, the value is 0.6.

## Output

After the user clicks the "Submit" button, the application processes the image and displays the processed image. The detected cells are labeled and surrounded by a bounding box. The area of each cell (in square nanometers) is displayed next to the corresponding cell. Below the image, the application displays a list of all detected cell areas (in square nanometers).

## Calculations

The threshold image function creates a distance map where the value of each pixel is the Euclidean distance from the center of the image. This map is then normalized to the range [0, 1], scaled and offset according to the user's input, and finally multiplied with the original image. The resulting image is then thresholded to create a binary image where the cells are distinct from the background.

The script then uses the watershed algorithm for segmentation. It starts by computing the Euclidean distance from every binary pixel to the nearest zero pixel and finds the peaks in this distance map. These peaks are used as markers for the watershed algorithm, which segments the image into different regions.

The script calculates the area of each of these regions in square nanometers and labels each cell with its corresponding area.

### Equations

- Creating a distance map:

    $`d_{ij} = \sqrt{(i - c_x)^2 + (j - c_y)^2}`$
   
    where $`d_{ij}`$ is the distance of a pixel at location $`(i, j)`$ from the center of the image $`(c_x, c_y)`$.

- Normalizing the distance map:
    
    $`d'_{ij} = \frac{d_{ij} - \min(d)}{\max(d) - \min(d)}`$
   
    where $`d'_{ij}`$ is the normalized distance, and $`min(d)`$ and $`max(d)`$ are the minimum and maximum values in the distance map, respectively.

- Scaling and offsetting the distance map:

    $`d''_{ij} = \text{scale} \cdot d'_{ij} + \text{offset}`$

    where $`d''_{ij}`$ is the final distance map used, and $`scale`$ and $`offset`$ are the provided scale and offset values.

- Adjusting the image:

    $`I'_{ij} = I_{ij} \cdot d''_{ij}`$

    where $`I'_{ij}`$ is the pixel value in the adjusted image, and $`I_{ij}`$ is the pixel value in the original grayscale image.

- Thresholding the image:

    $`\text{if } I'_{ij} \geq \text{threshold, then } B_{ij} = 255 \text{ else } B_{ij} = 0`$

    where $`B_{ij}`$ is the pixel value in the binary image.

- Computing the Euclidean distance from every white pixel to the nearest black pixel:

    $`D_{ij} = \min(\sqrt{(i - i')^2 + (j - j')^2})`$

    where $`D_{ij}`$ is the Euclidean distance at pixel $`(i, j)`$, and $`(i', j')`$ are the coordinates of all black pixels in the image.

- Applying the watershed algorithm, labelling the regions, and computing the area of each cell:

    $`W(D_{ij})`$


- Converting the area to nm²:

    $`A_{\text{nm}^2} = A_{\text{px}^2} / \text{scale\_factor\_px2\_per\_nm2}`$

    where $`A_{\text{nm}^2}`$ is the area in nm², $`A_{\text{px}^2}`$ is the area in pixels, and $`\text{scale\_factor\_px2\_per\_nm2}`$ is the provided conversion factor.

Please keep in mind that the above LaTeX represents only a rough approximation of the image processing algorithms, which include many additional steps and subtleties not captured by these equations. Some parts of the code, such as the peak finding and the watershed algorithm, are quite complex and would require extensive mathematical exposition to fully capture in LaTeX notation.

### Explanation of Methods

#### Euclidean Distance Calculation: 
For each pixel in the image, we calculate its Euclidean distance from the center of the image. This creates a distance map where the value of each pixel is proportional to its distance from the center.

#### Normalization: 
The distance map is then normalized to have values between 0 and 1. This is done by subtracting the minimum value of the distance map from each value, and then dividing by the range of the distance map (max - min).

#### Scaling and Offsetting: 
The normalized distance map is then scaled and offset according to the user's input. The scaling step multiplies each value in the distance map by the scale factor, effectively changing the "spread" of the values. The offset step then adds the offset value to each value in the distance map.

#### Clamping: 
The values in the distance map are then clamped to the range [0, 1] to ensure that no values fall outside this range after scaling and offsetting.

#### Multiplication with Original Image: 
The processed distance map is then multiplied with the original image. This has the effect of making the center of the image brighter and the edges darker, because the values in the distance map are larger near the center and smaller near the edges.

#### Thresholding: 
Finally, a global threshold is applied to the resulting image to create a binary image. Pixels with values above the threshold are set to white (255), and pixels with values below the threshold are set to black (0).

### Watershedding
Watershedding is a popular image segmentation technique used in image processing. It works by treating the image like a topographical map, with bright pixels representing high elevations and dark pixels representing low elevations. The algorithm then "floods" the image from the bottom up, with different "watersheds" forming in the basins between high points. These watersheds then serve as the boundaries between different objects in the image.

The watershed algorithm is used in this project to separate overlapping cells. After creating a binary image using the threshold_img function, the script uses the watershed algorithm to segment the image, creating a label for each detected cell. These labels are then used to calculate the area of each cell and display the processed image with each cell labeled and outlined.
