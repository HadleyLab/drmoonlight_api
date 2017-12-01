from django.core.management.base import BaseCommand
from dbmail.models import MailTemplate, MailBaseTemplate


class Command(BaseCommand):
    help = "Initialize email templates"

    def handle(self, **options):
        base_template, _ = MailBaseTemplate.objects.update_or_create(
            name="Main",
            defaults={
                'message': """
                <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
                    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
                <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
                <body>
                {{ content }}
                
                    
                <p>The {{ site_name }} team</p>
                </body>
                </html>
                """
            }
        )

        # Destination: account managers
        MailTemplate.objects.update_or_create(
            slug='resident_profile_filled',
            defaults={
                'name': 'Resident profile filled',
                'subject': 'New resident {{ resident.full_name }} filled profile',
                'message': """
                <p>
                    Hello!
                </p>
                <p></p>
                <p>
                    {{ resident.full_name }} is waiting for approving. Please review his profile
                and approve or reject him.
                </p>
                <p></p>
                <p>
                    <a href="{{ protocol }}://{{ domain }}/#/account-manager/detail/{{ resident.pk }}/">
                        Review resident on the site
                    </a>
                </p>
                """,
                'base': base_template,
            }
        )

        # Destination: resident
        MailTemplate.objects.update_or_create(
            slug='resident_approved',
            defaults={
                'name': 'Resident approved',
                'subject': 'You are approved',
                'message': """
                <p>
                    Hello {{ resident.full_name }}!
                </p>
                <p></p>
                <p>
                    You are successfully approved and now you can apply for a shifts.
                </p>
                <p></p>
                <p>
                    <a href="{{ protocol }}://{{ domain }}/#/resident/schedule/">
                        Go to the schedule
                    </a>
                </p>
                """,
                'base': base_template,
            }
        )

        # Destination: resident
        MailTemplate.objects.update_or_create(
            slug='resident_rejected',
            defaults={
                'name': 'Resident rejected',
                'subject': 'You are rejected',
                'message': """
                <p>
                    Hello {{ resident.full_name }}!
                </p>
                <p></p>
                <p>
                    You are rejected to be an approved resident. You can update your profile and our staff will consider your profile again. 
                </p>
                <p>
                    <a href="{{ protocol }}://{{ domain }}/#/resident/profile/">
                        Update profile
                    </a>
                </p>               
                """,
                'base': base_template,
            }
        )

        # Destination: resident
        MailTemplate.objects.update_or_create(
            slug='shift_created',
            defaults={
                'name': 'Shift created',
                'subject': 'A new suitable shift for you',
                'message': """
                <p>
                    Hello {{ resident.full_name }}!
                </p>
                <p></p>
                <p>
                    There is a new suitable shift for you was created right now.
                </p>
                <p>
                    <b>Location:</b> {{ shift.facility_name }} at {{ shift.department_name }}<br />
                    <b>Starts:</b> {{ shift.date_start }} <br />
                    <b>Ends:</b> {{ shift.date_end }} <br />
                    <b>Payment amount:</b> {{ shift.payment_amount }} {% if shift.payment_per_hour %}per hour{% endif %}<br />
                    {{ shift.description }}
                </p>
                <p>
                    <a href="{{ protocol }}://{{ domain }}/#/resident/messages/{{ shift.pk }}/">
                        Open the shift
                    </a>
                </p>               
                """,
                'base': base_template,
            }
        )

        # Destination: resident
        MailTemplate.objects.update_or_create(
            slug='shift_updated',
            defaults={
                'name': 'Shift updated',
                'subject': 'A shift was updated',
                'message': """
                <p>
                    Hello {{ resident.full_name }}!
                </p>
                <p></p>
                <p>
                    {% if is_applicant %}
                    The shift you applied for was changed.
                    {% else %}
                    Suitable shift for you was changed.
                    {% endif %}
                </p>
                <p>
                    <b>Location:</b> {{ shift.facility_name }} at {{ shift.department_name }}<br />
                    <b>Starts:</b> {{ shift.date_start }} <br />
                    <b>Ends:</b> {{ shift.date_end }} <br />
                    <b>Payment amount:</b> {{ shift.payment_amount }} {% if shift.payment_per_hour %}per hour{% endif %}<br />
                    {{ shift.description }}
                </p>
                <p>
                    <a href="{{ protocol }}://{{ domain }}/#/resident/messages/{{ shift.pk }}/">
                        Open the shift
                    </a>
                </p>               
                """,
                'base': base_template,
            }
        )

        # Destination: resident
        MailTemplate.objects.update_or_create(
            slug='shift_deleted',
            defaults={
                'name': 'Shift deleted',
                'subject': 'A shift was deleted',
                'message': """
                <p>
                    Hello {{ resident.full_name }}!
                </p>
                <p></p>
                The shift for {{ shift.facility_name }} at {{ shift.department_name }} which will start at {{ shift.date_start }} was deleted.    
                """,
                'base': base_template,
            }
        )

        # Destination: resident or scheduler
        MailTemplate.objects.update_or_create(
            slug='message_created',
            defaults={
                'name': 'Message created',
                'subject': 'You received new message from {{ source.full_name }}',
                'message': """
                <p>
                    Hello {{ destination.full_name }}!
                </p>
                <p></p>
                <p>
                    You received new message from {{ source.full_name }}:<br />
                    {{ text }}
                </p>
                <p>
                    <b>Shift details:</b>
                </p>
                <p>
                    <b>Location:</b> {{ shift.facility_name }} at {{ shift.department_name }}<br />
                    <b>Starts:</b> {{ shift.date_start }} <br />
                    <b>Ends:</b> {{ shift.date_end }} <br />
                    <b>Payment amount:</b> {{ shift.payment_amount }} {% if shift.payment_per_hour %}per hour{% endif %}<br />
                    {{ shift.description }}
                </p>
                <p>
                    <a href="{{ protocol }}://{{ domain }}/#/{{ destination.role }}/messages/{{ shift.pk }}/discuss/{{ application.pk }}/">
                        Open message dialog
                    </a>
                </p>               
                """,
                'base': base_template,
            }
        )

        MailTemplate.clean_cache()
