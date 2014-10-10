import json

from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models

from patt3rns.models import fields as patt3rns_fields


class BaseModel(models.Model):
    uuid = patt3rns_fields.UuidField(editable=False)
    date_created = patt3rns_fields.CreationDateTimeField()
    date_modified = patt3rns_fields.ModificationDateTimeField()

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # Make sure auto_now fields such as date_modified get automatically appended to any partial object saves
        if update_fields:
            update_fields = list(set(list(update_fields) + ["date_modified"]))
        super(BaseModel, self).save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def get_absolute_url(self):
        return reverse("object-detail", kwargs=dict(model=self.__class__.__name__.lower(), pk=self.pk))


class MetadataManager(models.Manager):
    """
    Serves metadata as a dict (useful for templates).
    """

    def __delitem__(self, key):
        try:
            metadata = self.instance.metadata.get(name=key)
            metadata.delete()
        except Metadata.DoesNotExist:
            pass

    def __getitem__(self, key):
        try:
            for item in self.get_queryset().filter(name=key).order_by("-date_created"):
                return item.value
        except Metadata.DoesNotExist:
            return None

    def __setitem__(self, key, value):
        try:
            metadata = self.instance.metadata.get(name=key)
            metadata.value = value
            metadata.save()
        except Metadata.DoesNotExist:
            self.instance.metadata.create(name=key, value=value)
        except Metadata.MultipleObjectsReturned:
            metadata = self.instance.metadata.filter(name=key).order_by("-date_created")[0]
            metadata.value = value
            metadata.save()

    def __contains__(self, key):
        try:
            return self[key] is not None
        except IndexError:
            return False

    def iterkeys(self):
        for metadata in self.get_queryset().order_by("name"):
            yield metadata.name

    def keys(self):
        return list(self.iterkeys())

    def itervalues(self):
        """
        Zip iterkeys and itervalues
        """
        for metadata in self.get_queryset().order_by("name"):
            yield metadata.value

    def values(self):
        return list(self.itervalues())

    def iteritems(self):
        for metadata in self.get_queryset().order_by('name'):
            yield metadata.name, metadata.value

    def items(self):
        return list(self.iteritems())


class Metadata(BaseModel):
    key = patt3rns_fields.CharField(max_length=100, db_index=True)
    value = patt3rns_fields.TextField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    objects = MetadataManager()

    class Meta:
        verbose_name_plural = u"Metadata"

    def __unicode__(self):
        return u"%s => %s" % (self.name, self.value)

    def as_tuple(self):
        return self.name, self.value

    def __repr__(self):
        return json.dumps(dict(
            name=self.name,
            value=self.value,
            content_type=self.content_type.name,
            object_id=self.object_id,
        ))
