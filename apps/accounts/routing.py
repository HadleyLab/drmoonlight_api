from .consumers import UserConsumer


channel_routing = [
    # WS user consumer
    UserConsumer.as_route(path=r'^/accounts/user/(?P<key>[\d\w]+)/$'),
]
