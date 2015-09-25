# coding=utf-8
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"pattern", views.PatternViewSet)

urlpatterns = [
    url(r"^", include(router.urls)),
    url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
