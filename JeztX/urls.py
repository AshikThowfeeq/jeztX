"""
URL configuration for JeztX project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from api.views import *
from myapp.views import *
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('index/', viewfromjson, name='index'),
    path('',login_view, name='login'),
    path('register/', register_view, name='register'),
    path('home/', home, name='home'),
    path('att/', dashboard, name='attendance'),
    path('search/', search_employee, name='search_employee'),
    path('camera-list', camera_list, name='camera-list'),
    path('persons/search-by-date/', search_persons_by_date, name='search_persons_by_date'),
    path('sorted_person_data/', sorted_person_data, name='sorted_person_data'),
    path('persons/search-by-time/', search_persons_by_datetime, name='search_persons_by_time'),
    path('camera-details/', search_camera_details, name='search_camera_details'),
    path('assign-camera/', assign_camera_view, name='assign_camera'),


    # api
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('files/', UploadedFilesView.as_view(), name='uploaded-files'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    

