#!/usr/bin/python3
import logging
import yaml
from enum import IntEnum
from email_validator import validate_email, EmailNotValidError


class email_validation(IntEnum):
    FALSE = -1
    NONE = 0
    TRUE = 1


NMR_CONFIG_PAR = 8

SUBSCRIBED_USERS_FILE_NAME = "output.csv"

BROWSER_SESSION_LIFETIME = 3

def read_configs():
    parameters = [""] * NMR_CONFIG_PAR

    with open(r"config.yaml") as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        config_list = yaml.load(file, Loader=yaml.FullLoader)

        for key, value in config_list.items():
            logging.debug(key + " : " + str(value))

            if key == "host":
                parameters[0] = value
            if key == "port":
                parameters[1] = value
            elif key == "facebook":
                parameters[2] = value
            elif key == "instagram":
                parameters[3] = value
            elif key == "youtube":
                parameters[4] = value
            elif key == "header":
                parameters[5] = value
            elif key == "paragraph":
                parameters[6] = value
            elif key == "central_image":
                parameters[7] = value
            else:
                logging.error("Unsupported key: " + key)
        logging.debug(parameters)
        return parameters


def validate_inserted_email(email):
    logging.debug(email)
    if email == None:
        return email_validation.NONE

    try:
        valid = validate_email(email)
        email = valid.email
    except EmailNotValidError as e:
        # email is not valid, exception message is human-readable
        logging.error(str(e))
        return email_validation.FALSE

    return email_validation.TRUE
