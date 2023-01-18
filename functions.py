from email_validator import validate_email
from schemas import Transaction

def isValidTransaction(transaction : str):
    # run transaction validation field by field
    # if not valid
        # return false
    # else
    return True
    
def fieldsAreValid(transaction : Transaction):
    # check if all fields are valid
    #check if updating creates conflicts
    # if not
     # return false
    #else
    return True

def emailIsValid(email : str):
    try:
        validate_email(email)
    except:
        return False
    
   
    # check if api key and email exist in db
    # if either do not
        # return false
    return True

def isValidVerificationCode(code : str, email : str):
    # if code and email are not valid
        # retrn false
    #else 
    return True