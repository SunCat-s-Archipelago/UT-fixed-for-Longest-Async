from kivy.core.image import ImageLoader, ImageLoaderBase, ImageData
from kivy.uix.image import AsyncImage
from typing import List, Union
import pkgutil
import io


class ImageLoaderPkgutil(ImageLoaderBase):
    def load(self, filename: str) -> List[ImageData]:
        # take off the "ap:" prefix
        module, path = filename[3:].split("/", 1)
        data = pkgutil.get_data(module, path)
        return self._bytes_to_data(data)

    def _bytes_to_data(self, data: Union[bytes, bytearray]) -> List[ImageData]:
        from PIL import Image as PImage
        p_im = PImage.open(io.BytesIO(data)).convert("RGBA")
        im_d = ImageData(p_im.size[0], p_im.size[1], p_im.mode.lower(), p_im.tobytes())
        return [im_d]
    
class ApAsyncImage(AsyncImage):
    def is_uri(self, filename: str) -> bool:
        if filename.startswith("ap:"):
            return True
        else:
            return super().is_uri(filename)

# grab the default loader method so we can override it but use it as a fallback
_original_image_loader_load = ImageLoader.load


def load_override(filename: str, default_load=_original_image_loader_load, **kwargs):
    if filename.startswith("ap:"):
        return ImageLoaderPkgutil(filename)
    else:
        return default_load(filename, **kwargs)

ImageLoader.load = load_override