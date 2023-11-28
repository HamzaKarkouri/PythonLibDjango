# views.py
import pandas as pd
from django.shortcuts import render,redirect
from .forms import CSVUploadForm
from django.utils.datastructures import MultiValueDictKeyError
import csv
from django.db import models

import os
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import UploadedFile


def process_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        selected_option = request.POST.get('selectedOption')
        data =request.POST.get('data')
        print(data,type(data))

        if form.is_valid():
            csv_data = form.cleaned_data['csv_file']
            df = pd.read_csv(csv_data)

            uploaded_file = UploadedFile(file=csv_data)
            uploaded_file.save()
            data_html = df
                
            lendata = len(data_html)


            return render(request, 'success.html', {'data': data_html,'lendata':lendata})
    else:
        form = CSVUploadForm()
        
    return render(request, 'success.html', {'form': form})


def index(request):
    return render(request, 'main.html')
