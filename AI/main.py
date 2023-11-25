from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import json

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

PROMPT_GENERATE_DESCRIPTION = (
    "Generate a description for a <BS_TYPE> business on a freelance platform "
    "The name of the business is <BS_NAME> and the tagline is <BS_TAGLINE>"
    "keeping the following key value pair of words/values important"
    "to the business in your mind "
    "<JSON_KV_PAIR>"
)
# prompt generation context.
CONTEXT_DESC_GENERATION = (
    "You're helping a business owner to write a description for "
    "their business on a freelance platform. They have choosen "
    "A key values pair to best describe themselves and their "
    "business."
)

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


def get_description(bs_name, bs_type, bs_tagline, kv_pair):
    messages = [
        {"role": "system", "content": CONTEXT_DESC_GENERATION},
        {
            "role": "user",
            "content": PROMPT_GENERATE_DESCRIPTION.replace(
                "<JSON_KV_PAIR>", str(kv_pair)
            )
            .replace("<BS_NAME>", bs_name)
            .replace("<BS_TYPE>", bs_type)
            .replace("<BS_TAGLINE>", bs_tagline),
        },
    ]
    response = client.chat.completions.create(
        model=MODEL, messages=messages  # type:ignore
    )
    return response


@app.route("/AI/words/list", methods=["POST", "GET"])
def word_list_api():
    data = request.get_json()
    if "key" in data:  # type:ignore
        if data["key"] != "kookkookiehackers":  # type:ignore
            return jsonify({"error": "Invalid Key"})

        business = data["business"]  # type:ignore
        model_response = get_words(business).choices[0].message.content
        return jsonify(json.loads(model_response))  # type:ignore

    return {"error": "Invalid Key"}


@app.route("/AI/business/description", methods=["POST", "GET"])
def business_description_api():
    data = request.get_json()
    if "key" in data:
        if data["key"] != "kookkookiehackers":
            return jsonify({"error": "Invalid Key"})

        bs_name = data["bs_name"]
        bs_type = data["bs_type"]
        bs_tag = data["bs_tag"]
        kv_pair = data["kv_pair"]
        model_response = (
            get_description(bs_name, bs_type, bs_tag, kv_pair)
            .choices[0]
            .message.content
        )
        return jsonify({"desc": model_response})
    return jsonify({"error": "Invalid Key"})


with open("dummy_data.json", "r") as file:
    data = json.load(file)


# Define a decorator for handling CORS headers
@app.route("/dummy/kv/", methods=["POST", "GET"])
def dummy_data_dump():
    return jsonify({"kv_pair": data[1]})


@app.route("/dummy/desc/", methods=["POST", "GET"])
def demo_desc():
    return jsonify({"desc": data[0]})


@app.route("/dummy/content", methods=["POST", "GET"])
def demo_content():
    return jsonify({"content": data[2:]})


if __name__ == "__main__":
    kv_pair = {
        "values": [
            "Professionalism",
            "Customer satisfaction",
            "Attention to detail",
            "Innovation",
            "Reliability",
        ],
        "services": [
            "Haircuts",
            "Hairstyling",
            "Hair coloring",
            "Highlights",
            "Treatments",
            "Beard trims",
        ],
        "expertise": [
            "Skilled stylists",
            "Experienced professionals",
            "Up-to-date with latest trends",
        ],
        "unique selling points": [
            "Personalized experience",
            "Relaxing environment",
            "Timely service",
            "Affordable prices",
        ],
    }
    bs_name = "Bimarsha Hair cutting"
    bs_type = "Hair cut"
    bs_tagline = "The best hair cut in hattiesburg"
    # print(get_description(bs_name, bs_type, bs_tagline, kv_pair))
    print(get_words(bs_type).choices[0].message.content)
    print(
        get_description(bs_name, bs_type, bs_tagline, kv_pair)
        .choices[0]
        .message.content
    )
