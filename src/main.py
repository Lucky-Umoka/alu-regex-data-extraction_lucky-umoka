import re

EMAIL_REGEX = re.compile(
    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
)


def group_email(email):
    domain =email.split('@')[-1].lower()
    if domain.endswith('alumni.alueducation.com'):
        return 'alu-alumni'
    elif domain.endswith('si.alueducation.com'):
        return 'alu-si'
    elif domain.endswith('alueducation.com'):
        return 'alu-official'
    else:
        return 'alu-email'


CREDIT_CARD_REGEX = re.compile(
    r'\b(?:\d{4}[-\s]?){3}\d{4}\b'
)


PHONE_REGEX = re.compile(
    r'\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}\b'       
)


TIME_REGEX = re.compile(
    r'\b(?:[01]?\d|2[0-3]):[0-5]\d(?::[0-5]\d)?\s?([APap][Mm])?\b'   
)


