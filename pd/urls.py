from django.urls import path
from pd import views

urlpatterns = [
   
  
    path('import-csv/', views.process_csv, name='process_csv'),
    path('', views.index, name='index'),

]
