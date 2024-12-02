from google.cloud import storage
import pandas as pd
from datetime import datetime
import io
import PyPDF2
import json  


client = storage.Client()
bucket_name = 'banking_assistant'
bucket = client.get_bucket(bucket_name)
def load_session_data():
    try:
        client = storage.Client()
        bucket_name = 'banking_assistant'
        bucket = client.get_bucket(bucket_name)
        blob_name = 'dataset/session.json'
        blob = bucket.blob(blob_name)
        session_data = json.loads(blob.download_as_string())
        return session_data
    except Exception as e:
        print(f"Error loading session data: {e}")
        return {}

def save_session_data(session_data):
    try:
        client = storage.Client()
        bucket_name = 'banking_assistant'
        bucket = client.get_bucket(bucket_name)
        blob_name = 'dataset/session.json'
        blob = bucket.blob(blob_name)
        blob.upload_from_string(json.dumps(session_data))
    except Exception as e:
        print(f"Error saving session data: {e}")

def get_user_info(bank_account):
    try:
        client = storage.Client()
        bucket_name = 'banking_assistant'
        bucket = client.get_bucket(bucket_name)
        file_path = 'dataset/users_status.csv'
        blob = bucket.blob(file_path)
        csv_data = blob.download_as_text()
        df = pd.read_csv(io.StringIO(csv_data))
        df["bank_account"] = df["bank_account"].astype(str)
        result = df[df["bank_account"] == bank_account]
        return result
    except Exception as e:
        print(f"Error fetching user info: {e}")
        return {}

def get_transaction(bank_account):
    try:
        client = storage.Client()
        bucket_name = 'banking_assistant'
        bucket = client.get_bucket(bucket_name)
        file_path = 'dataset/transactions.csv'
        blob = bucket.blob(file_path)

        csv_data = blob.download_as_text()

        df = pd.read_csv(io.StringIO(csv_data))
        df["bank_account"] = df["bank_account"].astype(str)
        result = df[df["bank_account"] == bank_account]
        if result.empty:
            return "You don't have transactions yet!"
        return result
    except Exception as e:
        print(f"Error fetching user transactions: {e}")
        return {}
def commit_transaction(receiver:str,sender:str,amount:int,reason:str):
    try:
        client = storage.Client()
        bucket_name = 'banking_assistant'
        bucket = client.get_bucket(bucket_name)
        file_path = 'dataset/transactions.csv'
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(file_path)
        csv_data = blob.download_as_text()
        df = pd.read_csv(io.StringIO(csv_data))
        sen = change_amount(sender,amount,True)
        if not sen:
            return "Insufficient balance"
        rec = change_amount(receiver,amount,False)
        date = datetime.now()
        receiver_transaction = pd.DataFrame({
        "bank_account": [receiver], 
        "amount": [amount], 
        "transaction_type": ["credited"], 
        "reason": [reason], 
        "transaction_date": [date]
        })
        sender_transaction = pd.DataFrame({
        "bank_account": [sender], 
        "amount": [amount], 
        "transaction_type": ["debited"], 
        "reason": [reason], 
        "transaction_date": [date]
        })
        df = pd.concat([df, sender_transaction,receiver_transaction], ignore_index=True)
        updated_csv = df.to_csv(index=False)
        blob.upload_from_string(updated_csv, content_type='text/csv')
        return "The Transaction successufully committed!"
    except Exception as e:
        return e
def check_existence(bank_account:str):
    try:
        client = storage.Client()
        bucket_name = 'banking_assistant'
        bucket = client.get_bucket(bucket_name)
        file_path = 'dataset/users_status.csv'
        blob = bucket.blob(file_path)
        csv_data = blob.download_as_text()
        df = pd.read_csv(io.StringIO(csv_data))
        df["bank_account"] = df["bank_account"].astype(str)
        result = df[df["bank_account"] == bank_account]
    except Exception as e:
        return True
    return result.empty

def loan_data():
    try:
        client = storage.Client()
        bucket_name = 'banking_assistant'
        bucket = client.get_bucket(bucket_name)
        blob_name = "documents/loan.pdf"  
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)

        pdf_bytes = blob.download_as_bytes()

        pdf_stream = io.BytesIO(pdf_bytes)
        reader = PyPDF2.PdfReader(pdf_stream)
            
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return e
def process_loan_application(userInfo,loan_type,loan_amount):
    try:
        client = storage.Client()
        bucket_name = 'banking_assistant'
        bucket = client.get_bucket(bucket_name)
        blob_name = "dataset/loan_applications.csv"
        blob = bucket.blob(blob_name)
        csv_data = blob.download_as_text()
        df = pd.read_csv(io.StringIO(csv_data))
        date = datetime.now()
        new_tran = pd.DataFrame({
            "applicant_name":[userInfo["user_name"]["0"]],"bank_account":[userInfo["bank_account"]["0"]],"loan_type":[loan_type],"application_date":[date],"application_status":["pending"],"approval_date":["not decided"],"loan_amount":[loan_amount]
        })
        df = pd.concat([df,new_tran],ignore_index=True)
        updated_csv = df.to_csv(index=False)
        blob.upload_from_string(updated_csv,content_type="text/csv")
        return True
    except:
        return False
def get_loan_application():
    try:
        client = storage.Client()
        bucket_name = 'banking_assistant'
        bucket = client.get_bucket(bucket_name)
        blob_name = "dataset/loan_applications.csv"
        blob = bucket.blob(blob_name)
        csv_data = blob.download_as_text()
        df = pd.read_csv(io.StringIO(csv_data))
        records = df.to_dict(orient='records')
        return records
    except:
        return []

def get_user_loan_application(bank_account):
    try:
        client = storage.Client()
        bucket_name = 'banking_assistant'
        bucket = client.get_bucket(bucket_name)
        blob_name = "dataset/loan_applications.csv"
        blob = bucket.blob(blob_name)
        csv_data = blob.download_as_text()
        df = pd.read_csv(io.StringIO(csv_data))
        df["bank_account"] = df["bank_account"].astype(str)
        result = df[df["bank_account"] == bank_account]
        if not result.empty:
            return result.iloc[-1].to_dict()
        return {}
    except:
        return {}
def get_officer(officer_id:str):
    try:
        blob_name = "dataset/bank_officers.csv"
        blob = bucket.blob(blob_name)
        csv_data = blob.download_as_text()
        df = pd.read_csv(io.StringIO(csv_data))
        df["officer_id"] = df["officer_id"].astype(str)
        result = df[df["officer_id"] == officer_id]
        return result
    except Exception as e:
        return {}
        

def modify_loan_application(bank_account:str,decision:str):
    try:
        blob_name = "dataset/loan_applications.csv"
        blob = bucket.blob(blob_name)
        blob = bucket.blob(blob_name)
        csv_data = blob.download_as_text()
        df = pd.read_csv(io.StringIO(csv_data))
        df["bank_account"] = df["bank_account"].astype(str)
        df["application_status"] = df["application_status"].astype(str)
        
        result_index = df[df["bank_account"] == bank_account].index  
        if result_index.empty:
            return "Incorrect bank account provided!"
        
        df.loc[result_index, "application_status"] = "approved"
        df.loc[result_index, "approval_date"] = datetime.now().isoformat()
        csv_updated = df.to_csv(index=False)
        blob.upload_from_string(csv_updated)
        
        return "successfully modified!"

    except Exception as e:
        return "Something went wrong!"
def change_amount(bank_account,amount,isDecrease):
    try:
        blob_name = "dataset/users_status.csv"
        blob = bucket.blob(blob_name)    
        csv_data = blob.download_as_text()
        df = pd.read_csv(io.StringIO(csv_data))

        df["bank_account"] = df["bank_account"].astype(str)
        df["balance"] = pd.to_numeric(df["balance"], errors='coerce') 
        result_index = df[df["bank_account"] == bank_account].index  
        if not result_index.empty:
            current_balance = df.loc[result_index, "balance"].values[0]  # Get the current balance
            if isDecrease and current_balance < amount:
                return False
            if isDecrease:
                df.loc[result_index, "balance"] = df.loc[result_index, "balance"] - amount
            else:
                df.loc[result_index, "balance"] = df.loc[result_index, "balance"] + amount
            csv_updated = df.to_csv(index=False)

            blob.upload_from_string(csv_updated)
        return True
    except:
        return False
