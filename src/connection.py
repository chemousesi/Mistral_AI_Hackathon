#!/usr/bin/env python

# https://docs.mistral.ai/platform/client/#embeddings

import os

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage # Not necessary for embeddings


def read_text_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")



def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    # model = "mistral-large-latest"
    model = "mistral-tiny"
    client = MistralClient(api_key=api_key)

    # embeddings_batch_response = client.embeddings(
    #     model="mistral-embed",
    #     input=["Embed this sentence.", "As well as this one."],
    # )

    file_content = read_text_file("../examples/example1.txt")

    print(file_content)

    seed_text = "Ceci est un document administratif pour un arret permanent sur une rue. \
        Fais un synthese de ce document dans ce CSV format: <date de l'arret>, <endroit de l'arret>, <raison de l'arret>, <Restrictions specifiques>.\
        Document:"

    payload = seed_text + file_content

    messages = [
        ChatMessage(role="user", content=payload)
    ]

    # No streaming
    chat_response = client.chat(
        model=model,
        messages=messages,
    )

    print(chat_response.choices[0].message.content)


if __name__ == "__main__":
    main()
