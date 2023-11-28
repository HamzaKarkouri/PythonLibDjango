
from django.contrib import admin
from django.urls import path,include
from pd import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pd.urls')), 
    path('vis/', include('vis.urls')),
    path('pandas/', include('pds.urls')), 
    
   
]
