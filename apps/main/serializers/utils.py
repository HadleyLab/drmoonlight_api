from collections import namedtuple


def get_request_user_context(user):
    Request = namedtuple('Request', ['user', 'build_absolute_uri'])

    return {
        'request': Request(user, lambda x: x),
    }
