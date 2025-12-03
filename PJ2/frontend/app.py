from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

# URL of the backend container inside Docker network
BACKEND_URL = "http://backend:5001"


@app.route("/", methods=["GET"])
def index():
    #TODO:
    #- Send a GET request to BACKEND_URL + "/api/message"
    try:
        resp = requests.get(f"{BACKEND_URL}/api/message")
        resp.raise_for_status() #exception handling
    #- Extract the message from the JSON response
        data = resp.json()
        message = data.get("message", "")
    except Exception:
        message = ""

    #- Render index.html and pass the message as "current_message"
    return render_template("index.html", current_message=message)

@app.route("/update", methods=["POST"])
def update():
    #TODO:
    #- Get the value from the form field named "new_message"
    new_message = request.form.get("new_message", "")

    try:
    #- Send a POST request to BACKEND_URL + "/api/message"
        requests.post(
                f"{BACKEND_URL}/api/message",
    #  with JSON body { "message": new_message }
                json={"message": new_message},
                timeout=3,
        )
    except Exception:
        pass

    #- Redirect back to "/"
    return redirect("/")

# v2 jTODO:
# - Change page title (in HTML)
# - Parse timestamp from backend message
# - Show "Last updated at: <timestamp>" in the template


if __name__ == "__main__":
    # Do not change the host or port
    app.run(host="0.0.0.0", port=5000)
