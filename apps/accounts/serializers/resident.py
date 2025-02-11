from rest_framework import serializers

from apps.accounts.fields import MultipartM2MField, MultipartArrayField
from apps.accounts.models import Resident
from apps.accounts.models.mixins import AvatarFieldMixin
from .user import UserCreateSerializer


class ResidentSerializer(AvatarFieldMixin):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Resident
        exclude = ('password', )


class ResidentCreateSerializer(UserCreateSerializer):
    class Meta:
        model = Resident
        fields = ('pk', 'email', 'first_name', 'last_name',
                  'password', 'timezone', )


class ResidentUpdateSerializer(AvatarFieldMixin):
    specialities = MultipartM2MField(required=False)
    state_license_states = MultipartArrayField(required=False)

    class Meta:
        model = Resident
        fields = (
            # Required fields
            'pk', 'email', 'first_name', 'last_name', 'avatar',
            'residency_program', 'residency_years', 'specialities', 'timezone',

            # Not required fields
            'earliest_availability_for_shift', 'preferences_for_work_location',
            'state_license', 'state_license_states', 'federal_dea_active',
            'bls_acls_pals', 'active_permanent_residence_card_or_visa',
            'active_current_driver_license_or_passport', 'active_npi_number',
            'ecfmg', 'active_board_certificates', 'cv_link',

            # Notifications
            'notification_new_shifts',
            'notification_application_status_changing',
            'notification_new_messages',
        )
        extra_kwargs = {
            'residency_years': {'required': True, 'allow_null': False, },
            'specialities': {'required': True, 'allow_empty': False, },
        }

    def validate(self, attrs):
        attrs = super(ResidentUpdateSerializer, self).validate(attrs)

        if attrs.get('state_license', False) and \
                not attrs.get('state_license_states', []):
            raise serializers.ValidationError({
                'state_license_states': [
                    'You must choose at least one state where you '
                    'have state licence'
                ]
            })

        return attrs


class ResidentFillProfileSerializer(ResidentUpdateSerializer):
    class Meta(ResidentUpdateSerializer.Meta):
        fields = (
            # Required fields
            'residency_program', 'residency_years',
            'specialities',

            # Not required fields
            'earliest_availability_for_shift', 'preferences_for_work_location',
            'state_license', 'state_license_states', 'federal_dea_active',
            'bls_acls_pals', 'active_permanent_residence_card_or_visa',
            'active_current_driver_license_or_passport', 'active_npi_number',
            'ecfmg', 'active_board_certificates', 'cv_link',
        )
