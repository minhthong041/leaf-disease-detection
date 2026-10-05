import uuid
from io import BytesIO
from pathlib import PurePath

from django.core.files.base import ContentFile
from django.utils import timezone
from PIL import Image, ImageOps


def _uuid_path(folder, filename):
    # Không giữ tên file gốc / user_id trong đường dẫn để ảnh lưu lại được ẩn danh
    ext = PurePath(filename).suffix.lower() or '.jpg'
    return f'{folder}/{timezone.now():%Y/%m}/{uuid.uuid4().hex}{ext}'


# upload_to phải là hàm cấp module để Django serialize được vào migration
def diagnosis_original_path(instance, filename):
    return _uuid_path('uploads', filename)


def diagnosis_processed_path(instance, filename):
    return _uuid_path('results', filename)


def strip_image_metadata(field_file):
    """Trả về bản sao ảnh không còn EXIF (GPS, thiết bị...), giữ đúng chiều xoay."""
    field_file.seek(0)
    with Image.open(field_file) as img:
        fmt = img.format or 'JPEG'
        clean = ImageOps.exif_transpose(img)
        if fmt == 'JPEG' and clean.mode not in ('RGB', 'L'):
            clean = clean.convert('RGB')
        buffer = BytesIO()
        clean.save(buffer, format=fmt, **({'quality': 95} if fmt == 'JPEG' else {}))
    return ContentFile(buffer.getvalue(), name=PurePath(field_file.name).name)
