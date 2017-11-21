from django.db import transaction
from rest_framework import mixins, response, status


class BulkCreateModelMixin(mixins.CreateModelMixin):
    """
    Either create a single or many model instances in bulk.
    """

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        bulk = isinstance(request.data, list)
        if bulk:
            serializers = []
            for data in request.data:
                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                serializers.append(serializer.data)
            return response.Response(serializers,
                                     status=status.HTTP_201_CREATED)
        else:
            return super(BulkCreateModelMixin, self).create(
                request, *args, **kwargs)
