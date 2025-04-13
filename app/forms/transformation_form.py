from fastapi import Request


class ImageTransformForm:
    def __init__(self, req: Request) -> None:
        self.req = req
        self.errors = []
        self.img_id = ""
        self.color_factor = 1.0
        self.brightness_level = 1.0
        self.contrast_level = 1.0
        self.sharpness_level = 1.0

    async def load_data(self):
        form_data = await self.req.form()
        self.img_id = form_data.get("image_id")

        color = form_data.get("color")
        brightness = form_data.get("brightness")
        contrast = form_data.get("contrast")
        sharpness = form_data.get("sharpness")

        if color:
            self.color_factor = float(color)
        if brightness:
            self.brightness_level = float(brightness)
        if contrast:
            self.contrast_level = float(contrast)
        if sharpness:
            self.sharpness_level = float(sharpness)

    def is_valid(self) -> bool:
        if not self.img_id or not isinstance(self.img_id, str):
            self.errors.append("Please select a valid image.")
        if not (0.0 <= self.color_factor <= 1.0):
            self.errors.append("Color must be between 0.0 and 1.0.")
        if self.brightness_level < 0.0:
            self.errors.append("Brightness must be non-negative.")
        if self.contrast_level < 0.0:
            self.errors.append("Contrast must be non-negative.")
        if self.sharpness_level < 0.0:
            self.errors.append("Sharpness must be non-negative.")

        return not self.errors
