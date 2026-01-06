from fastapi import APIRouter, UploadFile, File, Depends, status, Request
from backend.app.utils.uploads import validate_image, save_upload
from backend.app.core.ratelimit import limiter

router = APIRouter(prefix="/uploads", tags=["uploads"])


@router.post("/images", status_code=status.HTTP_201_CREATED)
@limiter.limit("20/minute")  # limit image uploads to protect abuse
async def upload_image(request: Request, file: UploadFile = File(...)):
    """Upload an image with validation (size, type)."""
    await validate_image(file)
    path = await save_upload(file)
    return {"path": path, "filename": file.filename}
