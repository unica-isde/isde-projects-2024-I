from PIL import ImageEnhance
from app.ml.classification_utils import fetch_image

def apply_transformations(img_id: str, color_factor: float, brightness_level: float, contrast_level: float, sharpness_level: float):
    """Applies enhancement transformations to the selected image."""
    image = fetch_image(img_id)
    image = ImageEnhance.Color(image).enhance(color_factor)
    image = ImageEnhance.Brightness(image).enhance(brightness_level)
    image = ImageEnhance.Contrast(image).enhance(contrast_level)
    image = ImageEnhance.Sharpness(image).enhance(sharpness_level)
    return image
