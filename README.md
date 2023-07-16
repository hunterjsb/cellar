# TEuPAC

###  W

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
