import re
import json

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
        return 'normal-mail'


CREDIT_CARD_REGEX = re.compile(
    r'\b(?:\d{4}[-\s]?){3}\d{4}\b'
)


DATE_PATTERN = re.compile(
    r'\b\d{4}-\d{2}(?:[T\s]\d{2}:\d{2}:\d{2})?\b|\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'
)


PHONE_REGEX = re.compile( 
    r'(?<!\w)\+?\d{0,3}[-.\s]?(?:\(\d{2,4}\)[-.\s]?)?(?:\d{2,4}[-.\s]?){1,4}\d{2,4}(?!\w)'     
)


TIME_REGEX = re.compile(
    r'\b(?:[01]?\d|2[0-3]):[0-5]\d(?::[0-5]\d)?\s?([APap][Mm])?\b'   
)


# Security measure: Clean the text, reject non-string or oversized input before any processing (resource exhaustion guard)
def clean_text(raw_text):
    if not isinstance(raw_text, str):
        raise TypeError("Input must be a string.")
    if len(raw_text) > 1_000_000:
        raise ValueError("Input is too large - not processing. Maximum allowed length is 1,000,000 characters.")
    # Extra security measure to strip null bytes which can be used to confuse downstream processing or logging systems
    cleaned = raw_text.replace('\x00', '')
    return cleaned


def extract_credit_cards(text):
    matches = []
    for m in CREDIT_CARD_REGEX.finditer(text):
        matches.append({'match': m.group(), 'start': m.start(), 'end': m.end()})
    return matches


def extract_dates(text):
    matches = []
    for m in DATE_PATTERN.finditer(text):
        matches.append({'match': m.group(), 'start': m.start(), 'end': m.end()})
    return matches


def hide_spans(text, spans):
    masked = list(text)
    for span in spans:
        for i in range(span['start'], span['end']):
            masked[i] = '*'
    return ''.join(masked)


# Security measure: Hide the credit card numbers and dates BEFORE phone extraction runs, since both
# share the same digit-group shape as phone numbers. This prevents accidental selection of sensitive data as phone numbers and would otherwise be misclassified
def extract_phones(text):
    spans_to_hide = extract_credit_cards(text) + extract_dates(text)
    masked_text = hide_spans(text, spans_to_hide)
    results = []
    for m in PHONE_REGEX.finditer(masked_text):
        digit_count = len(re.sub(r'\D', '', m.group()))
        if digit_count >= 7:
            results.append(m.group().strip())
    return results



def extract_emails(text):
    results = []
    for m in EMAIL_REGEX.finditer(text):
        results.append({'email': m.group(), 'type': group_email(m.group())})
    return results



def extract_times(text):
    results = []
    for m in TIME_REGEX.finditer(text):
        is_12_hour = m.group(1) is not None
        results.append({'time': m.group().strip(), 'format': '12-hour' if is_12_hour else '24-hour'})
    return results




def main():
    with open('input/raw-text.txt', 'r', encoding='utf-8') as f:
        raw_text = f.read()   # Reads the raw text from the input file

    text = clean_text(raw_text)  # Clean the text input (type/size checks and null byte removal)

    emails = extract_emails(text)  # Extracts + classifies emails
    phones = extract_phones(text)  # Extracts phone numbers (the cards/dates are masked first)
    times = extract_times(text)    # Extracts time strings, classifies as 12-hour/24-hour
    dates = extract_dates(text)    # Internal use only, not outputted, but used to mask phone numbers
    credit_cards = extract_credit_cards(text)   # Extracts credit card numbers

    # Hiding the card numbers in a mask before they ever reach the output or logs - show only last 4 digits of the card details
    # This is a security measure to prevent unnecessary exposure of sensitive data in logs or output files
    cards = []
    for c in credit_cards:
        digits_only = re.sub(r'\D', '', c['match'])
        masked = '**** **** **** ' + digits_only[-4:]
        cards.append(masked)

    results = {
        'emails': emails,
        'phones': phones,
        'times': times,
        'credit_cards': cards,
    }


    print('Extraction Summary:')
    print('   Emails found:', len(emails))
    print('  Phones found:', len(phones))
    print('   Times found:', len(times))
    print('  Credit cards found (masked):', len(cards))

    with open('output/sample-output.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)



if __name__ == '__main__':
    main()