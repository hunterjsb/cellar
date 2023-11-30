from flask import Flask, request, render_template, send_from_directory
from skimage import measure, color
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from skimage.segmentation import watershed
from skimage.feature import peak_local_max
from scipy import ndimage as ndi

from cellar.utils import cell_names, save_image_binary
from cellar.models import SubmitForm

import os

matplotlib.use('Agg')  # Use the 'Agg' backend for Matplotlib
app = Flask(__name__, static_folder='imgs')


@app.route('/get-filenames', methods=['GET'])
def get_filenames():
    files = os.listdir(app.static_folder)
    return {'files': files}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    form = SubmitForm.from_request(request)
    binary_image, filename = save_image_binary(request, form, app.static_folder)

    # Compute Euclidean distance from every binary pixel to the nearest zero pixel then find peaks in this distance map
    distance = ndi.distance_transform_edt(binary_image)
    coords = peak_local_max(distance, min_distance=20, labels=binary_image)
    mask = np.zeros(distance.shape, dtype=bool)
    mask[tuple(coords.T)] = True
    markers, _ = ndi.label(mask)
    labels: np.ndarray = watershed(-distance, markers, mask=binary_image)
    properties = measure.regionprops(labels)

    # Create a visualization for the labeled regions
    fig, ax = plt.subplots(figsize=(10, 10))
    image_label_overlay = color.label2rgb(labels, image=binary_image, bg_label=0, alpha=0.3)
    ax.imshow(image_label_overlay)

    i, total_area = 0, 0
    labeled_areas = {}
    for region in properties:
        area_nm2 = region.area / form.scale_factor_px2_per_nm2
        if form.minsize < area_nm2 < form.maxsize:
            area_str = f'{area_nm2:.2f} nm^2'
            total_area += area_nm2

            # Get the name for this cell
            name = cell_names[i]
            labeled_areas[name] = area_nm2
            i += 1 if i < len(cell_names) - 1 else -len(cell_names) + 1  # avoid 'name' IndexError

            # Draw the bounding box and label
            minr, minc, maxr, maxc = region.bbox
            rect = plt.Rectangle((minc, minr), maxc - minc, maxr - minr, fill=False, edgecolor='red', linewidth=3)
            ax.add_patch(rect)
            ax.text(minc, minr - 5, f'{name}: {area_str}', color='white', fontsize=12)

    # Save the visualization
    viz_filename = f'viz_{filename}.png'
    viz_filepath = os.path.join(app.static_folder, viz_filename)
    plt.savefig(viz_filepath)

    return {'areas': labeled_areas, 'viz_filename': viz_filename, 'avg_area': total_area/i if i else total_area}


@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(app.static_folder, filename)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
