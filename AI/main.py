from openai import OpenAI
from dotenv import load_dotenv
import os

# load the .env environment
load_dotenv()

# get the api key from .env file
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()
