import os
import secrets
import sys

try:
    with open("secret_key.txt", "r") as file:
        secret_key = file.readline().strip()
        SECRET_KEY = secret_key
except Exception as e:
    sys.stderr.write(str(e))
    with open("secret_key.txt", "w+") as file:
        file.write(secrets.token_hex(48))  # 384 bits
        SECRET_KEY = file.readline().strip()

TEMPLATES_AUTO_RELOAD = True
LOGGING_FILE_LOCATION = "logs/application.log"
