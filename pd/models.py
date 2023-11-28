# models.py
import csv
from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploaded_csv/')
    uploaded_at = models.DateTimeField(auto_now_add=True)