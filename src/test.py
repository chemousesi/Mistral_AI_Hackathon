import requests

def geolocation(address):      

    # Define the URL of the API endpoint
    ADDOK_URL = 'http://api-adresse.data.gouv.fr/search/'

    # Define the parameters for the API request, including the address and limit
    addresse = 'Rue du Valibout - Plaisir'
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


print(geolocation(None))
