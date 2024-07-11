from django.db import models
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor


class RepliesForward(ForwardManyToOneDescriptor):
    def get_queryset(self, **hints):
        related_model = self.field.remote_field.model
        return related_model.custom.db_manager(hints=hints).all()


class RepliesForeignKey(models.ForeignKey):
    forward_related_accessor_class = RepliesForward
