# Medical Image Web Viewer

A very simple slice viewer for DICOM files

## Setup

Requires Python 3

Run these commands:

    pip install -r requirements.txt
    python manage.py migrate
    python manage.py createsuperuser

# Run

    python manage.py runserver
    Go to: 
           * http://127.0.0.1:8000/admin to add DICOM zip files
           * http://127.0.0.1:8000 to see the listings
           * click View to see the image series