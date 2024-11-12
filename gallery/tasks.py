import time
from celery import shared_task
from django.core.mail import send_mail
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from .models import Photo
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
import os


@shared_task
def generate_thumbnail(photo_id):
    # Fetch the photo object
    photo = Photo.objects.get(id=photo_id)

    # Open the uploaded image file
    image_path = photo.image.path  # Get the path of the original image
    img = Image.open(image_path)

    # Define the thumbnail size (e.g., 200x200)
    thumbnail_size = (150, 150)

    # Resize the image
    img.thumbnail(thumbnail_size)

    # Save the thumbnail to a temporary in-memory file
    thumb_io = BytesIO()
    img.save(thumb_io, img.format)
    thumb_io.seek(0)

    # Save the thumbnail to the `thumbnail` field
    # Create an InMemoryUploadedFile to be saved in the model
    photo.thumbnail.save(
        os.path.basename(photo.image.name),  # Use original image name for thumbnail
        InMemoryUploadedFile(
            thumb_io, None, photo.image.name, 'image/jpeg', thumb_io.getbuffer().nbytes, None
        ),
        save=True
    )

def send_welcome_mail_realtime():
    time.sleep(5)
    send_mail(
        "Welcome!",
        "Thanks for uploading a photo! This mail was send in realtime.",
        "from@example.com",
        ["to@example.com"],
        fail_silently=False,
    )


@shared_task
def send_welcome_email_async():
    time.sleep(5)
    send_mail(
        "Welcome!",
        "Thanks for uploading a photo! This mail was send asynchronously.",
        "from@example.com",
        ["to@example.com"],
        fail_silently=False,
    )
