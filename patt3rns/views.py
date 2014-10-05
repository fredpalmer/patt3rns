import logging
import os

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.template.loader import select_template
from django.utils.safestring import mark_safe

from patt3rns.utils import sort_nicely

logger = logging.getLogger(__name__)


def can_view_design(u):
    result = False
    logger.debug("can_view_design => %s", settings.APP_ENV)
    if settings.APP_ENV == "dev":
        result = True
    # NOTE: customize to your liking, e.g.
    # elif settings.APP_ENV == "staging":
    # result = not u.is_anonymous()

    return result


@user_passes_test(can_view_design)
def dispatch(request, view):
    logger.debug("dispatch: view => %s, path => %s", view, request.path)
    template_name = "{0}.html".format(view)

    try:
        design_root_dirname = settings.DESIGNER_PLAYGROUND
        design_root_path = os.path.join(settings.TEMPLATE_DIRS[0], design_root_dirname)
        templates = [os.path.join(design_root_dirname, template_name)]
        listing = sort_nicely(os.listdir(design_root_path))
        for entry in listing:
            if os.path.isdir(os.path.join(design_root_path, entry)):
                templates.append(os.path.join(design_root_dirname, entry, template_name))
        selected_template = select_template(templates)
        response = render(request, selected_template.name, {"view": view, })
    except TemplateDoesNotExist:
        response = HttpResponseRedirect(reverse("design"))

    return response


@user_passes_test(can_view_design)
def design(request):
    """
    Simple response to iterate through templates in the designer's playground
    """

    def get_link(current_filename):
        current_filename, ext = os.path.splitext(current_filename)
        label = current_filename.replace("-", " ").replace("_", " ")
        label = label.title()
        link = "<a href=\"%(filename)s/\" title=\"%(label)s\">%(label)s</a>" % dict(filename=current_filename, label=label)
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
                current_tree.append(mark_safe(get_link(filename)))

        tree.append([mark_safe("<h1>%s</h1>" % os.path.basename(dir_path)), current_tree])

    logger.debug("%s indexed => %s", request.path, tree)
    return render(request, os.path.join(settings.DESIGNER_PLAYGROUND, "_index.html"), dict(tree=tree))
