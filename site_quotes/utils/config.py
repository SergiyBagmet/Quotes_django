import configparser
from pathlib import Path

file_config = Path(__file__).parent.joinpath("config.ini")
config = configparser.ConfigParser()
config.read(file_config)

username = config.get('MONGO', 'USER')
password = config.get('MONGO', 'PASSWORD')
db_name = config.get('MONGO', 'DB_NAME')
domain = config.get('MONGO', 'DOMAIN')
retry_writes = config.get('MONGO', 'RETRY_WRITES')
ssl = config.get('MONGO', 'SSL')

mongo_uri = (
    f"mongodb+srv://{username}:{password}@{domain}/"
    f"?retryWrites={retry_writes}&w=majority&ssl={ssl}"
)
