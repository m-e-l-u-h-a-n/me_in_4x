from django.urls import re_path
from .views import memoryDetailView,dashboardView
urlpatterns = [
    re_path(r'^dashboard/$',dashboardView,name= 'dashboard'),
    re_path(r'^memories/<int:pk>$',memoryDetailView,name='memory-detail'),
]