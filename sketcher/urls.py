from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/sketch/', views.sketch_image, name='sketch_image'),
    path('api/images/', views.list_images, name='list_images'),
]
