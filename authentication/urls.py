from django.urls import include, re_path
from .views import *
urlpatterns = [
    re_path(r'^$',home, name='home'),
    re_path(r'^signup/$', signup, name='signup'),
    re_path(r'^login/$',loginView,name='login'),
    re_path(r'^logout/$',logoutView,{'next_page':'login'},name='logout'),
    re_path(r'^account_activation_sent/$', account_activation_sent,
        name='account_activation_sent'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
]
