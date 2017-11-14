from copy import copy
import inspect

from django.core.exceptions import ImproperlyConfigured
from django.db import transaction

from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.serializers import Serializer, ValidationError

from django_fsm import (
    can_proceed, has_transition_perm, FSMFieldMixin, TransitionNotAllowed, )


def get_view_fn(name_):
    name = copy(name_)

    @transaction.atomic
    def fn(self, request, **kwargs):
        transition_args = []

        if self.get_serializer_class() != Serializer:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            transition_args = [serializer.validated_data]

        obj = self.get_object()
        transition = getattr(obj, name)

        if can_proceed(transition) and \
                has_transition_perm(transition, request.user):
            try:
                transition(*transition_args)
            except TransitionNotAllowed as err:
                raise ValidationError(str(err))
            obj.save()
            return Response(status=204)
        else:
            raise ValidationError(
                "Can't perform '{}' transition".format(name))

    return fn


def check_args(f, serializer_class):
    transition_argspec = inspect.getfullargspec(
        f.method)
    transition_argcount = len(transition_argspec.args)

    if transition_argcount == 1 and serializer_class:
        raise ImproperlyConfigured(
            "Transition '{0}' doesn't receive an additional argument "
            "but serializer is specified".format(f.name))

    if transition_argcount > 1 and not serializer_class:
        raise ImproperlyConfigured(
            "Transition '{0}' receives an additional argument "
            "but serializer is not specified".format(f.name))

    if transition_argcount > 2:
        raise ImproperlyConfigured(
            "Transition '{0}' receives arguments which "
            "can't be provided".format(f.name))


def add_transition_actions(*decorator_args, **decorator_kwargs):
    serializers = decorator_kwargs.get('serializers', {})

    def decorator(Klass):
        Model = Klass.queryset.model
        fsm_fields = [f.name for f in Model._meta.fields
                      if isinstance(f, FSMFieldMixin)]
        if len(fsm_fields) == 0:
            raise ImproperlyConfigured(
                "There is no FSM field at '{0}'".format(Model))

        if len(fsm_fields) > 1:
            raise ImproperlyConfigured(
                "There is more than one FSM field at '{0}'".format(Model))

        method_name = "get_all_{0}_transitions".format(fsm_fields[0])

        for f in getattr(Model, method_name)(Model()):
            # Skip methods which explicitly excluded via using `viewset=False`
            # in custom attr
            if not f.custom.get('viewset', True):
                continue

            serializer_class = serializers.get(f.name, None)
            check_args(f, serializer_class)

            if not serializer_class:
                # Use an empty serializer for the transition
                # without data argument
                serializer_class = Serializer

            setattr(Klass, f.name, detail_route(
                methods=['post'],
                # Skip permissions because transition has owns
                permission_classes=(),
                serializer_class=serializer_class)(get_view_fn(f.name)))
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
