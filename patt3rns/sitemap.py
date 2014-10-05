from django.core.urlresolvers import reverse
from django.contrib.sitemaps import Sitemap


class ProjectSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return [
            "home",
            "about",
            "terms-and-conditions",
            "privacy-policy",
            "press-info",
            "team",
            "faq"
        ]

    def location(self, item):
        if item == "home":
            return reverse(item)
        else:
            return reverse("portal", args=[item])
