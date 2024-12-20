import os
import requests
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from dotenv import load_dotenv


load_dotenv()

app = FastAPI()


BREVO_API_KEY = os.getenv('BREVO_API_KEY', None)

class EmailSchema(BaseModel):
    to: str
    subject: str
    message: str


def send_email_to_user(to: str, subject: str, message: str):
    """
    Send an email using the MailerSend API.
    """
    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json",
    }

    data = {
        "sender": {
            "name": "Sender Alex",
            "email": "aakash27khana@gmail.com",
        },
        "to": [
            {
                "email": to,
                "name": "John Doe",
            }
        ],
        "subject": subject,
        "htmlContent": f"<html><head></head><body><p>{message}</p></body></html>",
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return {"status": "success", "message": "Email sent successfully!"}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Email sending failed: {e}")


# @app.post("/send-email/")
# async def send_email_endpoint(email: EmailSchema, background_tasks: BackgroundTasks):
#     """
#     FastAPI endpoint to send an email. 
#     The email will be sent in the background.
#     """
#     background_tasks.add_task(send_email_to_user, email.to, email.subject, email.message)
#     return {"message": "Email is being sent in the background"}



send_email_to_user("12117038@nitkkr.ac.in", "MAIL TEST", "Hello testers!")