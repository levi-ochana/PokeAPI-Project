import requests
import random
import os

# Main function to run the game
def main():
    print("Welcome to the Pokémon game!")
    while True:
        print("\nOptions:")
        print("1. Draw a Pokémon")
        print("2. View all saved Pokémon")
        print("3. Exit")
        
        user_input = input("Choose an option (1/2/3): ").strip()
        
        if user_input == "1":
            print("Game start!")
            pokemon_list = fetch_pokemon_list(limit=5)  # Fetch a list of Pokémon
            if pokemon_list:
                # Fetch details for each Pokémon and avoid redundant calls
                pokemon_details_list = []
                for pokemon in pokemon_list:
                    details = fetch_pokemon_details(pokemon['url'])
                    if details:
                        pokemon_details_list.append(details)

                # Display fetched Pokémon names
                print("Pokémon names retrieved:")
                for pokemon in pokemon_details_list:
                    print(pokemon['name'])  # Display names

                # Choose a random Pokémon
                random_pokemon = random.choice(pokemon_details_list)  
                pokemon_name = random_pokemon['name']

                # Check if the random Pokémon already exists in the database
                exists, existing_pokemon = check_pokemon_in_db(pokemon_name)  # Check MongoDB (instead of file)
                if exists:
                    print(f"\n{pokemon_name} already exists in the database.")
                    # Display existing Pokémon details
                    print_pokemon_details(existing_pokemon)
                else:
                    # Save the new Pokémon to the database using the Flask API
                    save_pokemon_to_db(random_pokemon)  # Save to MongoDB via API
                    print(f"\nRandom Pokémon added:")
                    print_pokemon_details(random_pokemon)

        elif user_input == "2":
            display_saved_pokemon()  # Display all saved Pokémon (can be updated to fetch from DB)
        elif user_input == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please enter 1, 2, or 3.")

# Define the Flask API URL (the backend URL)
def get_backend_ip():
    backend_ip = os.getenv('BACKEND_IP', 'localhost')  # Default to 'localhost' if environment variable is not set
    return backend_ip

API_URL = f"http://{get_backend_ip()}:5000/api/pokemon"  # API URL of Flask service

# Function to check if Pokémon exists in the database
def check_pokemon_in_db(pokemon_name):
    response = requests.get(f"{API_URL}/{pokemon_name}")
    if response.status_code == 200:
        return True, response.json()
    else:
        return False, None

# Function to save a Pokémon to the database (via Flask API)
def save_pokemon_to_db(pokemon):
    pokemon_data = {
        "name": pokemon.get('name', 'Unknown'),
        "type": [t['type']['name'] for t in pokemon.get('types', [])],
        "abilities": [a['ability']['name'] for a in pokemon.get('abilities', [])]
    }
    response = requests.post(API_URL, json=pokemon_data)
    if response.status_code == 201:
        print("Pokémon saved to database.")
    else:
        print(f"Failed to save Pokémon: {response.status_code} - {response.text}")

# Function to display saved Pokémon (can be updated to fetch from DB)
def display_saved_pokemon():
    response = requests.get(API_URL)
    if response.status_code == 200:
        pokemon_list = response.json()
        if pokemon_list:
            print("Saved Pokémon in database:")
            for pokemon in pokemon_list:
                print(pokemon['name'])
        else:
            print("No Pokémon found in the database.")
    else:
        print(f"Failed to fetch saved Pokémon: {response.status_code} - {response.text}")

# Function to fetch Pokémon details from an external API (for example, PokeAPI)
def fetch_pokemon_list(limit=5):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon?limit={limit}")
    if response.status_code == 200:
        return response.json()['results']
    print("Failed to fetch Pokémon list.")
    return []

def fetch_pokemon_details(pokemon_url):
    response = requests.get(pokemon_url)
    if response.status_code == 200:
        return response.json()
    print(f"Failed to fetch Pokémon details from {pokemon_url}.")
    return None

# Function to display Pokémon details
def print_pokemon_details(pokemon):
    print(f"Name: {pokemon['name']}")
    
    # Check and print types
    types = pokemon.get('types', [])
    if types:
        print(f"Type: {', '.join([t['type']['name'] for t in types])}")
    else:
        print("Type: Not available")
    
    # Check and print abilities
    abilities = pokemon.get('abilities', [])
    if abilities:
        print(f"Abilities: {', '.join([a['ability']['name'] for a in abilities])}")
    else:
        print("Abilities: Not available")

if __name__ == "__main__":
    main()
