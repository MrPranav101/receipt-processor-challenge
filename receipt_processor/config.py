from os import getenv


APP_NAME = getenv('APP_NAME', 'receipt-processor')
VERSION = getenv('VERSION', '0.0.1')
LOG_LEVEL = getenv('LOG_LEVEL', 'INFO')
