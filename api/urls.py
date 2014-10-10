from django.conf.urls import url, include, patterns
from rest_framework.routers import DefaultRouter

from api import views


router = DefaultRouter()
router.register(r"pattern", views.PatternViewSet)
urlpatterns = router.urls

# urlpatterns = format_suffix_patterns(urlpatterns)

# urlpatterns = []

urlpatterns += patterns(
    "",
    # url("^$", include(router.urls)),
    url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),
)

