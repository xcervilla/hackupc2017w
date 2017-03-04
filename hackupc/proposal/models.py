from __future__ import unicode_literals

from model_utils.models import TimeStampedModel
from django.db import models
from hackupc.users.models import User
# Create your models here.


class Proposal(TimeStampedModel):
    title = models.TextField(blank=False, max_length=100)
    description = models.TextField(blank=False, max_length=2000)
    created_by = models.ForeignKey(User)


class ProposalImage(models.Model):
    image = models.ImageField(blank=False)
    proposal = models.ForeignKey(Proposal)


class ProposalVote(TimeStampedModel):
    user = models.ForeignKey(User)
    proposal = models.ForeignKey(Proposal)

    class Meta:
        unique_together = ("user", "proposal")
