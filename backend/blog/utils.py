# blog/utils.py
import uuid
from pathlib import Path


def blog_cover_upload_to(instance, filename):
    extension = Path(filename).suffix.lower() or ".jpg"
    return f"blog/cover/{uuid.uuid4().hex}{extension}"