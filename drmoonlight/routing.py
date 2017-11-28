from channels import include

from apps.accounts.routing import channel_routing as accounts_routing


channel_routing = [
    include(accounts_routing),
]
