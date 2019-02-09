from trello import TrelloClient

import settings

client = TrelloClient(
    api_key=settings.TRELLO_API_KEY,
    token=settings.TRELLO_TOKEN,
)
