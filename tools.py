import json
from storage_access import modify_loan_application,get_officer,get_user_loan_application,get_loan_application,process_loan_application,load_session_data,save_session_data,get_user_info,get_transaction,commit_transaction,check_existence,loan_data

def get_user_information(bank_account:str):
    """return users bank information based on the bank account the user entered if there is not bank account registed just return there is not bank account register
    Args:
        bank_account (string) : bank account the user entered in history
    
    """
    res = get_user_info(bank_account)
    return res.to_json()
    
def get_user_transaction(bank_account: str):
    """return users recent transactions based on the bank account the user entered in history
    Args:
        bank_account (string) : bank account the user entered in history
    
    """
    result = get_transaction(bank_account)
    return result.to_json()
def proccess_tranactions(sender_account:str,receiver_account:str,reason:str,amount:int):
    """process transaction between two users and return whether the transaction is made succesfully
    Args:
        sender_account (string) : bank account of sender based on current history
        receiver_account (string): bank_account of money receiver the sender mentioned
        reason (string) : the reason for this transaction 
        amount (int) : the amount of money the user want to send
    """
    if sender_account == receiver_account:
        return "The sender account and receiver account mustn't be identical"
    receiver = get_user_info(receiver_account)
    if receiver.empty:
        return "The receiver account is not registered!"
    res = commit_transaction(receiver_account,sender_account,amount,reason)
    return res
def check_bank_account_existence(bank_account:str):
    """check if the bank account number that user provided exist (registered) or not
    Args:
        bank_account (string) : bank account number the user provided
    
    """
    return not check_existence(bank_account)
def advice_about_loan():
    """answer question related to loan and stuff
    """
    result = loan_data()
    return result
def submit_loan_application_form(bank_account:str,loan_type:str,loan_amount:float):
    """process loan application form if the user ask and proceed with provide the following informations
       Args:
            bank_account (string) : the applicant bank account
            loan_type (string) : the type of loan the applicat want
            loan_amount (string) : the amount of money the user want
    """
    userInfo = json.loads(get_user_info(bank_account).to_json())
    if not userInfo["bank_account"]:
        return "Incorrect bank account!"
    result = process_loan_application(userInfo,loan_type,loan_amount)
    if result:
        return "successfully submited"
    return "something went wrong. you want try again"

def get_all_loan_applications():
    """get all loan applications
    """  
    applications = get_loan_application()
    return applications
def users_recent_application(bank_account:str):
    """ return users recent loan application if there is not application or if the json is empty ,
        answer that there is no recent application
        Args:
            bank_account (string) : users bank_account that recently entered
    """  
    application = get_user_loan_application(bank_account)
    
def verify_bank_user(bank_account:str,password:int):
    """check if the password is correct for the bank_account or check if the account if exist
        Args:
            bank_account (string) : bank account of the user
            password (int) : the password the user pass

    """  
    result = get_user_info(bank_account)
    if result.empty:
        return "The user is not registered.Please provide valid bank account"
    user =  result.iloc[-1].to_dict()
    if user.get("password") != password:
        return "Your password is not correct"
    return "Verified successfully" 
def verify_bank_officer(officer_id:str,password:int):
    """verify if the provided officer id and password if correct and matched
        officer_id (string) : bank officer id
        password (int) : bank officer's password
    """
    result = get_officer(officer_id)
    if result.empty:
        return "The officer id is not exist.Please try again"
    officer = result.iloc[-1].to_dict()
    if officer["password"] != password:
        return "The password you provided is not correct!"
    return "Verified successfully!"
def approve_loan_application(bank_account:str,decision:str):
    """make a decision on the loan application with bank_account
        Args:
            bank_account (string) : bank account the officer provide
            decision (string) : the decision of the officer. approve or denied
    """
    return modify_loan_application(bank_account,decision)
    
    
tools1 = [approve_loan_application,verify_bank_officer,verify_bank_user,get_all_loan_applications,submit_loan_application_form,advice_about_loan,check_bank_account_existence,proccess_tranactions,get_user_transaction,get_user_information]
