import os
import requests

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

import utils

load_dotenv()
app = Flask(__name__)


@app.route("/")
def index():
    """home page"""
    return render_template("index.html")


@app.route("/check", methods=["POST"])
def check():
    """handle website check request"""
    website = request.form.get("website", "").strip()

    if not website:
        return jsonify({"error": "Website is required"}), 400

    api_key = os.getenv("API_KEY")
    if not api_key:
        return (
            jsonify(
                {
                    "error": "API key not configured. Please check your .env file and ensure API_KEY is set."
                }
            ),
            500,
        )

    url = f"https://business.tabayyun.com.sa/business-api/v1/inquiry?inquiry={website}"
    headers = {"X-Authorization": api_key}

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.headers.get("content-type", "").startswith("application/json"):
            data = response.json()
        else:
            data = {"text": response.text}

        result = {
            "status_code": response.status_code,
            "website": website,
            "response": data,
        }

        formatted = utils.format_data(result)

        if formatted:
            return render_template("result.html", data=formatted)
        else:
            return jsonify({"error": "Invalid response format from API"}), 500

    except requests.RequestException as e:
        return jsonify({"error": f"Request failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
