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
                    <a href="{{ protocol }}://{{ domain }}/#/account-manager/detail/{{ resident.pk }}">
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
                    <a href="{{ protocol }}://{{ domain }}/#/resident/profile">
                        Update profile 
                    </a>
                </p>               
                """,
                'base': base_template,
            }
        )

        MailTemplate.clean_cache()
