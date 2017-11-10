from rest_framework import serializers

from apps.accounts.models import Resident
from .user import UserCreateSerializer


class ResidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resident
        fields = ('pk', 'email', 'state', )


class ResidentCreateSerializer(UserCreateSerializer):
    class Meta:
        model = Resident
        fields = ('pk', 'email', 'first_name', 'last_name', 'password', )


class ResidentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resident
        fields = (
            # Required fields
            'pk', 'email', 'residency_program', 'residency_year',
            'specialities',

            # Not required fields
            'earliest_availability_for_shift', 'preferences_for_work_location',
            'state_license', 'state', 'federal_dea_active', 'bls_acls_pals',
            'active_permanent_residence_card_or_visa',
            'active_current_driver_license_or_passport', 'active_npi_number',
            'ecfmg', 'active_board_certificates',

            # Notifications
            'notification_new_shifts',
            'notification_application_status_changing',
            'notification_new_messages',
        )
        extra_kwargs = {
            'residency_program': {'required': True, },
            'residency_year': {'required': True, },
            'specialities': {'required': True, },
        }


class ResidentFillProfileSerializer(ResidentUpdateSerializer):
    class Meta(ResidentUpdateSerializer.Meta):
        fields = (
            # Required fields
            'residency_program', 'residency_year',
            'specialities',

            # Not required fields
            'earliest_availability_for_shift', 'preferences_for_work_location',
            'state_license', 'state', 'federal_dea_active', 'bls_acls_pals',
            'active_permanent_residence_card_or_visa',
            'active_current_driver_license_or_passport', 'active_npi_number',
            'ecfmg', 'active_board_certificates',
        )
