#!/usr/bin/python3
import logging
import yaml
from email_validator import validate_email, EmailNotValidError

def read_configs():
    parameters = [""] * 5

    with open(r'config.yaml') as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        config_list = yaml.load(file, Loader=yaml.FullLoader)

        for key, value in config_list.items():
            logging.info(key + " : " + str(value))

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
            else:
                logging.error("Unsupported key: " + key)
        logging.info(parameters)
        return parameters

def validate_inserted_email(email):
    logging.debug(email)
    if email == None:
        return False

    try:
      valid = validate_email(email)
      email = valid.email
    except EmailNotValidError as e:
      # email is not valid, exception message is human-readable
      logging.error(str(e))
      return False

    return True