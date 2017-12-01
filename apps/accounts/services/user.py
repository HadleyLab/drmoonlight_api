from djoser import email


def process_user_creation(user):
    context = {'user': user}
    to = [user.email]
    email.ActivationEmail(context=context).send(to)
