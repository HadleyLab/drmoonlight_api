from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from django_fsm import FSMField, transition

from rest_framework import serializers, viewsets

from ..viewsets import add_transition_actions


class Simple(models.Model):
    title = models.CharField()


class SimpleModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Simple
        fields = ('title', )


class SimpleModelViewSet(viewsets.GenericViewSet):
    queryset = Simple.objects.none()
    serializer_class = SimpleModelSerializers()


class TwoFSMField(models.Model):
    state_one = FSMField(default='a')
    state_two = FSMField(default='b')


class TwoFSMFieldSerializers(serializers.ModelSerializer):
    class Meta:
        model = TwoFSMField
        fields = (
            'state_on',
            'state_two', )


class TwoFSMFieldViewSet(viewsets.GenericViewSet):
    queryset = TwoFSMField.objects.all()
    serializer_class = TwoFSMFieldSerializers()


class NormalFSM(models.Model):
    state = FSMField(default='a')

    @transition(field=state, source='a', target='b')
    def a_to_b(self):
        pass

    @transition(field=state, source='b', target='c')
    def b_to_c(self):
        pass

    @transition(field=state, source='a', target='c')
    def a_to_c(self):
        pass

    @transition(field=state, source='c', target='d', custom={
        'viewset': False})
    def c_to_d(self):
        pass


class NormalFSMModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = NormalFSM
        fields = ('state', )


class NormalFSMModelViewSet(viewsets.GenericViewSet):
    queryset = NormalFSM.objects.none()
    serializer_class = NormalFSMModelSerializers()


class AddTransitionActionsDecorator(TestCase):
    def test_that_you_cant_wrap_non_fsm_viewset(self):
        with self.assertRaises(ImproperlyConfigured):
            add_transition_actions(SimpleModelViewSet)

    def test_that_you_cant_wrap_fsm_viewset_with_two_fields(self):
        with self.assertRaises(ImproperlyConfigured):
            add_transition_actions(TwoFSMFieldViewSet)

    def test_that_for_viewset_with_exactly_one_fsm_action_creates(self):
        NewViewSet = add_transition_actions(NormalFSMModelViewSet)
        self.assertTrue(callable(NewViewSet.a_to_b))
        self.assertTrue(callable(NewViewSet.b_to_c))
        self.assertTrue(callable(NewViewSet.a_to_c))
        self.assertFalse(hasattr(NewViewSet, 'c_to_d'))

    def test_that_you_can_specify_custom_serializers(self):
        NewViewSet = add_transition_actions(
            serializers={'a_to_b': serializers.Serializer}
        )(NormalFSMModelViewSet)
        self.assertTrue(callable(NewViewSet.a_to_b))
        self.assertTrue(callable(NewViewSet.b_to_c))
        self.assertTrue(callable(NewViewSet.a_to_c))
