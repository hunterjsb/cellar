import numpy as np
import cv2
import matplotlib.pyplot as plt


def threshold_img(image, threshold=110, radial_contrast=0.5, image_brightness=0.5) -> np.ndarray:
    """
    :param image: the image to process
    :param threshold: determines how the final binary image distinguishes between light and dark areas
    :param radial_contrast: controls the contrast and brightness of the image based on the distance from the center
    :param image_brightness: uniformly adjusts the brightness across the entire image
    :return:
    """
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
    distance_map = radial_contrast * distance_map + image_brightness

    # Clamp values to the range [0, 1]
    distance_map = np.clip(distance_map, 0, 1)

    # Multiply the distance map with the original image
    image_adjusted = (image * distance_map).astype(np.uint8)

    # Apply a global threshold to the resulting image
    _, binary_image = cv2.threshold(image_adjusted, threshold, 255, cv2.THRESH_BINARY)
    return binary_image


if __name__ == '__main__':
    _image = cv2.imread('/cellar/imgs/cells_1.jpg', 0)
    # Display the resulting image
    bin_img = threshold_img(_image)
    plt.imshow(bin_img)
    plt.show()
