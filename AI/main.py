from openai import OpenAI
from dotenv import load_dotenv

# load the .env environment
load_dotenv()

# get the api key from .env file
client = OpenAI()
