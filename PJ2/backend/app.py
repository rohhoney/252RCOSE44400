from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# Path to stored message file
DATA_PATH = "/data/message.txt"


def read_message():
    
    #TODO:
    #- If DATA_PATH exists, read and return the text inside
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            return f.read()
    #- If it doesn't exist, return an empty string
    return ""


def write_message(msg: str):
    #TODO:
    #- Open DATA_PATH
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_msg = f"{msg} (updated at {now})"


    with open(DATA_PATH, "w") as f:
        f.write(msg) #- Write msg to the file


@app.route("/api/message", methods=["GET"])
def get_message():
    #TODO:
    #- Call read_message()
    message = read_message()
    #- Return { "message": <stored message> } as JSON
    return jsonify({"message": message})

@app.route("/api/message", methods=["POST"])
def update_message():
    #TODO:
    #- Get JSON from request
    data = request.get_json()
    #- Extract the field "message"
    msg = data.get("message","")
    #- Call write_message() to save it
    write_message(msg)
    #- Return { "status": "ok" }
    return jsonify({"status":"ok"})
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"})
# v1 has no /api/health endpoint
# (Students add this in v2)

# v2 TODO:
# - Modify write_message() or update_message() to include a timestamp
#   Format: "<message> (updated at YYYY-MM-DD HH:MM:SS)"
#
# - Add new endpoint /api/health that returns:
#   { "status": "healthy" }


if __name__ == "__main__":
    # Do not change the host or port
    app.run(host="0.0.0.0", port=5001)
