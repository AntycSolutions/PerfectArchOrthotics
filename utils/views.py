import os
import urllib

from django.conf import settings
from django.http import HttpResponse


def _rescale(input_file, width, height, force=True):
    from PIL import Image
    from PIL import ImageOps
    from io import BytesIO

    try:
        max_width = int(width)
        max_height = int(height)
    except:
        return None

    img = Image.open(input_file)
    if not force:
        img.thumbnail((max_width, max_height), Image.ANTIALIAS)
    else:
        img = ImageOps.fit(img, (max_width, max_height,),
                           method=Image.ANTIALIAS)

    tmp = BytesIO()
    img.save(tmp, 'JPEG')
    tmp.seek(0)
    output_data = tmp.getvalue()
    img.close()
    tmp.close()

    return output_data


def get_thumbnail(request, width, height, url):
    decoded_url = urllib.parse.unquote(url)
    media_root = settings.MEDIA_ROOT
    media_url = settings.MEDIA_URL
    partial_path = decoded_url.replace(media_url, "")
    path = os.path.join(media_root, partial_path)
    thumbnail = _rescale(path, width, height, force=False)
    return HttpResponse(thumbnail, 'image/jpg')
