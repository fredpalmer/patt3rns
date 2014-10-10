import logging
from django.conf import settings

from django.db import models
from django.contrib.contenttypes.generic import GenericRelation

from patt3rns import models as patt3rns_models

logger = logging.getLogger(__name__)


class Action(patt3rns_models.BaseModel):
    description = patt3rns_models.CharField(max_length=255, help_text=u"Should be in the form of <em>verb</em> or <em>verb at noun</em>, e.g.: <strong><em>jumped into the leaves</em></strong>")

    def __unicode__(self):
        return self.description


# TODO: should add auditing (e.g. reversion)
class Participant(patt3rns_models.BaseModel):
    first_name = patt3rns_models.CharField(max_length=255)
    last_name = patt3rns_models.CharField(max_length=255)
    date_born = models.DateField(blank=True, null=True)
    metadata = GenericRelation(patt3rns_models.Metadata)
    image = patt3rns_models.ImageField(blank=True, null=True)
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    # edited_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __unicode__(self):
        return u"{} {}".format(self.first_name, self.last_name)


# TODO: should add auditing (e.g. reversion)
class Pattern(patt3rns_models.BaseModel):
    edited_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    notes = patt3rns_models.TextField(blank=True)
    date_occurrence = patt3rns_models.DateField(db_index=True)
    time_occurrence = patt3rns_models.TimeField(null=True, blank=True)
    participant = models.ForeignKey(Participant)
    action = models.ForeignKey(Action)

    def __unicode__(self):
        return u"the instance where {} {} on {}".format(self.participant, self.action, self.date_occurrence)
