from fastapi import Request, UploadFile

class ImageUploadForm:
    def __init__(self, req: Request) -> None:
        self.req = req
        self.upload_errors = []
        self.selected_model = ""
        self.input_image: UploadFile = None

    async def load_data(self):
        form_data = await self.req.form()
        self.selected_model = form_data.get("model_id")
        self.input_image = form_data.get("uploaded_image")

    def is_valid(self) -> bool:
        if not self.selected_model or not isinstance(self.selected_model, str):
            self.upload_errors.append("Model ID must be a valid string.")

        if not self.input_image or not self.input_image.filename.lower().endswith(".jpeg"):
            self.upload_errors.append("Please upload a valid .jpeg image.")

        return not self.upload_errors