from collections import namedtuple


def get_request_user_context(user):
    Request = namedtuple('Request', ['user'])

    return {
        'request': Request(user),
    }
