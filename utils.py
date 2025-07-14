import os
import requests
import re
import json
from dotenv import load_dotenv

load_dotenv()


def get_risk_color(risk):
    # get color scheme for risk levels
    colors = {
        "GREEN": {"bg": "bg-green-100", "text": "text-green-800", "icon": "🟢"},
        "YELLOW": {"bg": "bg-yellow-100", "text": "text-yellow-800", "icon": "🟡"},
        "RED": {"bg": "bg-red-100", "text": "text-red-800", "icon": "🔴"},
    }
    return colors.get(
        risk, {"bg": "bg-gray-100", "text": "text-gray-800", "icon": "⚪"}
    )


def text_breaks(text):
    # add line breaks to arabic text for better readability
    if not text:
        return ""

    def __protect_urls(match):
        return match.group(0).replace(".", "___DOT___")

    # protect urls and emails from breaking
    text = re.sub(r"https?://[^\s]+", __protect_urls, text)
    text = re.sub(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", __protect_urls, text
    )

    # add breaks after punctuation and special chars
    # validated on https://regex101.com/r/YBptwe/1
    breaks = [
        r"(?<=\u061F)",  # Arabic question mark, https://www.fileformat.info/info/unicode/char/061f/index.htm
        r"(?<=\u060C)",  # Arabic comma, https://www.fileformat.info/info/unicode/char/60c/index.htm
        r"(?<=[!؟،])",  # Exclamation
        r"(📣📣)",  # special icons
        r"(…)",  # ellipsis
    ]

    # only add breaks after periods if they're followed by a space and not part of a URL/email
    text = re.sub(r"(?<=\.)\s", ".\n", text)

    pattern = "|".join(breaks)
    text = re.sub(pattern, r"\g<0>\n", text)
    text = text.replace("___DOT___", ".")

    return text


def format_data(data):
    # format api response data for template
    if not data or not isinstance(data, dict):
        return None

    resp = data.get("response", {})
    if not resp.get("status"):
        return None

    info = resp.get("data", {})
    risk = get_risk_color(info.get("risk_protocol", "UNKNOWN"))

    return {
        "public_id": info.get("public_id", "N/A"),
        "inquiry": info.get("inquiry", "N/A"),
        "targeted_url": info.get("targeted", "N/A"),
        "risk_protocol": info.get("risk_protocol", "UNKNOWN"),
        "risk_info": risk,
        "organization": {
            "name_ar": info.get("organization", {}).get("name_ar", "غير متوفر"),
            "name_en": info.get("organization", {}).get("name_en", "Not Available"),
        },
        "sector": {
            "name_ar": info.get("sector", {}).get("name_ar", "غير متوفر"),
            "name_en": info.get("sector", {}).get("name_en", "Not Available"),
        },
        "created_at": info.get("created_at", "N/A"),
        "belongs_to": info.get("belongs_to", "N/A"),
        "arabic_text": text_breaks(resp.get("text", "")),
        "status_code": data.get("status_code", 0),
        "website": data.get("website", "N/A"),
        "raw_json": json.dumps(data, indent=2, ensure_ascii=False),
    }
