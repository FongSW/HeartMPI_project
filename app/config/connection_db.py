from sqlalchemy import create_engine, MetaData
from dotenv import load_dotenv
from pathlib import Path
import os


# Load .env for getting variables
dotenv_path = Path('.env') # .env.local
load_dotenv(dotenv_path=dotenv_path)

# Access the environment variable and create the engine
engine = create_engine(os.environ['MAIN_DB'])

con_db = engine.connect()
meta = MetaData()
