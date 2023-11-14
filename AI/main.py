from openai import OpenAI
from dotenv import load_dotenv

# load the .env environment
load_dotenv()

# create openAI client
client = OpenAI()

# MODEL
MODEL = "gpt-3.5-turbo"

# word generation prompt.
PROMPT_GENERATE_WORDS = (
    "Generate words that could be used to write a detailed business "
    "description for a <BUSINESS_NAME> business. Include terms that "
    "highlight the business's values, services, expertise, and unique "
    "selling points."
)

# prompt generation context.
CONTEXT_WORD_GENERATION = (
    "You are helping a business owner to write a description of "
    "their business. You need to offer them a list of words to choose "
    "the best words that fit with their personal and business values "
)


# get response from the model for a given business
def get_words(business):
    messages = [
        {"role": "system", "content": CONTEXT_WORD_GENERATION},
        {
            "role": "user",
            "content": PROMPT_GENERATE_WORDS.replace("<BUSINESS_NAME>", business),
        },
    ]
    response = client.chat.completions.create(
        model=MODEL, messages=messages  # type: ignore
    )
    return response
