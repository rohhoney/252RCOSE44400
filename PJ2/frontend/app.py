from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

# URL of the backend container inside Docker network
BACKEND_URL = "http://backend:5001"


@app.route("/", methods=["GET"])
def index():
    try:
        resp = requests.get(f"{BACKEND_URL}/api/message", timeout=3)
        resp.raise_for_status()
        data = resp.json()
        raw_message = data.get("message", "")
    except Exception:
        raw_message = ""

    # v2: message 문자열에서 timestamp 파싱
    prefix = " (updated at "
    timestamp = ""
    message = raw_message

    idx = raw_message.rfind(prefix)
    if idx != -1 and raw_message.endswith(")"):
        timestamp = raw_message[idx + len(prefix):-1]  # 괄호 빼고
        message = raw_message[:idx]

    return render_template(
        "index.html",
        current_message=message,
        last_updated=timestamp,
    )

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
