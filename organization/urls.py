from django.conf.urls import url, patterns
from organization import views

urlpatterns = patterns(
    "",
    url(ur"$^", views.IdentityHome.as_view(), name="organization-home")
)
