from dotenv import load_dotenv, find_dotenv
from pathlib import Path

import logging
import os

env_path = Path('../') / '.env'
load_dotenv(find_dotenv())

TELEGRAM_TOKEN = os.getenv('BRB_TELEGRAM_TOKEN')
TELEGRAM_ADMIN_LIST = [os.getenv('BRB_TELEGRAM_ADMIN')]

TRELLO_API_KEY = os.getenv('BRB_TRELLO_API_KEY')
TRELLO_TOKEN = os.getenv('BRB_TRELLO_TOKEN')

ADMIN = os.getenv('BRB_TELEGRAM_ADMIN')

PROXY = os.getenv('BRB_PROXY', None)

START_TEXT = """I'm a bot which helps you to report bugs to your IT band!
Every time the hashtag #bugs is found in your message I will create a card in provided board and list.
First, you should set up a board and a list where I will put new cards.
To do this just type /config"""

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
