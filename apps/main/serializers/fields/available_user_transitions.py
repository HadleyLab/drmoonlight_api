from rest_framework import serializers


class FSMAvailableUserTransitionsField(serializers.ReadOnlyField):
    def __init__(self, *args, **kwargs):
        self.state_field = kwargs.pop('state_field', 'state')
        kwargs['source'] = '*'

        super(FSMAvailableUserTransitionsField, self).__init__(*args, **kwargs)

    def to_representation(self, obj):
        request = self.context.get('request', None)
        assert request is not None, "Pass `request` into serializer context"

        user = request.user

        method = getattr(
            obj, 'get_available_user_{0}_transitions'.format(self.state_field))
        available_transitions = method(user)

        return [
            transition.name
            for transition in available_transitions
            if transition.custom.get('viewset', True)
        ]
