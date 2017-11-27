from rest_framework import serializers
from django_fsm import get_available_user_FIELD_transitions


class FSMAvailableUserTransitionsField(serializers.ReadOnlyField):
    def __init__(self, *args, **kwargs):
        self.state_field = kwargs.pop('state_field', 'state')
        kwargs['source'] = '*'

        super(FSMAvailableUserTransitionsField, self).__init__(*args, **kwargs)

    def to_representation(self, obj):
        request = self.context.get('request', None)
        assert request is not None, "Pass `request` into serializer context"

        user = request.user

        state_model_field = obj.__class__._meta.get_field(self.state_field)
        available_transitions = get_available_user_FIELD_transitions(
            obj, user, state_model_field)

        return [
            transition.name
            for transition in available_transitions
            if transition.custom.get('viewset', True)
        ]
