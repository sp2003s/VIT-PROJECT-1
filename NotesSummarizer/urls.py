from django.urls import path
import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('upload_file/', views.upload_file, name = 'upload_file'),
]