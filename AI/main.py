from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
from flask_cors import CORS  # Import CORS

# initialize a flask app
app = Flask(__name__)
CORS(app)
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
    "selling points. Generate a JSON with key-value pairs for each topics."
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


@app.route("/AI/words/list", methods=["POST", "GET"])
def word_list_api():
    if not (request.is_json):
        return jsonify({"error": "send a json request"})
    data = request.json

    if "key" in data:  # type:ignore
        if data["key"] != "kookkookiehackers":  # type:ignore
            return jsonify({"error": "Invalid Key"})

        business = data["business"]  # type:ignore
        model_response = get_words(business)
        word_json = model_response["choices"][0]["message"]["content"]  # type:ignore
        return jsonify(word_json)

    return jsonify({"error": "Invalid Key"})


if __name__ == "__main__":
    print(get_words("hair cutting"))
