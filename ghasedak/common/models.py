import uuid

from django.db import models
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _


class UniversalModel(models.Model):
    """Universal primary key mixin

    This mixin changes the primary key of a model to UUID field.
    Using UUID as primary key could help application scalability
    and could make migrating to microservice, or exporting or importing data easier,
    by using a universally unique identifier for object that without fear of collision.
    """
    id = models.UUIDField(_('universal unique id'), primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

    @property
    def serial(self) -> str:
        return f'{self.id.__str__().upper().split("-")[0]}'

    def __str__(self):
        return self.serial


class ActivatedModelManager(models.Manager):
    @property
    def actives(self) -> QuerySet:
        return self.get_queryset().filter(is_active=True)


class ActivatedModel(models.Model):
    """Active objects mixin

    This mixin add is_active field to the model
    which indicated the model active status.
    It also adds a queryset to support
    getting only active objects.
    """
    is_active = models.BooleanField(
        _('active'),
        default=True,
        db_index=True  # It's a common situation where we want to find active objects so indexing would be beneficial.
    )

    objects = ActivatedModelManager()

    class Meta:
        abstract = True


class TimestampedModel(models.Model):
    """Timestamp mixin

    This mixin adds a timestamp to model for create and update events
    """
    created = models.DateTimeField(_('created at'), auto_now_add=True, db_index=True)
    updated = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        abstract = True
