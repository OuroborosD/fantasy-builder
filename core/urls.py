"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static # NEW
from django.conf import settings # NEW,  importar os settings.

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('characters/',include('character.urls')),
    path('',include('helper.urls')),        
    path('<slug:slug_book>/world/', include('geography.urls')),
    path('<slug:slug_book>/characters/', include('murim.urls')),
    path('<slug:slug_book>/bestiary/', include('bestiary.urls')),
]+ static(settings.MEDIA_URL,   document_root=settings.MEDIA_ROOT)
