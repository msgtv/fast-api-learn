import shutil

from fastapi import UploadFile, APIRouter

from app.tasks.tasks import process_pic


router = APIRouter(
    prefix="/images",
    tags=["Image loading"]
)


@router.post("/hotels")
async def add_hotel_image(name: int, file: UploadFile):
    im_path = f"app/static/images/{name}.webp"
    with open(im_path, "wb+") as fo:
        shutil.copyfileobj(file.file, fo)

    process_pic.delay(im_path)
