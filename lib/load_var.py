import toml
import os
from dotenv import load_dotenv
import logging

load_dotenv()
var_path = os.getenv('CONFIG_PATH')

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())

log.debug('Loading config...')
try:
    config_vars = toml.load(var_path)
except FileNotFoundError:
    log.critical('File {0} not found :(.)'.format(var_path))
    raise


def get_var(var: str):
    return config_vars[var]
