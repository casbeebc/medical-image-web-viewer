from django.shortcuts import render

from .models import ImageSeries


def image_series_list(request):
    return render(request, 'image_series_list.html', {
        'all_image_series': ImageSeries.objects.all(),
    })
