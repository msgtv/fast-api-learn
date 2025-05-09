import shutil

from fastapi import UploadFile, APIRouter


router = APIRouter(
    prefix="/images",
    tags=["Image loading"]
)


@router.post("/hotels")
async def add_hotel_image(name: int, file: UploadFile):
    with open(f"app/static/images/{name}.webp", "wb+") as fo:
        shutil.copyfileobj(file.file, fo)
