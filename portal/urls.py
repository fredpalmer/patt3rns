# coding=utf-8
from __future__ import unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = []

urlpatterns += (
    url(r"^(?P<view>[\w-]+)/$", views.PortalView.as_view(), name="portal"),
)
