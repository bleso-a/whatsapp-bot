import os
import time
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import threading, time, random


# load Mantium credentials
load_dotenv()
mantium_user = os.getenv("MANTIUM_USER")
mantium_password = os.getenv("MANTIUM_PASSWORD")


from mantiumapi import prompt
from mantiumapi import client

# Mantium Token
mantium_token = client.BearerAuth().get_token()
SLEEP_TIME = 5
PROMPT_ID = "98b58a5d-12ff-4e64-868e-4dabf986eac7"

# Init Flask App
app = Flask(__name__)
   
@app.route("/")
def hello():
    return "Welcome to Mantium WhatsApp Bot"


@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = str(request.values.get("Body", "").lower())
    print(incoming_msg)
    qaPrompt = prompt.Prompt.from_id(PROMPT_ID)
        
    result = qaPrompt.execute(incoming_msg)
    time.sleep(SLEEP_TIME)
    result.refresh()
    prompt_result = str(result.output)
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(prompt_result)
    print(msg.body(prompt_result))
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)