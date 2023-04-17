from pathlib import Path

BASE_DIR = Path().absolute()
env_file_name = '.env' if Path(BASE_DIR, '.env').exists() else '.env-example'
with open(Path(BASE_DIR, env_file_name)) as file:
    ENV = {line.split('=')[0]: line.split('=')[1] for line in file.read().strip().split()}

SECRET_KEY = ENV.get('SECRET_KEY', 'SECRET_KEY')
CREDITS_ON_LOGIN = ENV.get('CREDITS_ON_LOGIN', 100)
