from flask import Flask, render_template, jsonify, request
import requests
import random
import os

app = Flask(__name__)

# Define the Flask API URL
def get_backend_ip():
    backend_ip = os.getenv('BACKEND_IP', 'localhost')  # Default to 'localhost' if environment variable is not set
    return backend_ip

API_URL = f"http://{get_backend_ip()}:5000/api/pokemon"  # URL of Flask service

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/draw")
def draw_pokemon():
    pokemon_list = fetch_random_pokemon_list(limit=5)
    if pokemon_list:
        random_pokemon = random.choice(pokemon_list)
        pokemon_name = random_pokemon['name']

        # Check if the random Pokémon already exists in the database
        exists, existing_pokemon = check_pokemon_in_db(pokemon_name)
        if exists:
            return render_template("draw_pokemon.html", pokemon=existing_pokemon, message=f"{pokemon_name} already exists!")
        else:
            save_pokemon_to_db(random_pokemon)
            formatted_pokemon = {
                "name": random_pokemon["name"],
                "type": [t["type"]["name"] for t in random_pokemon["types"]],
                "abilities": [{"name": a["ability"]["name"], "url": a["ability"]["url"], "is_hidden": a["is_hidden"]} for a in random_pokemon["abilities"]],
                "image_url": random_pokemon["sprites"]["front_default"]
            }
            return render_template("draw_pokemon.html", pokemon=formatted_pokemon, message=f"{pokemon_name} added to the database!")
    return render_template("draw_pokemon.html", message="Error fetching Pokémon.")

@app.route("/saved")
def saved_pokemon_page():
    response = requests.get(API_URL)
    if response.status_code == 200:
        pokemon_list = response.json()
        return render_template("saved_pokemon.html", pokemon_list=pokemon_list)
    return render_template("saved_pokemon.html", message="Error fetching saved Pokémon.")

# Function to check if Pokémon exists in the database
def check_pokemon_in_db(pokemon_name):
    response = requests.get(f"{API_URL}/{pokemon_name}")
    if response.status_code == 200:
        return True, response.json()
    else:
        return False, None

# Function to save a Pokémon to the database
def save_pokemon_to_db(pokemon):
    pokemon_data = {
        "name": pokemon.get('name', 'Unknown'),
        "type": [t['type']['name'] for t in pokemon.get('types', [])],
        "abilities": [a['ability']['name'] for a in pokemon.get('abilities', [])],
        "image_url": pokemon['sprites']['front_default']  # Add image URL
    }
    response = requests.post(API_URL, json=pokemon_data)
    if response.status_code != 201:
        print(f"Failed to save Pokémon: {response.status_code} - {response.text}")

# Function to fetch 5 random Pokémon from PokeAPI
def fetch_random_pokemon_list(limit=5):
    pokemon_list = []
    for _ in range(limit):
        random_id = random.randint(1, 1000)
        pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{random_id}/"
        try:
            response = requests.get(pokemon_url)
            response.raise_for_status()  # Will raise an exception if status code is not 200
            pokemon_list.append(response.json())
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Pokémon data: {e}")
    return pokemon_list

# Function to fetch Pokémon by name from the database
@app.route("/api/pokemon/<name>", methods=["GET"])
def get_pokemon_by_name(name):
    response = requests.get(f"{API_URL}/{name}")
    if response.status_code == 200:
        return jsonify(response.json())
    return jsonify({"error": "Pokémon not found."}), 404

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9000)
