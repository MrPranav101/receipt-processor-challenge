from os import getenv


APP_NAME = getenv('APP_NAME', 'Receipt Processor')
VERSION = getenv('VERSION', '1.0.0')
LOG_LEVEL = getenv('LOG_LEVEL', 'INFO')
OPENAPI_VERSION = getenv('OPENAPI_VERSION', '3.0.3')
