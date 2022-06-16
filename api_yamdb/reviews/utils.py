from django.utils.crypto import get_random_string


def confirmation_code_generator():
    confirmation_code = get_random_string(length=10)
    return confirmation_code
