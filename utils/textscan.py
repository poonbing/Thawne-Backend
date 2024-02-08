import re

sensitive_data = [
    r'^[SFTG]\d{7}[A-Z]$', #NRIC
    r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$',  #IPv4
    r'^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$',  #Mastercard
    r'\b([4]\d{3}[\s]\d{4}[\s]\d{4}[\s]\d{4}|[4]\d{3}[-]\d{4}[-]\d{4}[-]\d{4}|[4]\d{3}[.]\d{4}[.]\d{4}[.]\d{4}|[4]\d{3}\d{4}\d{4}\d{4})\b', #Visa
    r'^3[47][0-9]{13}$',  #Amex
    r'\b[\w.-]{0,25}@(yahoo|hotmail|gmail)\.com\b' #Email
]

def text_scanning(text):
    words = text.split()  # Split the sentence into words
    for word in words:
        for pattern in sensitive_data:
            search = re.search(pattern, word, re.IGNORECASE)
            if search:
                matched_word = search.group()
                print('Matched:', matched_word)
                return True, matched_word

text_scanning('The IP address is 192.168.1.1 and the email is lewistay03@gmail.com')
text_scanning('192.168.1.1')
text_scanning('lewistay03@gmail.com')
text_scanning('4628450041156747')
text_scanning('My nric is t0325409c')

