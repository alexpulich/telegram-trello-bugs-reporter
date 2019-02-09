from tinydb import TinyDB, Query

db = TinyDB('../db.json')


def save_config(config):
    """
    Save config
    :param config: Config mapping chat id to trello configs
    {
        'chat_id': int,
        'board': int - id of a trello board,
        'list': int - id of a trello list
    :return:
    """
    if 'chat_id' not in config:
        return False

    chat_config = db.search(Query().chat_id == config['chat_id'])

    if chat_config:
        db.update(config, Query().chat_id == config['chat_id'])
        return True

    db.insert(config)
    return True


def get_list(chat_id):
    """
    Get trello list id for provided chat
    :param chat_id:
    :return:
    """
    item = db.search(Query().chat_id == chat_id)

    if not item:
        return False
    return item[0]['list']
