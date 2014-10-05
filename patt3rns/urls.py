""" Default urlconf for patt3rns """
import os
import sys

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView, CreateView, UpdateView, DeleteView, ListView, DetailView
from patt3rns.models import Habit

from patt3rns.sitemap import ProjectSitemap
from patt3rns.utils import URL_PATTERNS
from patt3rns.views import DashboardView
from portal.views import PortalView


def raise_error(request):
    """Simulates a server error"""
    import logging

    logger = logging.getLogger(__name__)
    logger.error("Test error log message")
    raise Exception("Test unhandled exception")


sitemaps = {
    "static": ProjectSitemap
}

urlpatterns = patterns(
    "",
    # Portal
    url(r"^$", PortalView.as_view(), name="home"),
    (r"portal/", include("portal.urls")),

    # Admin
    # (r"^grappelli/", include("grappelli.urls")),
    url(r"^manage/admin/doc/", include("django.contrib.admindocs.urls")),
    url(r"^manage/admin/", include(admin.site.urls)),

    # allauth urls and authentication urls
    # This overrides the allauth logout (which is just using the django.contrib.auth.views under the hood as well)
    url("^accounts/logout/$", "django.contrib.auth.views.logout_then_login", name="logout"),
    (r"^accounts/", include("allauth.urls")),

    # Handle some common urls for convenience
    ("^login/$", RedirectView.as_view(url=settings.LOGIN_URL)),
    ("^logout/$", RedirectView.as_view(url=settings.LOGOUT_URL)),

    # Upload Handler
    # url(r"^(?P<app>\w+)/(?P<model>\w+(-\w+)*)/(?P<pk>\d+)/(?P<field>\w+)/$", "patt3rns.views.upload_handler", name="upload-handler"),

    url(r"dashboard", DashboardView.as_view(), name="dashboard"),
    url(r"^habits/$", ListView.as_view(model=Habit), name="habit-list"),
    url(r"^habit/%(pk)s/$" % URL_PATTERNS, DetailView.as_view(model=Habit), name="habit-detail"),
    url(r"^habit/create/$", CreateView.as_view(model=Habit), name="habit-create"),
    url(r"^habit/update/%(pk)s/$" % URL_PATTERNS, UpdateView.as_view(model=Habit), name="habit-update"),
    url(r"^habit/delete/%(pk)s/$" % URL_PATTERNS, DeleteView.as_view(model=Habit, success_url=reverse_lazy("habit-list")), name="habit-delete"),


    (r"^sitemap\.xml$", "django.contrib.sitemaps.views.sitemap", {"sitemaps": sitemaps}),

    # Error handling testing
    url(r"^raise-error/", raise_error, name="raise-error"),
)

# We never want to expose the design playground on production
if settings.APP_ENV != "production":
    urlpatterns += patterns(
        "",
        url(r"^design/$", "patt3rns.views.design", name="design"),
        url(r"^design/(?P<view>.+)/$", "patt3rns.views.dispatch", name="design-dispatch"),
    )

# Allows us to run without DEBUG locally and still get files from MEDIA_ROOT
if settings.DEBUG or (len(sys.argv) > 0 and sys.argv[1] == "runserver"):
    urlpatterns += patterns(
        "",
        (r"^(?P<path>favicon.ico)$", "django.views.static.serve", {"document_root": os.path.join(settings.MEDIA_ROOT, "images"), "show_indexes": True}),
        (r"^m|media/(?P<path>.*)$", "django.views.static.serve", {"document_root": settings.STATIC_ROOT, "show_indexes": True}),
    )

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += patterns(
        "",
        url(r"^__debug__/", include(debug_toolbar.urls)),
    )
