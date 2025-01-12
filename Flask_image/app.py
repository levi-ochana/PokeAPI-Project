from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import socket
from bson.objectid import ObjectId

app = Flask(__name__)

# Function to get the appropriate MongoDB URI
def get_mongo_uri():
    try:
        # Try to resolve DNS for "mongo" (for Docker container or remote server)
        socket.gethostbyname("mongo")
        # If successful, return the URI for the Docker container
        return "mongodb://admin:secret_password@mongo:27017/pokemon_db?authSource=admin"
    except socket.gaierror:
        # If unable to resolve "mongo", fallback to localhost
        print("Failed to connect to mongo container, falling back to localhost.")
        return "mongodb://localhost:27017/pokemon_db"

# Set MongoDB URI dynamically
app.config["MONGO_URI"] = get_mongo_uri()

# Now create the PyMongo object with the configured URI
mongo = PyMongo(app)

@app.route("/")
def index():
    return "Connected to MongoDB!"

# Function to convert ObjectId to string and handle dict/list
def json_serializable(obj):
    if isinstance(obj, ObjectId):
        return str(obj)  # Convert ObjectId to string
    elif isinstance(obj, dict):
        return {key: json_serializable(value) for key, value in obj.items()}  # Handle dicts recursively
    elif isinstance(obj, list):
        return [json_serializable(item) for item in obj]  # Handle lists recursively
    return obj  # Return other types as is

@app.route("/api/pokemon/<name>", methods=["GET"])
def get_pokemon_by_name(name):
    try:
        # Searching the database by the Pokémon's name
        pokemon = mongo.db.pokemon.find_one({"name": name})
        if pokemon:
            return jsonify(json_serializable(pokemon))  
        return jsonify({"error": "Pokémon not found."}), 404  
    except Exception as e:
        return jsonify({"error": f"Error fetching Pokémon by name: {str(e)}"}), 500 

@app.route("/api/pokemon", methods=["GET"])
def get_pokemon():
    try:
        # Retrieving all Pokémon from the database
        pokemon_list = mongo.db.pokemon.find()
        return jsonify([json_serializable(pokemon) for pokemon in pokemon_list])
    except Exception as e:
        return jsonify({"error": f"Error fetching all Pokémon: {str(e)}"}), 500

@app.route("/api/pokemon", methods=["POST"])
def add_pokemon():
    try:
        # Receiving the Pokémon data from the request body
        data = request.get_json()

        # Checking if all required fields are provided
        if not all(key in data for key in ["name", "type", "abilities", "image_url"]):
            return jsonify({"error": "Missing required fields: name, type, abilities, image_url"}), 400

        # Preparing the Pokémon data to be inserted into the database
        pokemon = {
            "name": data["name"],
            "type": data["type"],
            "abilities": data["abilities"],
            "image_url": data["image_url"]  # Add image URL here
        }

        # Inserting the Pokémon into the database
        mongo.db.pokemon.insert_one(pokemon)
        return jsonify({"message": "Pokémon saved to database."}), 201
    except Exception as e:
        return jsonify({"error": f"Error saving Pokémon: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
