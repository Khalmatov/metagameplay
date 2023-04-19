import pathlib

BASE_DIR = pathlib.Path(__file__).parent.absolute()
CLIENT_DIR = BASE_DIR.parent / 'client'
AUTHORIZED_USER_PATH = CLIENT_DIR / '.AUTHORIZED_USER'
env_file_name = '.env' if pathlib.Path(BASE_DIR, '.env').exists() else '.env-example'
with open(pathlib.Path(BASE_DIR, env_file_name)) as file:
    ENV = {line.split('=')[0]: line.split('=')[1] for line in file.read().strip().split()}

CREDITS_ON_LOGIN = ENV.get('CREDITS_ON_LOGIN', 100)
