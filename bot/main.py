from dotenv import load_dotenv
from bot.run import run
import traceback
import logging


def main():
    logging.basicConfig(filename="std.log", format='%(asctime)s %(message)s', level=logging.DEBUG)
    load_dotenv()

    try:
        run()
    except Exception as e:
        logging.error(traceback.format_exc())
        exit(1)
