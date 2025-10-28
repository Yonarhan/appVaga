
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
   
    path('admin/', admin.site.urls),
     
    path('', include('sitevagas.urls')),
        
]
