import os
import time
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

# load Mantium credentials
load_dotenv()
mantium_user = os.getenv("MANTIUM_USER")
mantium_password = os.getenv("MANTIUM_PASSWORD")

from mantiumapi import prompt
from mantiumapi import client

# Mantium Token
mantium_token = client.BearerAuth().get_token()

# Init Flask App
app = Flask(__name__)


@app.route("/")
def hello():
    return "Welcome to Mantium WhatsApp Bot"


@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = str(request.values.get("Body", "").lower())
    print(incoming_msg)
    responded = False
    if type(incoming_msg) == str:
        qaPrompt = prompt.Prompt.from_id("98b58a5d-12ff-4e64-868e-4dabf986eac7")
        result = qaPrompt.execute(incoming_msg)
        result.refresh()
        prompt_result = str(result.output)
    else:
        prompt_result = "I could not retrieve an answer for you, try again"
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(prompt_result)
    responded = True
    
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)