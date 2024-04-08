#!/usr/bin/env python

# https://docs.mistral.ai/platform/client/#embeddings

import os
import csv

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
    model = "mistral-tiny" # mistral 7B 
    client = MistralClient(api_key=api_key)

    # embeddings_batch_response = client.embeddings(
    #     model="mistral-embed",
    #     input=["Embed this sentence.", "As well as this one."],
    # )

    file_content = read_text_file("../examples/example1.txt")

    print(file_content)

    # Determine if the document is a street or parking restriction document, if not, return "None"
    type_of_document = "Determine quel type de document entre un document de restriction de rue ou de stationnement. Si ce n'est pas le cas, retourne 'None' and stop the process.\n"

    # Describe the CSV format and if one of the fields is missing, set it to "None"
    CSV_format = "Fais un synthese de ce document avec une reponse très concis dans ce format de CSV avec ces champs precis: <date de l'arret>, <endroit de l'arret>, <raison de l'arret>, <Restrictions specifiques>, \
    si un des champs est manquant, mettez-le a 'None'.\n"

    example = """
    This is an example of the response that should be generated:
    "2013", "rue du Valibout, Plaisir", "Sécurité, Interdiction de stationnement pour poids lourds, sauf services publics ou déplacement", "Interdiction de stationnement pour poids lourds, sauf services publics ou déplacement"\n
    """

    seed_text = "Voici le document:\n"

    payload = type_of_document + CSV_format + example + seed_text + file_content

    print(payload)

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
