"""Image helpers for the IntelliOptics SDK."""

from __future__ import annotations

from importlib import import_module
from importlib.util import find_spec
from io import BufferedIOBase, BytesIO
from pathlib import Path
from typing import IO, Any, Union, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - type checking only
    from PIL.Image import Image as PILImage
    from numpy import ndarray
else:  # pragma: no cover - runtime fallback types
    PILImage = Any  # type: ignore[assignment]
    ndarray = Any  # type: ignore[assignment]

_pil_image_module = import_module("PIL.Image") if find_spec("PIL.Image") else None
_numpy_module = import_module("numpy") if find_spec("numpy") else None

ImageLike = Union[str, bytes, bytearray, IO[bytes], BufferedIOBase, PILImage, ndarray]


def _looks_like_jpeg(data: bytes) -> bool:
    return len(data) >= 2 and data[0:2] == b"\xff\xd8"


def _ensure_jpeg_bytes(data: bytes) -> bytes:
    if _looks_like_jpeg(data):
        return data

    if _pil_image_module is None:
        raise RuntimeError("Pillow is required to convert non-JPEG inputs to JPEG")

    with _pil_image_module.open(BytesIO(data)) as pil_image:  # type: ignore[attr-defined]
        return _encode_with_pillow(pil_image)


def _read_file_like(stream: Any) -> bytes:
    data = stream.read()
    if not isinstance(data, bytes):
        raise TypeError("File-like objects must return bytes when read()")

    if hasattr(stream, "seek") and callable(stream.seek):
        try:  # pragma: no cover - best effort rewind
            stream.seek(0)
        except Exception:
            pass

    return data


def _encode_with_pillow(pil_image: Any) -> bytes:
    buffer = BytesIO()
    pil_image.convert("RGB").save(buffer, format="JPEG", quality=95)
    return buffer.getvalue()


def _encode_numpy(array: Any) -> bytes:
    if _numpy_module is None:
        raise RuntimeError("numpy is required to encode numpy arrays to JPEG")

    if array.ndim not in (2, 3):
        raise ValueError("numpy array must have 2 or 3 dimensions")
    if array.ndim == 3 and array.shape[2] not in (1, 3):
        raise ValueError("numpy array must have shape (H, W, 3) or (H, W, 1)")
    if _pil_image_module is None:
        raise RuntimeError("Pillow is required to encode numpy arrays to JPEG")

    if array.ndim == 3 and array.shape[2] == 3:
        rgb = array.astype("uint8")
    else:  # grayscale
        rgb = array.squeeze().astype("uint8")

    image = _pil_image_module.fromarray(rgb)
    return _encode_with_pillow(image)


def to_jpeg_bytes(image: ImageLike) -> bytes:
    """Normalise supported image inputs into a JPEG byte payload."""

    pil_image_class = getattr(_pil_image_module, "Image", None)
    if pil_image_class is not None and isinstance(image, pil_image_class):
        return _encode_with_pillow(image)

    ndarray_class = getattr(_numpy_module, "ndarray", None)
    if ndarray_class is not None and isinstance(image, ndarray_class):
        return _encode_numpy(image)

    if isinstance(image, (bytes, bytearray)):
        return _ensure_jpeg_bytes(bytes(image))

    if hasattr(image, "read") and callable(image.read):  # file-like object
        data = _read_file_like(image)
        return _ensure_jpeg_bytes(data)

    if isinstance(image, (str, Path)):
        data = Path(image).read_bytes()
        return _ensure_jpeg_bytes(data)

    raise TypeError("Unsupported image type")
