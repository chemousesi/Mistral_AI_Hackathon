#!/usr/bin/env python

# https://docs.mistral.ai/platform/client/#embeddings

import os
import csv

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage # Not necessary for embeddings

## ----------------------- Definitions ----------------------- ##

CSV_FILE = "output.csv"

# Determine if the document is a street or parking restriction document, if not, return "None"
type_of_document = "Determine quel type de document entre un document de restriction de rue ou de stationnement. Si ce n'est pas le cas, retourne 'None' and stop the process.\n"

# Describe the CSV format and if one of the fields is missing, set it to "None"
CSV_fields = "Adresse, date, période, disponibilité, raison (loi/événement), critères, Source,"
CSV_format = "Fais un synthese de ce document avec une reponse très concis dans ce format de CSV avec ces champs precis: " + CSV_fields + " \
si un des champs est manquant, mettez-le a 'None'.\n"

example = """
This is an example of the response that should be generated:
"Rue du Valibout, Plaisir", "2018 Janvier", "3 mois", "Limitée", "Loi", "Sécurité, Interdiction de stationnement pour poids lourds, sauf services publics ou déplacement", "Interdiction de stationnement pour poids lourds, sauf services publics ou déplacement", "Direction des services techniquesdirection des services techniques"\n
"""

seed_text = "Voici le document:\n"


## ----------------------- Functions ----------------------- ##


# Function to read the content of a text file
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

    directory = "../examples"
    
    # Define the list of file extensions to check
    extensions_list = ('.pdf', '.jpg', '.jpeg', '.png', '.txt', '.docx', '.doc')
    csv_array = []
    # Create a loop to read all the files in the directory and extract the text from each file
    for file in os.listdir(directory):
        if file.endswith(extensions_list):

            file_content = read_text_file(os.path.join(directory, file))

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

            line = chat_response.choices[0].message.content.split(',') # Split the response into a list of strings
            # Remove all of the double quotes from the strings
            line = [string.replace('"', '') for string in line]

            print(line)

            csv_array.append(line)
        else
            print(f"Error: File '{file}' is not a valid file type.")

    # Write the response to a CSV file
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        for row in csv_array:
            writer.writerow(row)
    
    print(f"Response written to '{CSV_FILE}'")



if __name__ == "__main__":
    main()
