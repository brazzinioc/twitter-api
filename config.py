from dotenv import load_dotenv
from os import getenv

load_dotenv()

APP_NAME = getenv("APP_NAME")
HOST = getenv("HOST")
PORT = getenv("PORT")
DEBUG = getenv("DEBUG")