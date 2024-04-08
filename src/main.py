#!/usr/bin/env python

# https://docs.mistral.ai/platform/client/#embeddings

import os
import csv
import requests
from TxtExtraction import extract_text

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
"Rue du Valibout - Plaisir", "2018 Janvier", "3 mois", "Limitée", "Loi", "Sécurité, Interdiction de stationnement pour poids lourds, sauf services publics ou déplacement", "Interdiction de stationnement pour poids lourds, sauf services publics ou déplacement", "Direction des services techniquesdirection des services techniques"\n
"""

rules = "Règles pour la réponse : Supprimez chaque virgule (,) utilisée pour autre chose que pour séparer les champs. Joignez l'adresse complète du lieu avec - et non avec des espaces ou des virgules. Utilisez le même format que l'exemple ci-dessus.\n"
seed_text = "Voici le document:\n"


## ----------------------- Functions ----------------------- ##


def geolocation(addresse):      

    # Define the URL of the API endpoint
    ADDOK_URL = 'http://api-adresse.data.gouv.fr/search/'

    # Define the parameters for the API request, including the address and limit
    params = {
        'q': addresse,  # Address to search for
        'limit': 5  # Limit the number of results to 5
    }  
    # Send a GET request to the API endpoint with the defined parameters
    response = requests.get(ADDOK_URL, params=params)

    # Parse the JSON response into a Python dictionary
    j = response.json()

    # Check if there are any features (results) in the response
    if len(j.get('features')) > 0:
        # Get the first result from the features list
        first_result = j.get('features')[0]

        # Extract the longitude and latitude coordinates from the geometry property
        lon, lat = first_result.get('geometry').get('coordinates')

        postcode = first_result.get('properties').get('postcode')

        # Create a dictionary containing all information of the first result including lon and lat
        first_result_all_infos = { **first_result.get('properties'), **{"lon": lon, "lat": lat, "postcode": postcode}}

        return (f"Lon: {lon}, Lat: {lat}, Postcode: {postcode}")
    else:
        return "N/A"

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

            print("Converting file to text: ", file)
            file_content = extract_text(os.path.join(directory, file))
            if file_content is None:
                print(f"Error: Could not extract text from '{file}'")
                continue

            payload = type_of_document + CSV_format + example + rules + seed_text + file_content

            # print(payload)
            print (f"Processing file...")

            messages = [
                ChatMessage(role="user", content=payload)
            ]

            # No streaming
            chat_response = client.chat(
                model=model,
                messages=messages,
            )

            print("Generating CSV response...")
            line = chat_response.choices[0].message.content.split(',') # Split the response into a list of strings
            print("Line: ", line)
            # Remove all of the double quotes from the strings
            line = [string.replace('"', '') for string in line]

            line.append(geolocation(line[0])) # Append latitude and longitude and zip code to the list

            # Append the file name to the list
            line.append(os.path.join(directory, file))

            print(line)

            csv_array.append(line)
        else:
            print(f"Error: File '{file}' is not a valid file type.")

    # Write the response to a CSV file
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        for row in csv_array:
            writer.writerow(row)
    
    print(f"Response written to '{CSV_FILE}'")



if __name__ == "__main__":
    main()
