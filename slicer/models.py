import numpy as np

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models

import os
import shutil

from slicer.dicom_import import dicom_datasets_from_zip, combine_slices
from slicer.dicom_export import export_to_png

import zipfile

class ImageSeries(models.Model):
    dicom_archive = models.FileField(upload_to="dicom/")
    voxel_file = models.FileField(upload_to="voxels/")
    patient_id = models.CharField(max_length=64, null=True)
    study_uid = models.CharField(max_length=64)
    series_uid = models.CharField(max_length=64)

    @property
    def voxels(self):
        with self.voxel_file as f:
            voxel_array = np.load(f)
        return voxel_array
    
    @property
    def images_path(self):
        with self.voxel_file as f:
            path = settings.MEDIA_ROOT + "images/" + os.path.basename(f.name)
        return path
    
    def save(self, *args, **kwargs):
        with zipfile.ZipFile(self.dicom_archive, 'r') as f:
            dicom_datasets = dicom_datasets_from_zip(f)

        voxels, _ = combine_slices(dicom_datasets)
        content_file = ContentFile(b'')  # empty zero byte file
        np.save(content_file, voxels)
        self.voxel_file.save(name='voxels', content=content_file, save=False)
        self._export_pngs(voxels)
        
        self.patient_id = dicom_datasets[0].PatientID
        self.study_uid = dicom_datasets[0].StudyInstanceUID
        self.series_uid = dicom_datasets[0].SeriesInstanceUID
        super(ImageSeries, self).save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        
        # Delete the images folder as well
        shutil.rmtree(self.images_path)
        
        super(ImageSeries, self).delete(*args, **kwargs)
        
    def _export_pngs(self, voxels):
        path = self.images_path
        if not os.path.exists(path):
            os.makedirs(path)
        
        export_to_png(path, voxels)
        
    class Meta:
        verbose_name_plural = 'Image Series'
