import logging
import os

from django.apps import apps
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, TemplateView, View
from django.views.generic.base import ContextMixin
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.detail import SingleObjectTemplateResponseMixin

from patt3rns.utils import sort_nicely


logger = logging.getLogger(__name__)


def can_view_design(user):
    result = False
    logger.debug("can_view_design => %s with user => %s", settings.APP_ENV, user)
    if settings.APP_ENV == "dev":
        result = True
    # NOTE: customize to your liking, e.g.
    # elif settings.APP_ENV == "staging":
    # result = not u.is_anonymous()

    return result


class DesignDispatchView(TemplateView):
    """
    Simple view for handling requests in the designer's playground
    """
    def get_template_names(self):
        view = self.kwargs.get("view")
        design_template_name = "{}.html".format(view)
        design_root_dirname = settings.DESIGNER_PLAYGROUND
        design_root_path = os.path.join(settings.TEMPLATE_DIRS[0], design_root_dirname)
        templates = [os.path.join(design_root_dirname, design_template_name)]
        listing = sort_nicely(os.listdir(design_root_path))
        for entry in listing:
            if os.path.isdir(os.path.join(design_root_path, entry)):
                templates.append(os.path.join(design_root_dirname, entry, design_template_name))
        logger.debug("%s::get_template_names: path => %s, templates => %s", self.__class__.__name__, self.request.path, templates)
        return templates

    def get_context_data(self, **kwargs):
        return super(DesignDispatchView, self).get_context_data(**kwargs)

    @method_decorator(user_passes_test(can_view_design))
    def get(self, request, *args, **kwargs):
        return super(DesignDispatchView, self).get(request, *args, **kwargs)


class DesignIndexView(TemplateView):
    """
    Simple view to iterate through templates in the designer's playground
    """
    # noinspection PyUnresolvedReferences
    template_name = os.path.join(settings.DESIGNER_PLAYGROUND, "_index.html")

    def get_context_data(self, **kwargs):
        context = super(DesignIndexView, self).get_context_data(**kwargs)

        def massage_label(label):
            label = label.replace("-", " ").replace("_", " ")
            label = label.title()
            return label

        def get_link(current_filename, current_path=None):
            current_filename, ext = os.path.splitext(current_filename)
            label = massage_label(current_filename)
            if current_path:
                current_filename = os.path.join(current_path, current_filename)
            link = "<a href=\"{filename}/\" title=\"{label}\">{label}</a>".format(filename=current_filename, label=label)
            return link

        design_root_dirname = settings.DESIGNER_PLAYGROUND
        design_root_path = os.path.join(settings.TEMPLATE_DIRS[0], design_root_dirname)
        tree = []
        for dir_path, dir_names, filenames in os.walk(design_root_path):
            logger.debug("dir_path => %s, dir_names => %s, filenames => %s", dir_path, dir_names, filenames)
            filenames.sort()
            current_tree = []
            for filename in filenames:
                if not (filename.startswith(".") or filename.startswith("_")):
                    base_dir_path = os.path.basename(dir_path)
                    if base_dir_path == design_root_dirname:
                        base_dir_path = None
                    current_tree.append(mark_safe(get_link(filename, base_dir_path)))

            dir_label = massage_label(os.path.basename(dir_path))
            tree.append([mark_safe("<h1>{}</h1>".format(dir_label)), current_tree])

        context["tree"] = tree
        logger.debug("%s::get_context_data: path => %s, context => %s", self.__class__.__name__, self.request.path, context)
        return context

    @method_decorator(user_passes_test(can_view_design))
    def get(self, request, *args, **kwargs):
        return super(DesignIndexView, self).get(request, *args, **kwargs)


class ScheduleView(TemplateView):
    template_name = "patt3rns/schedule.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ScheduleView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ScheduleView, self).get_context_data(**kwargs)
        context["objects"] = ["action", "participant", "pattern"]
        return context


class DashboardView(TemplateView):
    template_name = "patt3rns/dashboard.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DashboardView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context["objects"] = ["action", "participant", "pattern"]
        return context


class GenericSingleObjectTemplateResponseMixin(SingleObjectTemplateResponseMixin):
    """
    Mixin for responding with a template and a single object.
    """
    model = None
    object = None

    def get_template_names(self):
        """
        Return a list of template names to be used for the request.
        """
        template_names = super(GenericSingleObjectTemplateResponseMixin, self).get_template_names()

        if isinstance(self.object, models.Model):
            # noinspection PyProtectedMember
            template_names.append("{}/{}{}.html".format(self.object._meta.app_label, "object", self.template_name_suffix))
        elif hasattr(self, "model") and self.model is not None and issubclass(self.model, models.Model):
            # noinspection PyProtectedMember
            template_names.append("{}/{}{}.html".format(self.model._meta.app_label, "object", self.template_name_suffix))

        logger.debug("%s::get_template_names => %s", self.__class__.__name__, template_names)
        return template_names


class SingleObjectViewBase(TemplateResponseMixin, ContextMixin, View):
    """
    This class essentially serves the same purpose as a `django.views.generic.TemplateView` except we do not want to define
    any methods to dispatch to.  That's the responsibility of any subclasses.
    """

    def get_context_data(self, **kwargs):
        context = super(SingleObjectViewBase, self).get_context_data(**kwargs)
        # Add the meta of the model to the context - variables that start with underscore are not available
        # noinspection PyProtectedMember
        context["meta"] = self.model._meta
        logger.debug("%s::get_context_data => %s", self.__class__.__name__, context)
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        model = kwargs.get("model")
        for app_config in apps.get_app_configs():
            try:
                model_class = app_config.get_model(model)
            except LookupError:
                pass
            else:
                # noinspection PyAttributeOutsideInit
                self.model = model_class
                break

        if not self.model:
            raise ImproperlyConfigured("Could not find model => {}".format(model))

        return super(SingleObjectViewBase, self).dispatch(request, *args, **kwargs)


class ObjectCreateView(GenericSingleObjectTemplateResponseMixin, SingleObjectViewBase, CreateView):
    template_name_suffix = "-form"


class ObjectDeleteView(GenericSingleObjectTemplateResponseMixin, SingleObjectViewBase, DeleteView):
    template_name_suffix = "-confirm-delete"

    def get_success_url(self):
        return reverse("object-list", kwargs=dict(model=self.kwargs.get("model")))


class ObjectListView(SingleObjectViewBase, ListView):
    template_name_suffix = "-list"

    def get_template_names(self):
        """
        Return a list of template names to be used for the request.
        """
        templates_names = super(ObjectListView, self).get_template_names()
        if hasattr(self.object_list, "model"):
            # noinspection PyProtectedMember
            opts = self.object_list.model._meta
            templates_names.append("{}/{}{}.html".format(opts.app_label, "object", self.template_name_suffix))
        return templates_names


class ObjectDetailView(GenericSingleObjectTemplateResponseMixin, SingleObjectViewBase, DetailView):
    template_name_suffix = "-detail"


class ObjectUpdateView(GenericSingleObjectTemplateResponseMixin, SingleObjectViewBase, UpdateView):
    template_name_suffix = "-form"

