import random
import datetime
from io import BytesIO
import qrcode
import os


def generate_slug():
    from shortener.models import Url
    slug = _generate_new_slug()
    while Url.objects.filter(slug=slug).exists():
        slug = _generate_new_slug()
    return slug


def _generate_new_slug():
    # new_slug = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=5))
    all_symbols = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    new_slug = ''.join(random.choices(all_symbols, k=5))
    return new_slug


def get_obj_and_increase_counter(obj):
    obj.counter += 1
    obj.last_redirect = datetime.datetime.now()
    obj.save()
    return obj


def qr_generate(slug):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(os.getenv('SITE_HOST') + '/' + str(slug))
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    qrByte = BytesIO()
    img.save(qrByte)
    return qrByte.getvalue()
