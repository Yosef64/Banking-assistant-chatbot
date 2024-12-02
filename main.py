import functions_framework
import google.generativeai as genai
import pandas as pd
import json
import io
from google.cloud import storage
from tools import tools1
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from datetime import datetime
from access import save_session_data,load_session_data
@functions_framework.http
def hello_http(request):
    request_json = request.get_json(silent=True)
    request_args = request.args
    
    if not request_json or 'prompt' not in request_json or 'id' not in request_json:
        return "Invalid request", 400

    prompt, user_id = request_json["prompt"], request_json["id"]
    
    
    genai.configure(api_key="API_KEY")

    generation_config = {
        "temperature": 1.5,
        "top_p": 1,
        "top_k": 64,
        "max_output_tokens": 200,
        "response_mime_type": "text/plain",
    }

    instruction = """
        start with amazing greeting and make sure to verify
        Ask the user to specify their identity:
            - Bank User: If the user identifies themselves as a bank user, request their bank account number and password on same time.
            - Bank Officer: If the user identifies themselves as a bank officer, request their officer ID and password.

        Once the user provides their identity information:
            - For Bank Users:
                1. verify that the account number and password is correct
                2. If the bank account provided is already registered (check without looking into history conversation):
                    - Ask the user how you can assist them further.
                3. If the bank account is not registered:
                    - Ask the user to provide a valid bank account number.

            - For **Bank Officers**:
                1. Verify the officer ID and password.
                2. If the credentials are valid, proceed with the required action.
                3. If the credentials are invalid:
                    - Ask the user to provide valid officer ID and password.

        If someone wants to transfer money to another bank account:
            1. Ensure the receiver’s account number is registered by calling `check_bank_account_existence`.
            2. If the receiver’s account number is not registered:
                - Ask the user to enter a valid account number.
            3. If the receiver’s account number is registered:
                - Proceed with the transfer.
        if bank officer ask to get loan applications, please provide with user (that submit the application) bank account
        only bank officer can see all loan applications and approve loan applications
        """
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=instruction,
        generation_config=generation_config,
        tools=tools1,
    )
    session_data = load_session_data()
    history = session_data.get(user_id, [])
    chat = model.start_chat(enable_automatic_function_calling=True, history=history)
    res = chat.send_message(prompt, safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    })
    if user_id not in session_data:
        session_data[user_id] = []
    
    session_data[user_id].append({"role": "user", "parts": prompt})
    session_data[user_id].append({"role": "model", "parts": res.text})
    save_session_data(session_data)
    
    return res.text

