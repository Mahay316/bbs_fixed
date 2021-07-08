import os
from os import path
import logging.config

SECRET_KEY = os.urandom(24)

# SQLAlchemy configuration
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:mahay@localhost/bbs"
SQLALCHEMY_TRACK_MODIFICATIONS = True

# logging.config.fileConfig(str(path.abspath(path.dirname(__file__)))+'/logger.conf')
# logger = logging.getLogger("cse")

CONF_LOG = "./logger.conf"
logging.config.fileConfig(str(path.abspath(path.dirname(__file__)))+'/'+CONF_LOG);  # 采用配置文件
logger = logging.getLogger('BBS')
