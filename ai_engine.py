
import os
import json
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()


def get_config(key, default=None):
    """
    Read configuration from environment variables
    or Streamlit Cloud secrets.
    """

    value = os.getenv(key)

    if value:
        return value

    try:
        import streamlit as st
        return st.secrets.get(key, default)

    except Exception:
        return default


API_KEY = get_config("GEMINI_API_KEY")
MODEL = get_config(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
)

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. "
        "Configure it in your .env file or Streamlit secrets."
    )

client = genai.Client(api_key=API_KEY)


def analyze_complaint(problem, language="English"):
    """
    Analyze a consumer complaint using Gemini.

    Retries temporary server errors using
    exponential backoff.
    """

    from prompts import SYSTEM_PROMPT

    prompt = f"""
    {SYSTEM_PROMPT}

    USER'S PREFERRED LANGUAGE:
    {language}

    CONSUMER COMPLAINT:

    {problem}

    Analyze the complaint and return the requested
    JSON structure.

    Return only valid JSON without Markdown fences.
    """

    max_attempts = 3

    for attempt in range(max_attempts):

        try:

            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config={
                    "response_mime_type": "application/json"
                }
            )

            if not response.text:
                raise ValueError(
                    "Gemini returned an empty response."
                )

            result = json.loads(response.text)

            if not isinstance(result, dict):
                raise ValueError(
                    "Expected a JSON object from Gemini."
                )

            return result

        except Exception as error:

            error_message = str(error).upper()

            is_temporary_error = (
                "503" in error_message
                or "UNAVAILABLE" in error_message
                or "429" in error_message
                or "RESOURCE_EXHAUSTED" in error_message
            )

            if is_temporary_error and attempt < max_attempts - 1:

                wait_time = 2 ** (attempt + 1)

                print(
                    f"Gemini temporarily unavailable. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

                continue

            raise RuntimeError(
                f"Gemini API error: {error}"
            ) from error

    raise RuntimeError(
        "Gemini is temporarily unavailable. "
        "Please try again later."
    )
