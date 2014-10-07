import json

from django.conf import settings
from django.contrib.contenttypes.generic import GenericForeignKey, GenericRelation
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

    def get_default_queryset(self):
        """
            Unfiltered queryset (includes 'date_removed' objects).
        """
        return super(MetadataManager, self).get_queryset()

    def get_queryset(self):
        """
            Queryset which only contains active, non-removed objects.
        """
        return self.get_default_queryset().filter(date_removed__isnull=True)


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


class Action(BaseModel):
    description = patt3rns_fields.CharField(max_length=255, help_text=u"Should be in the form of <em>verb</em> or <em>verb at noun</em>, e.g.: <strong><em>jumped into the leaves</em></strong>")

    def __unicode__(self):
        return self.description


# TODO: should add auditing (e.g. reversion)
class Participant(BaseModel):
    first_name = patt3rns_fields.CharField(max_length=255)
    last_name = patt3rns_fields.CharField(max_length=255)
    date_born = patt3rns_fields.DateField()
    metadata = GenericRelation(Metadata)
    image = patt3rns_fields.ImageField(blank=True, null=True)
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    # edited_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __unicode__(self):
        return u"{} {}".format(self.first_name, self.last_name)


# TODO: should add auditing (e.g. reversion)
class Pattern(BaseModel):
    edited_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    notes = patt3rns_fields.TextField(blank=True)
    date_occurrence = patt3rns_fields.DateField(db_index=True)
    time_occurrence = patt3rns_fields.TimeField(null=True, blank=True)
    participant = models.ForeignKey(Participant)
    action = models.ForeignKey(Action)

    def __unicode__(self):
        return u"the instance where {} {} on {}".format(self.participant, self.action, self.date_occurrence)

