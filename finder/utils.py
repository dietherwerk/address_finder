import re


def validate_address(cep):
    if re.search('^[0-9]+$', cep):
        return True

    return
