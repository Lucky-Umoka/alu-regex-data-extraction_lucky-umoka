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
        return 'alu-email'


CREDIT_CARD_REGEX = re.compile(
    r'\b(?:\d{4}[-\s]?){3}\d{4}\b'
)


PHONE_REGEX = re.compile( 
    r'(?<!\w)\+?\d{0,3}[-.\s]?(?:\(\d{2,4}\)[-.\s]?)?(?:\d{2,4}[-.\s]?){1,4}\d{2,4}(?!\w))'     
)


TIME_REGEX = re.compile(
    r'\b(?:[01]?\d|2[0-3]):[0-5]\d(?::[0-5]\d)?\s?([APap][Mm])?\b'   
)

def clean_text(raw_text):
    if not isinstance(raw_text, str):
        raise TextError("Input must be a string.")
    if len(raw_text) > 1_000_000:
        raise TextError("Input is too large - not processing. Maximum allowed length is 1,000,000 characters.")
    cleaned = raw_text.replace('\x00', '')
    return cleaned

def extract_credit_cards(text):
    matches = []
    for m in CREDIT_CARD_REGEX.finditer(text):
        matches.append({'match': m.group(), 'start': m.start(), 'end': m.end()})
    return matches


def hide_spans(text, spans):
    masked = list(text)
    for span in spans:
        for i in range(span['start'], span['end']):
            masked[i] = '*'
    return ''.join(masked)


def extract_phones(text):
    masked_text = mask_spans(text, extract_credit_cards(text))
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
    with open('input/raw-text.text', 'r', encoding='utf-8') as f:
        raw_text = f.read()

    text = clean_text(raw_text)

    emails = extract_emails(text)
    phones = extract_phones(text)
    credit_cards = extract_credit_cards(text)

    # Hiding the card numbers in a mask before they ever reach the output or logs - show only last 4 digits of the card details
    cards = []
    for c in cards_raw:
        digits_only = re.sub(r'\D', '', c['match'])
        masked = '**** **** **** ' + digits_only[-4]
        cards.append(masked)

    results = {
        'emails': emails,
        'phones': phones,
        'times': times,
        'credit_cards': cards,
    }


    print('Extraction Summary:')
    print('   Emails found:', len(emails))
    print('.  Phones found:', len(phones))
    print('   Times found:', len(times))
    print('.  Credit cards found (masked):', len(cards))

    with open('output/sample-output.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)



if __name__ == '__main__':
    main()