import requests
import socket
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import time

from utils import promptInput
from utils import formatDebug
from utils import formatErr
from utils import clearTerminal

# Variables
lange = "en"


def lookupIp():
    while True:
        ip = promptInput("Enter IP (q to exit)")

        if ip.lower()=="q": break

        try:
            fetch = requests.get(f'http://ip-api.com/json/{ip}?fields=66846719').json()
        except Exception as e:
            print(formatErr(e))

        if fetch.get("status") == "fail":
            msg = fetch.get("message")
            if msg == "invalid query":
                print(formatErr(f"{ip} is an invalid IP address"))
            elif msg == "private range":
                print(formatErr(f"{ip} is a private IP address"))
            elif msg == "reserved range":
                print(formatErr(f"{ip} is a reserved IP address"))
            else:
                print(formatErr(msg))
        else:
            for label in fetch:
                val = fetch.get(label)
                print(formatDebug(label, val))

        print() 

def lookupNum():
    while True:
        phoneNumber = promptInput("Enter Phone number (q to exit)")

        if str(phoneNumber).lower()=="q": break

        if not str(phoneNumber).startswith("+"): phoneNumber="+" + phoneNumber

        try:
            parsed = phonenumbers.parse(phoneNumber, None)

            toget = {
                'query': phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                'is_valid_number': phonenumbers.is_valid_number(parsed), 
                'country_code': "+" + str(parsed.country_code), 
                'carrier':carrier.name_for_valid_number(parsed, lange),
                'country': geocoder.country_name_for_number(parsed, lange),
                'timezone': timezone.time_zones_for_number(parsed)
            }

            for label, returned in toget.items():
                print(formatDebug(str(label), str(returned)))
            print()


        except phonenumbers.NumberParseException as err:
            if err.error_type == phonenumbers.NumberParseException.NOT_A_NUMBER:
                print(formatErr("query isn't an int object"))
            elif err.error_type == phonenumbers.NumberParseException.TOO_LONG:
                print(formatErr("query is too long"))
            elif err.error_type == phonenumbers.NumberParseException.INVALID_COUNTRY_CODE:
                print(formatErr("invalid country code"))

        

