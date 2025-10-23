from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/sketch/', views.sketch_image, name='sketch_image'),
    path('api/images/', views.list_images, name='list_images'),
    path('api/images/<str:image_id>/', views.get_image, name='get_image'),
]
