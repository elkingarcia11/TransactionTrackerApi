from email_validator import validate_email

def isValidTransaction(transaction : str):
    # run transaction validation field by field
    # if not valid
        # return false
    # else
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

