from django.conf.urls import include, url
from . import views

urlpatterns = [
        url(r'^$', views.auth),
        url(r'^ini$', views.auth),
        url(r'^main$', views.main),
        url(r'^register$', views.register),
        url(r'^index$', views.index, name='index'),
        url(r'^solicitudp$', views.solicitudp, name='solicitudp'),
        url(r'^solicitudg$', views.solicitudg, name='solicitudg'),
        url(r'^incidentp$', views.incidentp, name='incidentp'),
        url(r'^incidentg$', views.incidentg, name='incidentg'),
        url(r'^ticket/(?P<pk>[0-9]+)/$', views.ticket),
        url(r'^auth/$', views.auth, name='auth'),
        url(r'^management/logout/$', 'django.contrib.auth.views.logout'),
       # url(r'accounts/login', views.auth, name="auth"),
    ]