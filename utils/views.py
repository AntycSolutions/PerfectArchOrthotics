import os
import urllib

from django.conf import settings
from django.http import HttpResponse


def _get_exif(filename):
    import piexif
    # from PIL.ExifTags import TAGS

    orientation = None
    exif_bytes = None

    # exifinfo = img._getexif()
    # if exifinfo is not None:
    #     ret = {}
    #     for tag, value in exifinfo.items():
    #         decoded = TAGS.get(tag, tag)
    #         ret[decoded] = value
    #     for k, v in ret.items():
    #         if k == "Orientation":
    #             orientation = v

    try:
        zeroth_ifd, exif_ifd, gps_ifd = piexif.load(filename)

        if piexif.ZerothIFD.Orientation in zeroth_ifd:
            orientation = zeroth_ifd.pop(piexif.ZerothIFD.Orientation)
            exif_bytes = piexif.dump(zeroth_ifd, exif_ifd, gps_ifd)
    except:
        orientation = None
        exif_bytes = None

    return orientation, exif_bytes


def _update_orientation(img, orientation):
    from PIL import Image

    if orientation == 2:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    elif orientation == 3:
        img = img.rotate(180)
    elif orientation == 4:
        img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
    elif orientation == 5:
        img = img.rotate(-90).transpose(Image.FLIP_LEFT_RIGHT)
    elif orientation == 6:
        img = img.rotate(-90)
    elif orientation == 7:
        img = img.rotate(90).transpose(Image.FLIP_LEFT_RIGHT)
    elif orientation == 8:
        img = img.rotate(90)

    return img


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
    orientation, exif_bytes = _get_exif(input_file)
    if orientation:
        img = _update_orientation(img, orientation)
        img.save(tmp, 'JPEG', exif=exif_bytes)
    else:
        if img.mode != 'RGB':
            img.convert('RGB').save(tmp, 'JPEG')
        else:
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
