from django.conf.urls import url
from portal.views import PortalView

urlpatterns = []

urlpatterns += (
    url(r"^(?P<view>[\w-]+)/$", PortalView.as_view(), name="portal"),
)
