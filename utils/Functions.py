import re

def check_if_valid_email(username):

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.fullmatch(regex, username):
        return True
    return False


def get_valid_phone_number(username):
    return re.sub('[^0-9]+', '', username)