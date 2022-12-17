#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import telegram
from telegram.error import NetworkError, Unauthorized, TimedOut
from time import sleep
import os
from time import time
from src.entry import entry
import sys
import traceback

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

try:
    # BOT_TOKEN = os.environ["BOT_TOKEN"]
    BOT_TOKEN = "1045060630:AAETNfpHmDbGv8W3AzE_EO4i9zCNxAXDHws"
except KeyError:
    logging.error("Bot credentials not found in environment")
    sys.exit("End program with error")

# How long the container exist
LIFESPAN = 7200


def main():
    """Run the bot."""
    try:
        update_id = int(os.environ["UPDATE_ID"])
    except:
        update_id = 0
    bot = telegram.Bot(BOT_TOKEN)

    while True:
        try:
            for update in bot.get_updates(offset=update_id, timeout=10):
                update_id = update.update_id + 1
                logging.info(f"Update ID:{update_id}")
                entry(bot, update)
        except NetworkError as e:
            print("Network Error")
            print(e)
            traceback.print_exc()
            # logging.error(update)
            sleep(1)
        except Unauthorized:
            print("Unauthorized")
            logging.error(update)
            # The user has removed or blocked the bot.
            update_id += 1
        except TimedOut:
            logging.error("Timeout")
            traceback.print_exc()
            sleep(5)
        except Exception as e:
            logging.error("Generic Error")
            logging.error(e)
            traceback.print_exc()
            sleep(5)
            sys.exit("End program with error")

if __name__ == "__main__":
    main()
