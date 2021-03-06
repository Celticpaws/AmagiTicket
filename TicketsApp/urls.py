from django.conf.urls import include, url
from django.conf import settings
from . import views

urlpatterns = [
        url(r'^$', views.auth),
        url(r'^ini$', views.auth),
        url(r'^main$', views.main),
        url(r'^register$', views.register),
        url(r'^index$', views.index, name='index'),
        url(r'^personal/(?P<pk>[0-9]+)/$', views.personal, name='personal'),
        url(r'^group/(?P<pk2>[0-9]+)/(?P<pk1>[0-9]+)/$', views.group, name='group'),
        url(r'^ptasks$', views.ptasks, name='ptasks'),
        url(r'^users/(?P<pk>[0-9]+)/$',views.users, name='users'),
        url(r'^departments$',views.departments, name='departments'),
        url(r'^department/(?P<pk>[0-9]+)$',views.department_id),
        url(r'^user/(?P<pk>[0-9]+)$',views.users_id),
        url(r'^ticket/(?P<pk>[0-9]+)/$', views.ticket),
        url(r'^ticket_create/(?P<pk>[-\w]+)/$', views.ticket_create), 
        url(r'^ticket_edit/(?P<pk>[0-9]+)/$', views.ticket_edit), 
        url(r'^ticket_attach/(?P<pk>[0-9]+)/$', views.ticket_attach),
        url(r'^ticket_scale/(?P<pk>[0-9]+)/$', views.ticket_scale),
        url(r'^ticket_transfer/(?P<pk>[0-9]+)/$', views.ticket_transfer),
        url(r'^ticket_assign/(?P<pk>[0-9]+)/$', views.ticket_assign),
        url(r'^ticket_print/(?P<pk>[0-9]+)/$', views.ticket_print),
        url(r'^ticket_close/(?P<pk>[0-9]+)/$', views.ticket_close),           
        url(r'^auth/$', views.auth, name='auth'),
        url(r'^management/logout/$', 'django.contrib.auth.views.logout'),
       # url(r'accounts/login', views.auth, name="auth"),
    ]
