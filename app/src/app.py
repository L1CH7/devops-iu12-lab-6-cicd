"""Simple Flask service for CI/CD lab.

Provides health, info and greeting endpoints.
"""

import os
import socket

from flask import Flask, Response, jsonify, request

app: Flask = Flask(__name__)

APP_VERSION: str = "1.1.0"


@app.route("/", methods=["GET"])
def index() -> Response:
    """Return service info as JSON.

    Returns:
        Response: JSON with service name, version and hostname.
    """
    return jsonify(
        {
            "service": "devops-cicd-lab",
            "version": APP_VERSION,
            "hostname": socket.gethostname(),
        }
    )


@app.route("/health", methods=["GET"])
def health() -> Response:
    """Return health status.

    Returns:
        Response: JSON with status ok.
    """
    return jsonify({"status": "ok"})


@app.route("/greeting", methods=["GET"])
def greeting() -> Response:
    """Return greeting message controlled by a feature flag.

    If environment variable FEATURE_NEW_GREETING is set to 'true',
    returns a personalised greeting using optional query param 'name'.
    Otherwise returns the classic message.

    Returns:
        Response: JSON with greeting message.
    """
    if os.environ.get("FEATURE_NEW_GREETING", "false").lower() == "true":
        name: str = request.args.get("name", "World")
        message = f"Hello, {name}! 🎉 (new greeting feature)"
    else:
        message = "Hello, World!"
    return jsonify({"greeting": message})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
