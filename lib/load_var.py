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
    config_vars = toml.load(var_path or 'config_default.toml')
except FileNotFoundError:
    log.critical('File {0} not found :(.)'.format(var_path))
    raise


def get_var(var: str, default=None):
    """Return configuration variable.

    Args:
        var: The name of the value to retrieve from the configuration file
        default: The value to be returned if the value var doesn't exist in the
        configuration file
    """
    if var in config_vars:
        return config_vars[var]
    else:
        return default


if __name__ == "__main__":
    print(get_var("CMD_PREFIX", "non"))
