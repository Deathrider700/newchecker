#--- START OF FILE utils.py ---

#utils.py - Utility functions used across the bot

import string
import random
from faker import Faker
import re
import keyword

def get_string_between(text, start_word, end_word):
    """
    Extracts the string between two specified words in a given text.
    Returns an empty string if start_word or end_word is not found, or if there's nothing between them.
    """
    start_index = text.find(start_word)
    if start_index == -1:
        return ''
    start_index += len(start_word)
    end_index = text.find(end_word, start_index)
    if end_index == -1:
        return ''
    return text[start_index:end_index]

def generate_random_alphabet_string(length):
    """
    Generates a random string of lowercase alphabet characters of the specified length.
    """
    alphabet_string = string.ascii_lowercase
    random_string = ''.join(random.choice(alphabet_string) for _ in range(length))
    return random_string

def generate_address():
    """
    Generates a random US address (city, state, street address, zip code).
    Returns a tuple: (city, state, street_address, zip_code).
    """
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"]
    states = ["NY", "CA", "IL", "TX", "AZ", "PA", "TX", "CA", "TX", "CA"]
    streets = ["Main St", "Park Ave", "Oak St", "Cedar St", "Maple Ave", "Elm St", "Washington St", "Lake St", "Hill St", "Maple St"]
    zip_codes = ["10001", "90001", "60601", "77001", "85001", "19101", "78201", "92101", "75201", "95101"]

    city = random.choice(cities)
    state = states[cities.index(city)]
    street_address = str(random.randint(1, 999)) + " " + random.choice(streets)
    zip_code = zip_codes[states.index(state)]
    return city, state, street_address, zip_code

def generate_phone_number():
    """
    Generates a random US phone number starting with '303'.
    """
    num = ''.join(random.choices(string.digits, k=7))
    return f"303{num}"

def generate_random_email():
    """
    Generates a random email address using Faker.
    """
    faker = Faker()
    return str(faker.email()).replace('example', 'gmail')

def generate_username():
    """
    Generates a random username using Faker.
    """
    faker = Faker()
    return faker.user_name()

def generate_password():
    """
    Generates a random password using Faker.
    """
    faker = Faker()
    return faker.password()

def get_card_type_from_bin(bin_prefix):
    """
    Simple function to guess card type from the first digit of BIN.
    Note: This is a very basic guess and might not be accurate for all BINs.
    For more reliable card type detection, use a proper BIN lookup service.
    """
    first_digit = bin_prefix[0] if bin_prefix else ''
    if first_digit == '4':
        return 'VISA'
    elif first_digit == '5':
        return 'MASTERCARD'
    elif first_digit == '3':
        return 'AMEX'
    elif first_digit == '6':
        return 'DISCOVER'
    else:
        return 'Unknown'

def extract_ccs_from_line(text):
    """
    Extracts credit card details from a text line.
    Assumes CC details are in the format: cc|mm|yy|cvv.
    Returns a list of CC strings found in the text.
    """
    ccs = []
    lines = text.strip().splitlines()
    for line in lines:
        cc_match = re.findall(r'(\d{13,19})\|(\d{1,2})\|(\d{2,4})\|(\d{3,4})', line)
        if cc_match:
            for match in cc_match:
                ccs.append("|".join(match))
    return ccs

def generate_iban():
    """Generates a random IBAN (International Bank Account Number)."""
    faker = Faker()
    return faker.iban()

def generate_swift():
    """Generates a random SWIFT/BIC code."""
    faker = Faker()
    return faker.swift()

def generate_btc_address():
    """Generates a random Bitcoin (BTC) address."""
    faker = Faker()
    return faker.btc_address()

def generate_usdt_address():
    """Generates a random USDT (Tether) TRC20 address (using Tron address as approximation)."""
    faker = Faker()
    return faker.tron_address()