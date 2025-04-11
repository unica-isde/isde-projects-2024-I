from fastapi import Request

class HistogramRequestForm:
    def __init__(self, incoming_request: Request) -> None:
        self.incoming_request: Request = incoming_request
        self.validation_errors: list = []
        self.selected_image_name: str = ""

    async def parse_form_data(self):
        submitted_form = await self.incoming_request.form()
        self.selected_image_name = submitted_form.get("image_id")

    def validate(self):
        if not self.selected_image_name or not isinstance(self.selected_image_name, str):
            self.validation_errors.append("Please select a valid image name.")
        return len(self.validation_errors) == 0
