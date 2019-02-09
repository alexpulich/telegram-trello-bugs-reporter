#Telegram - Trello Bugs Reporter
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/938eddec003548a890ac574f717db067)](https://www.codacy.com/app/alexpulich/telegram-trello-bugs-reporter?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=alexpulich/telegram-trello-bugs-reporter&amp;utm_campaign=Badge_Grade)

## Description
Simple telegram long polling bot which tracks messages in chats with #bugs/#bug hash tags and creates a trello card in configured list of tasks with reported bug. Supports plain text massages and images/documents attachments.

## Core dependencies
* py-trello
* python-dotenv
* python-telegram-bot
* tinydb

## How to start
1. Create .env file from provided .env.example and fill it up with your data
2. docker-compose up
