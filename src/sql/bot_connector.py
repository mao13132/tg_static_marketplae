import os

from settings import program_dir
from src.sql.bd import BotDB

BotDB = BotDB(f"{program_dir}{os.sep}DB.db")
