from django.urls import re_path
from .views import memoryDetailView, dashboardView, addMemoryView, validateFiles
urlpatterns = [
    re_path(r'^dashboard/$', dashboardView, name='dashboard'),
    re_path(r'^memories/<int:pk>$', memoryDetailView, name='memory-detail'),
    re_path(r'^add-memories/$', addMemoryView, name='add-memories'),
    re_path(r'^validate-files/$', validateFiles, name='validate-files'),
]
