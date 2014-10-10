import logging

logger = logging.getLogger(__name__)


# noinspection PyClassHasNoInit
class ModelFormMetaBase:
    abstract = True
    fields = "__all__"
    localized_fields = "__all__"
