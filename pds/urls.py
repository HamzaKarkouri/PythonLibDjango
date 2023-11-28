from django.urls import path
from .views import list_uploaded_files

urlpatterns = [
    # ... other URL patterns
    path('list_files/', list_uploaded_files, name='list_files'),

]