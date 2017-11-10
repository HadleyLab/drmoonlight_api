from copy import copy
from functools import wraps

from django.core.exceptions import ImproperlyConfigured
from django.db import transaction

from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.serializers import Serializer, ValidationError

from django_fsm import (
    can_proceed, has_transition_perm, FSMFieldMixin, TransitionNotAllowed, )


def add_transition_actions(*decorator_args, **decorator_kwargs):
    serializers = decorator_kwargs.get('serializers', {})

    def decorator(Klass):
        Model = Klass.queryset.model
        fsm_fields = [f.name for f in Model._meta.fields
                      if isinstance(f, FSMFieldMixin)]
        if len(fsm_fields) == 0:
            raise ImproperlyConfigured(
                "There is no FSM field at {0}".format(Model))

        if len(fsm_fields) > 1:
            raise ImproperlyConfigured(
                "There is more than one FSM field at {0}".format(Model))

        method_name = "get_all_{0}_transitions".format(fsm_fields[0])

        for f in getattr(Model, method_name)(Model()):
            # Skip methods which explicitly excluded via using `viewset=False`
            # in custom attr
            if not f.custom.get('viewset', True):
                continue

            def get_fn(name_):
                name = copy(name_)

                @transaction.atomic
                def fn(self, request, **kwargs):
                    args = self.get_serializer(data=request.data)
                    args.is_valid(raise_exception=True)
                    obj = self.get_object()
                    transition = getattr(obj, name)
                    if can_proceed(transition) and \
                            has_transition_perm(transition, request.user):
                        try:
                            transition(**args.validated_data)
                        except TransitionNotAllowed as err:
                            raise ValidationError(str(err))
                        obj.save()
                        return Response(status=204)
                    else:
                        raise ValidationError(
                            "You cant perform '{}' transition".format(name))
                return fn

            serializer_class = serializers.get(f.name, Serializer)

            setattr(Klass, f.name, detail_route(
                methods=['post'],
                # Skip permissions because transition has owns
                permission_classes=(),
                serializer_class=serializer_class)(get_fn(f.name)))
        return Klass

    # Add an ability to use decorator without arguments
    # For example:
    # @add_transition_actions
    # class MyViewSet:
    # ...
    if len(decorator_args) == 1 and callable(decorator_args[0]) and \
            not decorator_kwargs:
        return decorator(decorator_args[0])

    return decorator
