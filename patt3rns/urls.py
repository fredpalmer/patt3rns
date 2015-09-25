""" Default urlconf for patt3rns """
# coding=utf-8
from __future__ import unicode_literals
import os
import logging
import sys

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView

from .sitemap import ProjectSitemap
from .utils import URL_PATTERNS
from . import views
from portal.views import PortalView

logger = logging.getLogger(__name__)


def raise_error(request):
    """Simulates a server error"""
    logger.error("Test error log message => %s", request.path)
    raise Exception("Test unhandled exception")


sitemaps = {
    "static": ProjectSitemap
}

primary_urls = [
    # Portal
    url(r"^$", PortalView.as_view(), name="home"),
    url(r"portal/", include("portal.urls")),

    # Api
    url(r"api/", include("api.urls")),

    # Organization
    url(r"org/", include("organization.urls")),

    # Admin
    # (r"^grappelli/", include("grappelli.urls")),
    url(r"^manage/admin/doc/", include("django.contrib.admindocs.urls")),
    url(r"^manage/admin/", include(admin.site.urls)),

    # allauth urls and authentication urls
    # This overrides the allauth logout (which is just using the django.contrib.auth.views under the hood as well)
    url("^accounts/logout/$", "django.contrib.auth.views.logout_then_login", name="logout"),
    url(r"^accounts/", include("allauth.urls")),

    # Handle some common urls for convenience
    url("^login/$", RedirectView.as_view(url=settings.LOGIN_URL)),
    url("^logout/$", RedirectView.as_view(url=settings.LOGOUT_URL)),

    # Upload Handler
    # url(r"^(?P<app>\w+)/(?P<model>\w+(-\w+)*)/(?P<pk>\d+)/(?P<field>\w+)/$", "patt3rns.views.upload_handler", name="upload-handler"),

    url(r"dashboard/", views.DashboardView.as_view(), name="dashboard"),
    url(r"schedule/", views.ScheduleView.as_view(), name="schedule"),
    url(r"^o/list/%(model)s/$" % URL_PATTERNS, views.ObjectListView.as_view(), name="object-list"),
    url(r"^o/detail/%(model)s/%(pk)s/$" % URL_PATTERNS, views.ObjectDetailView.as_view(), name="object-detail"),
    url(r"^o/create/%(model)s/$" % URL_PATTERNS, views.ObjectCreateView.as_view(), name="object-create"),
    url(r"^o/update/%(model)s/%(pk)s/$" % URL_PATTERNS, views.ObjectUpdateView.as_view(), name="object-update"),
    url(r"^o/delete/%(model)s/%(pk)s/$" % URL_PATTERNS, views.ObjectDeleteView.as_view(), name="object-delete"),

    url(r"^sitemap\.xml$", "django.contrib.sitemaps.views.sitemap", {"sitemaps": sitemaps}),

    # Error handling testing
    url(r"^raise-error/", raise_error, name="raise-error"),
]

additional_urls = []

# We never want to expose the design playground other than dev
if settings.APP_ENV == "dev":
    additional_urls += [
        url(r"^design/$", views.DesignIndexView.as_view(), name="design"),
        url(r"^design/(?P<view>models/.+)/$", views.DesignModelView.as_view(), name="design-model"),
        url(r"^design/(?P<view>.+)/$", views.DesignDispatchView.as_view(), name="design-dispatch"),
    ]

# Allows us to run without DEBUG locally and still get files from MEDIA_ROOT
if settings.DEBUG or (len(sys.argv) > 0 and sys.argv[1] == "runserver"):
    additional_urls += [
        url(r"^(?P<path>favicon.ico)$", "django.views.static.serve", {"document_root": os.path.join(settings.MEDIA_ROOT, "images"), "show_indexes": True}),
        url(r"^m|media/(?P<path>.*)$", "django.views.static.serve", {"document_root": settings.STATIC_ROOT, "show_indexes": True}),
    ]

if settings.DEBUG:
    import debug_toolbar

    additional_urls += [
        url(r"^__debug__/", include(debug_toolbar.urls)),
    ]
    try:
        import debug_toolbar

        logger.warning("Allowing Django Debug Toolbar urls...")
        additional_urls += [
            url(r"^__debug__/", include(debug_toolbar.urls)),
        ]
    except ImportError:
        logger.warning("Django debug toolbar is not setup properly.  Make sure its installed...")

urlpatterns = primary_urls + additional_urls
