import os
import json
import tempfile
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("agg")

from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import Configuration
from app.utils import list_images, get_image_path, generate_histogram, add_image_to_list
from app.forms.classification_form import ClassificationForm
from app.forms.histogram_form import HistogramForm
from app.forms.upload_form import UploadForm
from app.forms.transformation_form import ImageTransformForm
from app.ml.classification_utils import classify_image
from app.ml.transformation_utils import apply_transformations

app = FastAPI()
config = Configuration()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/info")
def info() -> dict[str, list[str]]:
    """Returns a dictionary with the list of models and
    the list of available image files."""
    list_of_images = list_images()
    list_of_models = Configuration.models
    data = {"models": list_of_models, "images": list_of_images}
    return data


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """The home page of the service."""
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/classifications")
def create_classify(request: Request):
    return templates.TemplateResponse(
        "classification_select.html",
        {"request": request, "images": list_images(), "models": Configuration.models},
    )


@app.post("/classifications")
async def request_classification(request: Request):
    form = ClassificationForm(request)
    await form.load_data()
    image_id = form.image_id
    model_id = form.model_id
    classification_scores = classify_image(model_id=model_id, img_id=image_id)
    return templates.TemplateResponse(
        "classification_output.html",
        {
            "request": request,
            "image_id": image_id,
            "classification_scores": json.dumps(classification_scores),
        },
    )

@app.get("/histogram", response_class=HTMLResponse)
def show_histogram_form(request: Request):
    return templates.TemplateResponse(
        "histogram_select.html", {"request": request, "images": list_images()}
    )


@app.post("/histogram", response_class=HTMLResponse)
async def generate_histogram_output(request: Request):
    form = HistogramForm(request)
    await form.load_data()
    if not form.is_valid():
        return templates.TemplateResponse(
            "histogram_select.html", {"request": request, "images": list_images(), "errors": form.errors}
        )

    image_path = get_image_path(form.image_id)
    histogram_data = generate_histogram(image_path)

    return templates.TemplateResponse(
        "histogram_output.html",
        {"request": request, "image_id": form.image_id, "histogram_data": histogram_data}
    )


@app.get("/image-transformation", response_class=HTMLResponse)
def show_transformation_form(request: Request):
    return templates.TemplateResponse(
        "image_transformation_select.html",
        {"request": request, "images": list_images()},
    )

@app.post("/image-transformation", response_class=HTMLResponse)
async def apply_image_transformation(request: Request):
    form = ImageTransformForm(request)
    await form.load_data()

    if not form.is_valid():
        return templates.TemplateResponse(
            "image_transformation_select.html",
            {"request": request, "images": list_images(), "errors": form.errors},
        )

    transformed_image = apply_transformations(
        img_id = form.img_id,
        color_factor = form.color_factor,
        brightness_level = form.brightness_level,
        contrast_level = form.contrast_level,
        sharpness_level = form.sharpness_level,
    )

    buffer = BytesIO()
    transformed_image.save(buffer, format="PNG")
    img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    buffer.close()

    return templates.TemplateResponse(
        "image_transformation_output.html",
        {
            "request": request,
            "image_id": form.img_id,
            "transformed_image_url": f"data:image/png;base64,{img_base64}",
        },
    )

