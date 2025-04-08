import json
from io import BytesIO
import base64
import os
import matplotlib.pyplot as plt
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import BackgroundTasks
from fastapi.responses import FileResponse
from app.config import Configuration
from app.forms.classification_form import ClassificationForm
from app.forms.histogram_form import HistogramForm
from app.ml.classification_utils import classify_image
from app.utils import list_images,generate_histogram,get_image_path
from app.utils import add_image_to_list
import tempfile

import matplotlib
matplotlib.use("agg")


app = FastAPI()
config = Configuration()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Histogram Creation

@app.get("/histogram", response_class=HTMLResponse)
def create_histogram(request: Request):
    """Creates the page for the histogram form.

    Args:
        request (Request): request issued from base.html

    Returns:
        (TemplateResponse): TemplateResponse with histogram_select.html
    """
    return templates.TemplateResponse(
        "histogram_select.html",
        {"request": request, "images": list_images()}
    )


@app.post("/histogram")
async def request_histogram(request: Request):
    """Processes the form submission and returns the histogram image.

    Args:
        request (Request): issued from histogram_select.html

    Returns:
        (Template_Response): TemplateResponse with histogram_output.html to display the histogram
    """
    form = HistogramForm(request)
    await form.load_data()
    error = form.errors

    if not form.is_valid():
        return templates.TemplateResponse("histogram_select.html", {"request": request, "errors": error})

    image_path = get_image_path(form.image_id)
    histogram_data = generate_histogram(image_path)

    return templates.TemplateResponse(
        "histogram_output.html",
        {"request": request, "image_id": form.image_id, "histogram_data": histogram_data}
    )


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
