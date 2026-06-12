from flask import Flask, request, jsonify

app = Flask(__name__)

def response():
    return jsonify({
        "remote_addr": request.remote_addr,
        "x_forwarded_for": request.headers.get("X-Forwarded-For"),
        "headers": dict(request.headers)
    })

@app.route("/")
def root():
    return response()

@app.route("/chain")
def chain():
    return response()

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)