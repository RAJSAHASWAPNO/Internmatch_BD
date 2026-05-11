from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self, *args, **kwargs):
        """Soft delete the object."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self, *args, **kwargs):
        """Permanently delete the object."""
        super().delete(*args, **kwargs)

    class Meta:
        abstract = True
