import os
from app.config import Configuration

conf = Configuration()

def list_images():
    img_names = filter(
        lambda x: x.endswith(".JPEG"), os.listdir(conf.image_folder_path)
    )
    return list(img_names)

async def add_image_to_list(image, name: str) -> bool:
    if not name.lower().endswith((".jpeg", ".jpg", ".png")):
        return False

    save_path = os.path.join(conf.image_folder_path, name)
    with open(save_path, "wb") as f:
        f.write(await image.read())

    return True
