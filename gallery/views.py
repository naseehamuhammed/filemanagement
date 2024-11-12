from django.shortcuts import render, redirect
from .forms import PhotoForm
from .models import Photo
from .tasks import send_welcome_email_async, generate_thumbnail


def gallery_view(request):
    photos = Photo.objects.all()
    return render(request, "gallery/gallery.html", {"photos": photos})


def upload_photo(request):
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the photo only once
            photo = form.save()

            # Trigger the Celery task to generate the thumbnail asynchronously
            generate_thumbnail.delay(photo.id)

            # Optionally send welcome email asynchronously
            send_welcome_email_async.delay()

            # Redirect to the gallery view
            return redirect("gallery")
    else:
        form = PhotoForm()
    return render(request, "gallery/upload.html", {"form": form})

