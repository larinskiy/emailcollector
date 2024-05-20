import smtplib
import dns.resolver
from tqdm import tqdm


def get_mx_records(domain):
    try:
        records = dns.resolver.resolve(domain, 'MX')
        mx_records = [record.exchange.to_text() for record in records]
        return mx_records
    except Exception as e:
        return []


def validate_email(email):
    domain = email.split('@')[1]
    mx_records = get_mx_records(domain)

    if not mx_records:
        return False

    for mx in mx_records:
        try:
            server = smtplib.SMTP(mx)
            server.set_debuglevel(0)

            server.helo()

            server.mail('info@gmail.com')

            code, message = server.rcpt(email)
            server.quit()

            if code == 250:
                return True
            else:
                return False
        except Exception as e:
            continue

    return False


validated = []
not_validated = []
with (open('mail.txt') as file):
    for email in tqdm(file.readlines(), desc="Searching", unit="mail"):
        email = email.strip()
        if validate_email(email):
            validated.append(email)
        else:
            not_validated.append(email)

with open('out_mail.txt', 'w') as file:
    print(f'Количество валидных почт: {len(validated)}', file=file)
    print(f'Количество невалидных почт: {len(not_validated)}', file=file)
    print('Валидные:\n', '\n'.join(validated), file=file)
    print('Невалидные:\n', '\n'.join(not_validated), file=file)
