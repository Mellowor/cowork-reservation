import configparser
import logging
import logging.config
import os

IN_DOCKER = os.environ.get("IS_IN_DOCKER", False)


class ConfigDatabase:
    logging.config.fileConfig(
        "db/resources/configs/logging.conf",
    )
    logger = logging.getLogger("AccessDataBase")
    logger.debug("logging.conf got")
    db_info = configparser.ConfigParser()
    if IN_DOCKER:
        db_info.read("db/resources/database.ini")
    else:
        db_info.read("db/resources/database_local.ini")
    logger.debug("database.ini got")
    postgres_access = {value[0]: value[1] for value in db_info.items("POSTGRES_CONNECT")}
    if new_value := os.environ.get("DATABASE_HOST"):
        postgres_access["host"] = new_value
    if new_value := os.environ.get("DATABASE_PASSWORD"):
        postgres_access["password"] = new_value
    if new_value := os.environ.get("DATABASE_DATABASE"):
        postgres_access["database"] = new_value
    if new_value := os.environ.get("DATABASE_USER"):
        postgres_access["username"] = new_value
    logger.debug("DATABASE INFO CONFIGURED")
