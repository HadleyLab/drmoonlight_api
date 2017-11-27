import json

from django.db import transaction
from libs.drf_kebab_case.utils import kebabize
from channels import Group


def notify(channel, event, payload):
    def _notify():
        Group(channel).send({
            'text': json.dumps({
                'event': event,
                'payload': kebabize(payload),
            })
        })

    transaction.on_commit(_notify)
