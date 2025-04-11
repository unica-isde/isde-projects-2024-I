import os
import base64
import io
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from app.config import Configuration

conf = Configuration()


def list_images():
    """Returns the list of available images."""
    return [img for img in os.listdir(conf.image_folder_path) if img.endswith(".JPEG")]


def get_image_path(image_id: str) -> str:
    """Builds the full path for a given image ID."""
    return os.path.join(conf.image_folder_path, image_id)


def generate_histogram(image_path: str) -> str:
    """Generates a histogram for the given image and returns it as base64."""
    img = Image.open(image_path)
    img_array = np.array(img)

    plt.figure(figsize=(6, 4))

    if img_array.ndim == 2:  # Grayscale
        plt.hist(img_array.ravel(), bins=256, color='gray', alpha=0.7, label="Grayscale")
    else:
        channels = ['red', 'green', 'blue']
        for idx, color in enumerate(channels):
            plt.hist(img_array[:, :, idx].ravel(), bins=256, color=color, alpha=0.5, label=color.capitalize())

    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')
    plt.legend()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)

    return base64.b64encode(buffer.getvalue()).decode()
