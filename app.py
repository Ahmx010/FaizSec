from flask import Flask, request, jsonify
import hashlib

stored_hashes = []

app = Flask(__name__)

# Test route (health check)
@app.route('/')
def home():
    return jsonify({"message": "FAIZSEC API is running"})


# Hashing route
@app.route('/hash', methods=['POST'])
def hash_data():
    data = request.json.get("data")

    if not data:
        return jsonify({"error": "No data provided"}), 400

    hashed = hashlib.sha256(data.encode()).hexdigest()
    stored_hashes.append(hashed)

    return jsonify({
        "original": data,
        "hash": hashed
    })


# Verify route (compare hash)
@app.route('/verify', methods=['POST'])
def verify_data():
    data = request.json.get("data")
    given_hash = request.json.get("hash")

    if not data or not given_hash:
        return jsonify({"error": "Missing data or hash"}), 400

    new_hash = hashlib.sha256(data.encode()).hexdigest()
    is_valid = new_hash == given_hash

    return jsonify({
        "valid": is_valid
    })


# Run server (ALWAYS LAST)

@app.route('/stored', methods=['GET'])
def get_stored():
    return jsonify({
        "stored_hashes": stored_hashes
    })

if __name__ == '__main__':
    app.run(debug=True)