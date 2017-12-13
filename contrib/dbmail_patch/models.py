from dbmail.models import MailTemplate


def hack_models():
    subject_field = MailTemplate._meta.get_field('subject')
    subject_field.max_length = 1024
    hack_validators(subject_field.validators, 1024)


def hack_validators(validators, length):
    from django.core.validators import MaxLengthValidator
    for key, validator in enumerate(validators):
        if isinstance(validator, MaxLengthValidator):
            validators.pop(key)
    validators.insert(0, MaxLengthValidator(length))


hack_models()
