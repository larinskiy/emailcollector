import smtplib
import dns.resolver
from tqdm import tqdm
import requests
import json
import re
import os


def get_key(domain):
    url = f"https://2.intelx.io:443/phonebook/search?k={token}"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0",
               "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate",
               "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "Origin": "https://phonebook.cz",
               "Dnt": "1", "Referer": "https://phonebook.cz/", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors",
               "Sec-Fetch-Site": "cross-site", "Te": "trailers"}
    json = {"maxresults": 10000, "media": 0, "target": 2,
            "term": domain, "terminate": [None], "timeout": 20}
    response = requests.post(url, headers=headers, json=json)
    key = response.text
    status = response.status_code
    if status == 402:
        exit('[-] Your IP is rate limited. Try switching your IP address then re-run.')
    else:
        return key


def make_request(key):
    key = json.loads(key)['id']
    url = f"https://2.intelx.io:443/phonebook/search/result?k={
        token}&id={key}&limit=1000000"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0",
        "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate",
        "Origin": "https://phonebook.cz", "Dnt": "1", "Referer": "https://phonebook.cz/", "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "cross-site", "Te": "trailers"}
    response = requests.get(url, headers=headers)
    items = response.text
    status = response.status_code
    if status == 402:
        exit('[-] Your IP is rate limited. Try switching your IP address then re-run.')
    else:
        return items


def get_mx_records(domain):
    try:
        records = dns.resolver.resolve(domain, 'MX')
        mx_records = [record.exchange.to_text() for record in records]
        return mx_records
    except Exception as e:
        return []


def validate_email(email, mx_records):
    if not mx_records:
        return False
    for mx in mx_records:
        try:
            server = smtplib.SMTP(mx)
            server.set_debuglevel(0)
            server.helo()
            server.mail(validation_email)
            code, message = server.rcpt(email)
            server.quit()
            if code == 250:
                return True
            else:
                return False
        except Exception as e:
            continue
    return False


if input('[?] Do you want to make search for domain emails via Phonebook.cz? [Y/N] ').upper() == 'Y':
    token = ''
    while not (re.search(r"[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}", token)):
        token = input(
            '[?] Specify valid Phonebook.cz token: [Get it after authorization on Phonebook.cz] ').lower()
    domain = input(
        '[?] Specify the domain name for email search: [For ex. company.com] ')
    key = get_key(domain)
    answer = json.loads(make_request(key))['selectors']
    emails = sorted(set(email['selectorvalue'] for email in answer))
    if len(emails) != 0:
        print(
            f'[+] {len(emails)} addresses was collected in file collected_emails.txt')
        with open('collected_emails.txt', 'w') as file:
            print('\n'.join(emails), file=file)
        collected_emails_file = 'collected_emails.txt'
    else:
        exit('[-] No emails was found. Try use another domain name or run without Phonebook.cz')
else:
    collected_emails_file = -1
    while not os.path.isfile(collected_emails_file):
        collected_emails_file = input(
            '[?] Specify path to emails file: [For.ex emails.txt] ')
validation_email = input(
    '[?] Specify valid existing email address for validation or press Enter: [Def. info@gmail.com] ')
if not (re.search('\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', validation_email)):
    validation_email = 'info@gmail.com'
print(f'[+] Email address for validation is set to {validation_email}')
validated = []
not_validated = []
mx_dict = {}
with (open(collected_emails_file) as file):
    for email in tqdm(file.readlines(), desc="Validating", unit="mail"):
        email = email.strip()
        domain = email.split('@')[1]
        if domain in mx_dict:
            mx_records = mx_dict[domain]
        else:
            mx_records = get_mx_records(domain)
            mx_dict[domain] = mx_records
        if validate_email(email, mx_records):
            validated.append(email)
        else:
            not_validated.append(email)
if len(validated) != 0 or len(not_validated) != 0:
    with open('checked_emails.txt', 'w') as file:
        print(f'Count of valid emails: {len(validated)}', file=file)
        print(f'Count of invalid emails: {len(not_validated)}', file=file)
        print('Valid:\n', '\n'.join(validated), file=file)
        print('Invalid:\n', '\n'.join(not_validated), file=file)
    print(f"[+] {len(validated)} valid and {len(not_validated)
                                            } invalid emails was collected in file checked.email.txt")
else:
    print("[-] Something went wrong. No addressess was discovered")
