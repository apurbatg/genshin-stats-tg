import requests

import json

import logging

from telegram import Update

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Set up logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',

                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Replace YOUR_BOT_TOKEN with your actual bot token obtained from BotFather

TOKEN = '6128210574:AAGFmQPO6GiUO1WQr4UZvJv48rfqVuQWF6A'

def start(update: Update, context: CallbackContext) -> None:

    """Send a message when the command /start is issued."""

    update.message.reply_text('Hi! Send me the name of a Genshin Impact character to get information on their uses.')

def character_info(update: Update, context: CallbackContext) -> None:

    """Search for character information and send it to the user."""

    character_name = context.args[0]

    # Call the API to search for the character

    url = f'https://api.genshin.dev/characters/{character_name}'

    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:

        data = json.loads(response.text)

        try:

            # Extract the section containing the character uses

            character_title = data['name']

            character_description = data['description']

            character_rarity = data['rarity']

            character_weapon = data['weapon']

            character_element = data['element']

            character_artifact = data['artifact']

            # Send the information to the user

            update.message.reply_text(f'{character_title}\n\n'

                                      f'Description: {character_description}\n\n'

                                      f'Rarity: {character_rarity}\n'

                                      f'Weapon: {character_weapon}\n'

                                      f'Element: {character_element}\n'

                                      f'Artifact: {character_artifact}')

        except:

            update.message.reply_text(f'Sorry, I could not find any information on {character_name}.')

    else:

        update.message.reply_text('Sorry, something went wrong. Please try again later.')

def error(update: Update, context: CallbackContext) -> None:

    """Log the error and send a message to the user."""

    logger.warning(f'Update {update} caused error {context.error}')


def main() -> None:

    """Start the bot."""

    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler("start", start))

    updater.dispatcher.add_handler(CommandHandler("character_info", character_info))

    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, character_info))

    updater.dispatcher.add_error_handler(error)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':

    main()

