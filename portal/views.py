from django.views.generic import TemplateView


class PortalView(TemplateView):
    template_name = "index.html"

    def get_template_names(self):
        template_names = super(PortalView, self).get_template_names()
        section = self.kwargs.get("view")
        if section:
            template_names.insert(0, "portal/{}.html".format(section))
        return template_names

