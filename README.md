# CellAr

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

### Scale Factor

The "Scale Factor" input field allows users to specify a factor that adjusts the intensity of the center-weighted thresholding. The value must be between 0.01 and 1. By default, the value is 0.35.

### Offset

The "Offset" input field allows users to specify an offset that adjusts the base threshold of the center-weighted thresholding. The value must be between 0.01 and 1. By default, the value is 0.6.

## Output

After the user clicks the "Submit" button, the application processes the image and displays the processed image. The detected cells are labeled and surrounded by a bounding box. The area of each cell (in square nanometers) is displayed next to the corresponding cell. Below the image, the application displays a list of all detected cell areas (in square nanometers).

## Calculations

The script converts the pixel measurements to nanometers using a given conversion factor. The default conversion factor is calculated as follows:

- First, it is determined that 155 pixels correspond to 100 nanometers. This gives a conversion factor of `100 / 155` nanometers per pixel.

- This is then squared to convert the area measurements from square pixels to square nanometers.

The threshold image function creates a distance map where the value of each pixel is the Euclidean distance from the center of the image. This map is then normalized to the range [0, 1], scaled and offset according to the user's input, and finally multiplied with the original image. The resulting image is then thresholded to create a binary image where the cells are distinct from the background.

The script then uses the watershed algorithm for segmentation. It starts by computing the Euclidean distance from every binary pixel to the nearest zero pixel and finds the peaks in this distance map. These peaks are used as markers for the watershed algorithm, which segments the image into different regions.

The script calculates the area of each of these regions in square nanometers and labels each cell with its corresponding area.

## Image Processing and Mathematics

In the `threshold_img` function, the image processing involves several mathematical operations. Here's a step-by-step breakdown of what happens:

```python
import numpy as np
import cv2

def threshold_img(image, threshold=110, scale_factor=0.5, offset=0.5) -> np.ndarray:
    # Calculate the Euclidean distance of each pixel from the center
    x = np.arange(image.shape[1])
    y = np.arange(image.shape[0])
    xx, yy = np.meshgrid(x, y)
    center_x = image.shape[1] / 2
    center_y = image.shape[0] / 2
    distance_map = np.sqrt((xx - center_x)**2 + (yy - center_y)**2)

    # Normalize the distance map to have values between 0 and 1
    distance_map = (distance_map - distance_map.min()) / (distance_map.max() - distance_map.min())

    # Scale and offset the distance map
    distance_map = scale_factor * distance_map + offset

    # Clamp values to the range [0, 1]
    distance_map = np.clip(distance_map, 0, 1)

    # Multiply the distance map with the original image
    image_adjusted = (image * distance_map).astype(np.uint8)

    # Apply a global threshold to the resulting image
    _, binary_image = cv2.threshold(image_adjusted, threshold, 255, cv2.THRESH_BINARY)
    return binary_image
```

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
