"""ai_evm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from .views import start, dbg
from detect_face.views import detect_face
from detect_person.views import detect_person
from detect_mask.views import detect_mask
from recognize_face.views import recognize_face

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', start, name = 'start'),
    path('dbg/', dbg, name = 'dbg'),
    path('detect_face/', detect_face, name = 'detect_face'),
    path('detect_person/', detect_person, name = 'detect_person'),
    path('detect_mask/', detect_mask, name = 'detect_mask'),
    path('recognize_face', recognize_face, name = 'recognize_face')
]
