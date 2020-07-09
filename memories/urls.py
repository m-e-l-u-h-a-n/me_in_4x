from django.urls import re_path
from .views import memoryDetailView,dashboardView,addMemoryView
urlpatterns = [
    re_path(r'^dashboard/$',dashboardView,name= 'dashboard'),
    re_path(r'^memories/<int:pk>$',memoryDetailView,name='memory-detail'),
    re_path(r'^add-memories$',addMemoryView,name='add-memories')
]