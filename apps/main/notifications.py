import json

from django.db import transaction
from libs.drf_kebab_case.utils import kebabize
from channels import Group


def notify(channel, event, payload_fn):
    """
    Notifies `channel` about event with payload from `payload_fn` result.
    This method accepts `payload_fn` because this notification will be sent
    after transaction is finished, so after that new payload can be different.

    :param channel: str
    :param event: str
    :param payload_fn: func
    """
    def _notify():
        Group(channel).send({
            'text': json.dumps({
                'event': event,
                'payload': kebabize(payload_fn()),
            })
        })

    transaction.on_commit(_notify)
