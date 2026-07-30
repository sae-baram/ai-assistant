import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "hu")


def language_instruction():
    """Return a short instruction telling the model which language to use.

    For Hungarian (`hu`) we return the instruction in Hungarian so the model
    sees it in the target language.
    """
    lang = DEFAULT_LANGUAGE.lower()
    if lang.startswith("hu"):
        return "A válasz mindig legyen magyar nyelvű."
    return f"Please answer in {DEFAULT_LANGUAGE}."
