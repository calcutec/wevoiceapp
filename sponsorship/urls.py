from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.url_redirect, name='url_redirect'),
    url(r'^sponsorship/$', views.sponsorship, name='sponsorship'),
    url(r'^sponsorship-login/$', views.sponsorship_login, name='sponsorship_login')
]