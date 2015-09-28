# coding=utf-8
from __future__ import unicode_literals
import inspect
import logging
import os
import uuid

from django.db import models
from django.utils.timezone import now as datetime_now

logger = logging.getLogger(__name__)


class UuidVersionError(Exception):
    pass


class UuidField(models.CharField):
    """
    By default uses UUID version 4 (generate from host ID, sequence number and current time)

    The field support all uuid versions which are natively supported by the uuid python module.
    For more information see: http://docs.python.org/lib/module-uuid.html
    """

    def __init__(self, verbose_name=None, name=None, auto=True, version=1, node=None, clock_seq=None, namespace=None, **kwargs):
        kwargs["max_length"] = 36
        if auto:
            self.empty_strings_allowed = False
            kwargs["blank"] = True
            kwargs.setdefault("editable", False)
        self.auto = auto
        self.version = version
        if version == 1:
            self.node, self.clock_seq = node, clock_seq
        elif version == 3 or version == 5:
            self.namespace, self.name = namespace, name
        super(UuidField, self).__init__(verbose_name=verbose_name, name=name, **kwargs)

    def get_internal_type(self):
        return models.CharField.__name__

    # noinspection PyProtectedMember
    def contribute_to_class(self, cls, name, virtual_only=False):
        if self.primary_key:
            assert not cls._meta.has_auto_field, "A model can't have more than one AutoField: %s %s %s; have %s" % (
                self, cls, name, cls._meta.auto_field
            )
            super(UuidField, self).contribute_to_class(cls, name)
            cls._meta.has_auto_field = True
            cls._meta.auto_field = self
        else:
            super(UuidField, self).contribute_to_class(cls, name)

    def create_uuid(self):
        if not self.version or self.version == 4:
            return uuid.uuid4()
        elif self.version == 1:
            return uuid.uuid1(self.node, self.clock_seq)
        elif self.version == 2:
            raise UuidVersionError("UUID version 2 is not supported.")
        elif self.version == 3:
            return uuid.uuid3(self.namespace, self.name)
        elif self.version == 5:
            return uuid.uuid5(self.namespace, self.name)
        else:
            raise UuidVersionError("UUID version %s is not valid." % self.version)

    def pre_save(self, model_instance, add):
        value = super(UuidField, self).pre_save(model_instance, add)
        if self.auto and add and value is None:
            value = unicode(self.create_uuid())
            setattr(model_instance, self.attname, value)
            return value
        else:
            if self.auto and not value:
                value = unicode(self.create_uuid())
                setattr(model_instance, self.attname, value)
        return value

    def formfield(self, **kwargs):
        if self.auto:
            return None
        super(UuidField, self).formfield(**kwargs)


class CreationDateTimeField(models.DateTimeField):
    """
    By default, sets editable=False, blank=True, default=datetime.now
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("editable", False)
        kwargs.setdefault("blank", True)
        kwargs.setdefault("default", datetime_now)
        super(CreationDateTimeField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "DateTimeField"


class ModificationDateTimeField(CreationDateTimeField):
    """
    By default, sets editable=False, blank=True, default=datetime.now
    Sets value to datetime.now() on each save of the model.
    """

    def pre_save(self, model, add):
        value = datetime_now()
        setattr(model, self.attname, value)
        return value

    def get_internal_type(self):
        return "DateTimeField"


class Choice(object):
    """
    Model Choice metaclass from http://tomforb.es/using-python-metaclasses-to-make-awesome-django-model-field-choices
    """

    # noinspection PyPep8Naming
    class __metaclass__(type):
        # noinspection PyMethodParameters,PyMissingConstructor,PyUnusedLocal
        def __init__(self, *args, **kwargs):
            self._data = []
            for name, value in inspect.getmembers(self):
                if not name.startswith("_") and not inspect.ismethod(value):
                    if isinstance(value, tuple) and len(value) > 1:
                        data = value
                    else:
                        pieces = [x.capitalize() for x in name.split("_")]
                        data = (value, " ".join(pieces))
                    self._data.append(data)
                    setattr(self, name, data[0])

            self._hash = dict(self._data)

        def __iter__(self):
            for value, data in self._data:
                yield (value, data)

    # noinspection PyMethodParameters
    @classmethod
    def get_value(self, key):
        # noinspection PyUnresolvedReferences
        return self._hash[key]


def content_filename(instance, filename):
    """
    instance:   An instance of the model where the FileField is defined. More specifically,
                this is the particular instance where the current file is being attached.
                In most cases, this object will not have been saved to the database yet,
                so if it uses the default AutoField, it might not yet have a value for its primary key field.

    filename    The filename that was originally given to the file. This may or may not be taken
                into account when determining the final destination path.
    """
    klass_name = instance.__class__.__name__
    instance.filename = filename
    uuid_part = str(uuid.uuid4())
    extension = os.path.splitext(filename)[1]
    generated_name = os.path.join("uploads", klass_name, uuid_part + extension).lower()
    logger.debug(u"Generating file name for \"%s\" to be uploaded as => %s", filename, generated_name)
    return generated_name


class FileField(models.FileField):
    def __init__(self, verbose_name=None, name=None, upload_to=content_filename, storage=None, **kwargs):
        super(FileField, self).__init__(verbose_name=verbose_name, name=name, upload_to=upload_to, storage=storage, **kwargs)


class ImageField(models.ImageField):
    def __init__(self, verbose_name=None, name=None, width_field=None, height_field=None, upload_to=content_filename, **kwargs):
        super(ImageField, self).__init__(verbose_name=verbose_name,
                                         name=name,
                                         width_field=width_field,
                                         height_field=height_field,
                                         upload_to=upload_to,
                                         **kwargs)


class CharField(models.CharField):
    __metaclass__ = models.SubfieldBase

    def clean(self, value, model_instance):
        if hasattr(value, "strip"):
            value = value.strip()
        return super(CharField, self).clean(value=value, model_instance=model_instance)

    def formfield(self, **kwargs):
        from patt3rns import forms as patt3rns_forms

        return super(CharField, self).formfield(form_class=patt3rns_forms.CharField, **kwargs)


class TextField(models.TextField):
    __metaclass__ = models.SubfieldBase

    def formfield(self, **kwargs):
        from patt3rns import forms as patt3rns_forms

        return super(TextField, self).formfield(form_class=patt3rns_forms.CharField, **kwargs)


class DateField(models.DateField):
    __metaclass__ = models.SubfieldBase

    def formfield(self, **kwargs):
        from patt3rns import forms as patt3rns_forms

        return super(DateField, self).formfield(form_class=patt3rns_forms.DateField, **kwargs)


class DateTimeField(models.DateTimeField):
    __metaclass__ = models.SubfieldBase

    def formfield(self, **kwargs):
        from patt3rns import forms as patt3rns_forms

        return super(DateTimeField, self).formfield(form_class=patt3rns_forms.DateTimeField, **kwargs)


class TimeField(models.TimeField):
    __metaclass__ = models.SubfieldBase

    def formfield(self, **kwargs):
        from patt3rns import forms as patt3rns_forms

        return super(TimeField, self).formfield(form_class=patt3rns_forms.TimeField, **kwargs)
