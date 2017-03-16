from django.conf import settings
from django.shortcuts import render

from .models import ImageSeries

def image_series_list(request):
    return render(request, 'image_series_list.html', {
        'all_image_series': ImageSeries.objects.all(),
    })

def image_series_view(request, id):
    series = ImageSeries.objects.get(id=id)
    voxels = series.voxels
    
    return render(request, 'image_series_view.html', {
        'series': series,
        'voxels': voxels,
    })
