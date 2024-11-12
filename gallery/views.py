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
            photo = form.save()
            generate_thumbnail.delay(photo.id)
            send_welcome_email_async.delay()
            return redirect("gallery")
    else:
        form = PhotoForm()
    return render(request, "gallery/upload.html", {"form": form})

