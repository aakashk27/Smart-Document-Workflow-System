import os
from dotenv import load_dotenv

load_dotenv()

MAIN_EMAIL = os.getenv("MAIN_EMAIL", " ")
ALTERNATE_EMAIL = os.getenv("SIDE_EMAIL", " ")

DOC_SENDER_DICT = {
    "invoice": MAIN_EMAIL,
    "receipt": MAIN_EMAIL,
    "report": MAIN_EMAIL,
    "other": ALTERNATE_EMAIL,
}
